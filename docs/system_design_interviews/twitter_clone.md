Title: Staff-level System Design Interview Script — Design Twitter (X) Clone

Format: Full conversation transcript between Interviewer (I) and Candidate (C). The goal is to demonstrate senior/staff-level depth, tradeoff reasoning, capacity planning, and failure-handling.

I: Let’s design a simplified Twitter clone. Core features: users can tweet, follow users, and see a home timeline. We’ll ignore ads, DMs, and long-form for now. You have 35–45 minutes. How would you approach this?

C: I’ll start by clarifying requirements, drafting APIs and SLOs, estimating scale, proposing a high-level architecture, then deep-diving into home timeline fanout strategy, storage, and multi-region. Finally, I’ll cover reliability, cost, and abuse/fraud controls.

I: That works. What are your functional and non-functional requirements?

C:
- Functional
  - Post Tweet (text up to 280 chars, optionally media pointer)
  - Follow/Unfollow
  - Read Home Timeline (posts from people you follow, reverse-chronological, basic ranking optional)
  - Read User Timeline (only that user’s tweets)
  - Engagements (Like, Retweet) — counters surface on tweets
  - Basic Search (optional MVP: hashtag/keyword)
- Non-Functional
  - Read-heavy system; low latency reads: Home timeline P50 < 200ms, P99 < 1s from edge
  - Write durability: tweets must persist with at-least once indexing to derived stores
  - Availability over strong consistency for timelines (eventual consistency acceptable)
  - Multi-region read scaling; disaster recovery RPO ≤ minutes for core writes; RTO ≤ 1 hour target

I: Give me some scale assumptions to anchor design choices.

C:
- Scale Assumptions (order-of-magnitude; can tune)
  - DAU: 100M
  - Tweets/day: 300M → ~3.5k writes/sec average, peak 10x → ~35k tps
  - Home timeline reads/day: 50B views → ~580k reads/sec average, peaks up to ~3–5M rps regionally during events
  - Follows: avg 200 followings/user; heavy tail with “celebrities” at 10M+ followers
  - Media: stored via object store + CDN, but we’ll mostly handle pointers in Tweet objects
- Implications
  - Read-heavy: timeline must be cached and/or precomputed
  - Write fanout for normal accounts, pull for superstars (hybrid fanout)

I: Propose APIs and SLOs.

C:
- Public APIs (behind API Gateway; authenticated)
  - POST /v1/tweets
    - body: { user_id, text, media_ids? }
    - returns: { tweet_id, created_at }
    - SLO: P99 < 300ms (excluding media upload)
  - GET /v1/timeline/home?user_id=U&cursor=X&limit=50
    - returns: [{tweet...}] with pagination
    - SLO: P99 < 500ms from edge (warm cache)
  - GET /v1/timeline/user?user_id=U&cursor=X&limit=50
  - POST /v1/follow { follower_id, followee_id }
  - POST /v1/unfollow { follower_id, followee_id }
  - POST /v1/like { user_id, tweet_id }
  - POST /v1/retweet { user_id, tweet_id }
- Internal APIs
  - ID generation service (Snowflake-like)
  - Fanout service: enqueue fanout jobs; backpressure controls
  - Graph service: follow relationships, consistency guarantees
- Edge
  - CDN for media and potentially static assets
  - Global API gateway with rate limiting, auth, and WAF

I: High-level architecture?

C:
- Ingress/Edge
  - Global Anycast + CDN + API Gateway (Auth, Rate Limiter, WAF)
- Services (stateless, autoscaled)
  - Tweet Service: validate, ID-gen, write to primary store, enqueue indexing/fanout
  - Timeline Service: home timeline reads, user timeline reads, pagination
  - Graph Service: follow/unfollow, follower/following queries; supports bulk reads for fanout
  - Engagement Service: like/retweet counters; anti-dup; eventual consistency to counters
  - Search/Indexing Service: tokenize, index in search cluster (e.g., Elasticsearch/OpenSearch)
  - Media Service: pointers to object storage (e.g., S3/GCS), signed URLs
- Async/Streaming
  - Durable queue (Kafka/PubSub) for fanout jobs, index updates, metrics
  - Stream processors: fanout workers, enrichment, anomaly detection
- Storage
  - Tweets: time-ordered store with high write throughput (Cassandra/DynamoDB/Bigtable)
  - Home Timelines: Redis/Memcache lists per user (LRU with TTL), backed by persistent timeline store (Cassandra/DynamoDB) for cold backfill
  - Graph: adjacency lists partitioned by user_id (Cassandra/DynamoDB or specialized graph store/TAO-like)
  - Counters: Redis with periodic write-behind to source of truth
  - Search: OpenSearch/Elasticsearch
  - ID Gen: Snowflake (time+shard+sequence)
- Observability & Control
  - Tracing, metrics, structured logs; redrive dead-letter queues; feature flags

I: Deep-dive: How do you build the home timeline?

C:
- Strategy: Hybrid Fanout
  - For normal users (followers ≤ threshold T, e.g., 500k): Fanout-on-write
    - When a tweet arrives, push references (tweet_id) onto followers’ home timeline lists
    - Store in Redis for hot timelines and a persistent timeline store for durability/cold reads
  - For celebrities (followers > T): Fanout-on-read
    - Do not push to millions of timelines. Instead, store the tweet in an author shard and merge at read time
- Read Path
  - GET home timeline:
    1) Check Redis list: timeline:{user_id} (most recent N items, e.g., 600–2000 ids)
    2) If cache miss or need deeper pagination, read from persistent timeline store
    3) Merge celebrity authors’ recent tweets on the fly if needed (bounded lookback window)
    4) Hydrate tweet bodies from tweet store (batch get by tweet_id), attach counters from cache
    5) Return
- Write Path
  - POST tweet:
    1) Generate tweet_id (Snowflake)
    2) Persist tweet to primary store (quorum write) for durability
    3) Produce fanout job to Kafka (topic: fanout)
    4) Index in search asynchronously
  - Fanout Worker:
    1) Get followers from Graph Service (possibly paginated)
    2) For each follower:
       - LPUSH tweet_id to Redis timeline list
       - Also append to persistent timeline table (user_id, tweet_id, created_at)
    3) Throttle and shard the work; avoid hot partitions; retry with backoff

I: How do you size this and handle the celebrity problem?

C:
- Capacity (back-of-envelope)
  - Assume 300M tweets/day, avg 200 followers ⇒ 60B fanout inserts/day
  - Avg ~700k inserts/sec, peak ~7M/sec (10x). We cannot push all. Hence hybrid approach.
- Celebrity Threshold
  - We set a threshold T for push fanout. For users > T followers (e.g., 500k), we skip push and require read-time merge.
  - This reduces worst-case fanout load from millions to O(1) per tweet per celebrity.
- Read-time Merge Cost
  - At read, we maintain a short bounded list of last K celebrity tweets per followed celebrity in a min-heap/merge-iterator
  - Optimize by caching per-user “hot celebrity” merge list and refreshing asynchronously
- Cold Start and Backfill
  - On sign-in or long inactivity, rebuild home timeline by pulling recent tweets from top followed authors, merge, then rewarm cache

I: What about the data model?

C:
- Tweet
  - tweet_id (Snowflake, sortable by time)
  - user_id (author)
  - text (≤280 chars)
  - media_refs (optional)
  - created_at, language, visibility flags
- User Graph
  - following:{user_id} → set/list of followee_ids
  - followers:{user_id} → set/list of follower_ids (batched reads for fanout)
  - Store in partitioned KV columnar store with secondary indexes on user_id
- Timeline
  - home_timeline:{user_id} → ordered list of tweet_ids (Redis)
  - persistent_timeline table: (user_id, time_bucket, [tweet_ids]) or (user_id, created_at, tweet_id)
- Counters
  - like_count, retweet_count in Redis hash; periodic reconcile to durable store
- Search Index
  - Inverted index of tokens → tweet_ids; de-duplicate, stopword/snowball

I: Discuss consistency and failure modes.

C:
- Consistency
  - Tweets: strong durability (quorum writes), monotonic IDs
  - Timelines: eventual consistency; a new tweet may appear with delay due to fanout queues
  - Counters: eventual; we accept temporary staleness, reconcile periodically
- Failure Modes
  - Queue Backlog: spikes cause fanout lag — mitigate with autoscaled workers, priority queues (own timeline first, then close friends, then the rest), DLQ + redrive
  - Hot Keys: celebrity timelines or massive follower set; mitigate via hybrid strategy, key sharding, and rate caps
  - Cache Stampedes: protect with request coalescing, soft TTL + background refresh
  - Partial Region Outage: route reads to healthy regions; write fallback to active region; reconcile timelines asynchronously
  - Tweet Store Partition Hotspots: route by tweet_id (time-based) with many logical shards; use compaction strategy to spread load

I: How do you handle rate limiting and abuse?

C:
- Rate Limiting
  - Token bucket per user/app/IP at API gateway; separate limits for read and write
  - Sliding window for visibility endpoints; stricter write quotas; burst vs sustained controls
  - Adaptive limits using anomaly signals (new accounts, IP reputation, ASN, device fingerprint)
  - Per-user, per-app, per-endpoint buckets; safelists for internal jobs
- Abuse and Integrity
  - WAF rules at edge; bot heuristics; CAPTCHA/step-up auth on risky flows
  - URL and media scanning via async pipelines; quarantine flags
  - Spam/fake engagement detection with features from graph + velocity; action throttles
- Security
  - OAuth2/OIDC for user auth; HMAC request signing for service-to-service; mTLS internally
  - Principle of least privilege; secrets via KMS; audit logging; row-level privacy tags
- Cost/Perf Optimizations
  - Cache tweet bodies and timelines aggressively; compaction of cold timelines by time buckets
  - Batch hydration of tweets and counters; coalesced requests to stores; tail latency SLAs
  - Storage planning: 300M tweets/day, 1 KB avg payload → ~300 GB/day raw; 3x replication → ~900 GB/day
- Multi-Region and DR
  - Active-active reads; region-local writes with global ID-gen (time-ordered)
  - Async x-region replication for tweet store and persistent timelines; bounded staleness
  - Regional fanout: local queues/workers; cross-region failover switches; DLQ redrive
  - Disaster recovery: periodic snapshots + change streams; RPO minutes, RTO ≤ 1 hour
- Data Lifecycle and Privacy
  - Deletion pipeline: tombstones propagate to caches, timelines, search index
  - Retention policies for logs/metrics; compliance (GDPR/CPRA) with subject erasure jobs
- Rollout and Testing
  - Dark reads for new timeline service; shadow traffic; canaries with SLO guards
  - Replay harness using Kafka topics for correctness and performance regression tests

I: If you had more time, how would you evolve ranking for the home timeline?

C:
- Introduce a ranking service:
  - Candidate generation: recent tweets from follow graph, author affinity, real-time signals
  - Feature store (online/offline) for user, author, tweet features
  - Ranker (LR, GBDT, or neural) with A/B experiment framework
  - Guardrails: diversity/novelty constraints; spam demotion; health metrics

I: Summarize tradeoffs you chose.

C:
- Hybrid fanout balances write amplification vs read merge cost; celebrity threshold avoids hot partitions
- Eventual consistency for timelines enables availability and cost efficiency
- Redis + persistent store for timelines yields low-latency warm reads with durable backfill
- Counters are approximate in real-time; reconciled for accuracy later
- Active-active reads with async replication prioritize availability; accept bounded staleness

I: Looks solid. Let’s stop here.
