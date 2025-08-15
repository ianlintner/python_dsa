Title: Staff-level System Design Interview Script — Design Facebook (Social Network) Clone

Format: Full conversation transcript between Interviewer (I) and Candidate (C). Target: staff-level depth on feed design, graph/storage, ranking, privacy, multi-region, and failure handling.

I: Design a Facebook-style social network. Core: users can befriend (mutual), post text/media, like/comment, and view a ranked News Feed that includes friends, groups, and pages. Ignore ads and live video. You have ~45 minutes. What’s your plan?

C: I’ll clarify requirements and SLOs, establish scale assumptions, define APIs, propose a high-level architecture, then deep-dive into News Feed (candidate generation + ranking), privacy enforcement, data model, multi-region, and reliability. I’ll end with capacity/cost and failure modes.

I: Start with requirements.

C:
- Functional
  - User graph: friend requests (mutual), follow pages, join groups
  - Post creation: text, images/video pointers; visibility (public/friends-only/group/page scope)
  - News Feed: ranked feed combining friends/groups/pages; infinite scroll
  - Engagements: like, comment; counters
  - Notifications: basic for comments/likes/mentions (defer details)
  - Search: user/page/group lookup (post search optional MVP)
- Non-Functional
  - Feed read latency: P50 < 200ms, P99 < 800ms from edge (warm)
  - Post write: P99 < 400ms including media pointer
  - Privacy correctness over availability for scoped content; no privacy leaks
  - High availability for reads (4 nines target in steady state), eventual consistency acceptable for feed order/counters
  - Multi-region active-active reads, region-local writes where possible

I: Scale assumptions?

C:
- Assumptions (tunable)
  - MAU 2B; DAU 1B; peak concurrent users 100–150M
  - Posts/day: 1B; likes/day: 20B; comments/day: 3B
  - Feed views/day: 100B → ~1.16M rps avg; regional peaks 5–10M rps
  - Friends: median ~300; heavy tails
  - Media: large fraction; stored via object store + CDN; posts store media pointers
- Implications
  - Read-heavy feed; must blend precomputation (candidates) with on-read ranking/caching
  - Privacy checks at candidate generation and at read to prevent leaks
  - Massive fanout cost if naive; rely on efficient candidate stores + caches

I: Define public/internal APIs and SLOs.

C:
- Public (behind API Gateway + Auth + Rate Limiter)
  - POST /v1/users/{id}/posts { text, media_ids?, visibility, target_group_id? }
    - returns: { post_id, created_at }
  - GET /v1/users/{id}/feed?cursor=X&limit=50
    - returns: [{ post_id, actor, snippet, media, like_count, comment_count, ... }]
  - POST /v1/friends/requests { to_user_id } ; POST /v1/friends/accept { request_id }
  - POST /v1/posts/{post_id}/likes ; POST /v1/posts/{post_id}/comments { text }
  - GET /v1/users/{id} ; GET /v1/pages/{id} ; GET /v1/groups/{id}
- Internal
  - Graph Service (TAO-like): edges (friend, member_of, follows)
  - Content Service: posts/comments CRUD
  - Feed Service: candidate generation, ranking, feed assembly
  - Feature Store: online features for ranking; offline store for training
  - Media Service: signed URLs to object store/CDN
  - Notification Service; Search/Indexing
- SLOs
  - GET feed: P99 < 800ms edge; 95th percentile cache hit > 90%
  - POSTs: P99 < 400ms; writes are durable (quorum)

I: High-level architecture?

C:
- Edge
  - Anycast DNS, CDN for media; API Gateway with WAF/rate limits; global session/auth
- Services (stateless)
  - Graph Service: friendship, membership, follow relationships; adjacency lists with secondary indexes; privacy lists (blocked)
  - Content Service: posts, comments, attachments; write-through to primary store, publish to streams
  - Feed Service: candidate generation, fanout queues, online ranking, feed cache assembly
  - Engagement Service: likes/comments counters (approximate in cache, reconcile to source of truth)
  - Search/Indexing; Notification; Profile/Identity
- Streaming
  - Kafka/PubSub topics: posts, likes, comments, graph mutations, feed-candidate updates
  - Stream processors: candidate builders, feature updaters, integrity signals
- Storage
  - Graph Store: TAO-like over sharded MySQL/Cassandra with memcache/Redis tier
  - Content Store: sharded MySQL/Spanner/Cassandra for posts/comments (time-partitioned)
  - Feed Stores:
    - Candidate Store: per-user pools of eligible stories (friends/groups/pages)
    - Feed Cache: Redis timeline fragments per user (ids + scores + metadata)
    - Cold/long-term: persistent per-user feed/source-of-truth for backfill/debug
  - Feature Store: online (Redis/KeyDB) + offline (HDFS/BigQuery)
  - Media: object storage + CDN
- Observability
  - Tracing, metrics (tail latency, hit ratios), logging, DLQs, replay harness

I: Deep-dive the News Feed. How do you build and serve it?

C:
- Definitions
  - Candidate generation: retrieve eligible stories for a viewer (friends’ posts, group posts for groups the user belongs to, page posts the user follows), applying privacy filters
  - Ranking: score candidates using ML model and constraints; assemble top-K with diversity
- Strategy
  - Hybrid: maintain per-user Candidate Store (precomputed rolling window) updated by streams + on-demand refresh; rank on read using online features; cache feed fragments
- Candidate Generation
  1) On new post event:
     - Determine visibility scope: public, friends-only, group, page followers
     - Produce events to “candidate-build” streams keyed by viewer segments
     - For friends-only: enumerate author’s friends (bounded fanout) → append post_id into each friend’s candidate pool with lightweight metadata (author_id, created_at, type)
     - For groups/pages: push to member/follower candidate pools; throttle for very large pages (celebrity/page problem) and instead mark as “global candidate” to be pulled on read
  2) On viewer read or background refresh:
     - Pull recent from friends since last checkpoint; merge with group/page deltas
     - Apply blocklists/muted users; privacy ACLs
     - Trim candidate pool by recency and size (e.g., last N days or M posts)
- Ranking & Assembly
  - Online features: user-author affinity, freshness, engagement prediction (pCTR/pLike), content type, negative feedback, inventory saturation
  - Ranker: GBDT or DNN; top-K via heap; apply constraints (e.g., limit consecutive posts from same author; diversity of sources/types)
  - Attach hydration: counters (approx), preview text, media pointers
  - Cache: write ranked chunk (e.g., 100 items) to Redis: feed:{user_id}:{shard}
  - Pagination: cursor into cached ranked list; background refresh to maintain head freshness
- Cache Strategy
  - Head (first 50–200 items) cached; tail fetched from candidate store and reranked as needed
  - Soft TTL with background refresh; request coalescing to prevent stampede
- Celebrity/Page Problem
  - For pages with tens of millions followers: avoid per-follower writes; store page posts in an author/page shard; at read, merge limited “hot” page posts using small K and cache per-viewer merged results
  - Maintain “viewer × hot-pages” premerge cache based on follows and regional popularity

I: How do you enforce privacy?

C:
- Privacy Model
  - Per-post ACL: public, friends-only, friends-of-friends (optional), custom lists, group/page scope
  - Blocks: user-level blocks override all; hide in both directions
- Enforcement
  - Write Path: validate ACLs; annotate post with immutable visibility scope and ACL tokens
  - Candidate Generation: apply ACL filters early — only emit to eligible viewers’ candidate pools; for large scopes (public/page), candidates are fetchable but still re-checked
  - Read Path: re-validate ACLs at assembly (cheap check using ACL tokens + graph membership cache) to prevent leaks due to eventual consistency
- Data Separation
  - Separate stores/namespaces for private groups; avoid mixing public indexes with private content; search index respects ACL tokens

I: Describe the data model.

C:
- Graph
  - Nodes: user, page, group
  - Edges: FRIEND(user,user) mutual; FOLLOWS(user,page); MEMBER(user,group); BLOCK(user,user)
  - Partition by user_id/page_id/group_id; maintain forward/backward adjacency lists
- Post
  - post_id (Snowflake), author_id, created_at, visibility (enum), scope_id (nullable for group/page), text, media_refs[], privacy_tokens, soft_delete, edit_history_meta
  - secondary: index by author_id + created_at (user timeline), by scope_id for groups/pages
- Comment
  - comment_id (Snowflake), post_id, author_id, created_at, text, parent_comment_id (for threads), soft_delete
  - secondary: post_id → recent comments (bounded)
- Candidate Store
  - candidates:{viewer_id} → list of {post_id, source_type(friend|group|page), author_id, created_at, coarse_score?, acl_token}
- Feed Cache
  - feed:{viewer_id}:{shard} → list of {post_id, score, metadata} (ranked)
- Counters (approx online + durable offline)
  - likes:{post_id} (Redis hash/integer), comments:{post_id}; periodic write-behind to durable store
- Privacy/ACL
  - acl_token on each post embeds visibility and scope; read path checks token against viewer graph/membership caches
- Notifications
  - notif:{user_id} append-only log for events (comment on your post, friend request, etc.)

I: Walk me through the write path for a new post.

C:
- Write Path (POST create)
  1) Validate auth and visibility; compute acl_token (e.g., bit flags + scope id)
  2) Generate post_id (Snowflake), persist to Content Store with quorum write
  3) Publish event to Kafka: posts topic {post_id, author_id, visibility, scope, created_at}
  4) Media pointers validated separately; text sanitized; links scanned asynchronously
  5) Stream processors:
     - For friends-only: look up author’s friends (Graph Service) and append to each friend’s Candidate Store
     - For group/page: for small/medium audiences, append to member/follower candidate pools; for huge pages, mark as global candidate for pull-on-read to avoid massive fanout
  6) Write minimal author’s own timeline (for profile view)
  7) Return {post_id}

I: And the read path for News Feed?

C:
- Read Path (GET feed)
  1) Resolve viewer session → user_id; apply rate limits
  2) Try Redis Feed Cache: feed:{viewer_id}:{head}. If present and fresh, return first page and next cursor
  3) On cache miss/stale:
     - Fetch N candidates from Candidate Store (viewer_id), merging with “hot” page/group posts as needed
     - Filter by privacy using acl_token + graph/membership caches; remove blocked/muted authors
     - Hydrate online features (affinity, freshness, lightweight engagement priors)
     - Rank via online model; enforce constraints (diversity, author caps)
     - Materialize ranked chunk into Feed Cache with soft TTL
  4) Hydrate post payloads: batch fetch post bodies, counters from Redis (fallback to durable store)
  5) Return page; kick background task to refresh next chunk

I: What consistency guarantees do you provide?

C:
- Consistency
  - Content writes: strongly durable (quorum/transactional per shard)
  - Feed order: eventual; posts may appear with slight delay due to streaming/candidate building
  - Privacy: best-effort strong — enforced at candidate build and re-checked at read; if graph/membership is stale, read-time check prevents leaks
  - Counters: approximate in real time; durable reconciliation jobs for accuracy
- Idempotency
  - Post creation uses idempotency keys on retries; stream processors are idempotent (checkpoints, exactly-once or effectively-once via dedupe keys)

I: How do you handle multi-region?

C:
- Multi-Region
  - Active-active for reads; region-local caches and feed assembly
  - Writes: region-local primaries per shard with async cross-region replication (or globally consistent store if available, with cost/latency tradeoffs)
  - Streams: Kafka with Mirror topics; per-region candidate builders; DLQs per region
  - Graph: TAO-like cache layer per region; write-through to backing store; conflict resolution by last-write-wins on edge version or CRDT where applicable
  - Disaster Recovery: periodic snapshots for content and graph; replay streams for candidate rebuild; RPO minutes, RTO ≤ 1 hour
- Federation of Pages/Groups
  - Very large pages/groups can be region-pinned for write locality; readers merge regionally “hot” content with bounded lookback

I: Capacity planning quick math?

C:
- Capacity (back-of-envelope)
  - Feed views/day 100B → ~1.16M rps avg; peaks up to ~5–10M rps regionally
  - Target 90%+ cache hit for head fragments → origin/ranking load ~100k–500k rps globally
  - Candidate inserts:
    - 1B posts/day; average 300 friends → naive 300B inserts/day is infeasible
    - Mitigations: only recent posts enter candidate pools; deduplicate authors; cap pool sizes; for large pages/groups use pull-on-read
  - Storage growth:
    - Posts: 1B/day × 1 KB avg ⇒ ~1 TB/day raw; 3x replication ⇒ ~3 TB/day
    - Comments/likes dominate event volume; counters compressed in aggregates; cold data offloaded to object storage

I: What about failure modes and mitigations?

C:
- Failure Modes
  - Cache stampede: use request coalescing, soft TTL, serve-stale, background refresh
  - Stream backlog: autoscale processors, prioritization (viewer self, close friends), DLQ with redrive, backpressure on writes if needed
  - Hot keys: celebrity pages; mitigate with pull-on-read, sharded caches, per-key rate caps
  - Partial graph outages: fall back to cached ACL tokens; conservative deny on ambiguity to avoid leaks
  - Model outages: degrade to recency-based ranking; keep UX functional
- Safe Deploys
  - Shadow traffic for new ranker; dark reads for new candidate builders; canaries with SLO guards and auto-rollback

I: Discuss security, privacy, and abuse.

C:
- Security/Privacy
  - Strong isolation for private groups; separate indexes; ACL tokens validated on read
  - Data minimization: redact PII from logs; access via fine-grained IAM; audit trails
  - E2E not required for feed, but TLS everywhere; service mTLS; secrets via KMS
- Abuse/Integrity
  - Spam detection via graph + velocity + text signals; demote/suppress at ranking
  - Harassment/blocked users: hard filters at candidate and read time
  - Media/links scanning; quarantine pipeline; user reporting with fast takedown
- Compliance
  - Right-to-erasure pipeline: tombstones propagate to feed caches, candidate stores, search indexes

I: How do groups and pages differ from friends’ content?

C:
- Groups
  - Membership scope; stricter privacy; per-group moderation; candidate pools segmented per group; reader must be MEMBER(user, group)
- Pages
  - One-way follow; very large audiences; avoid fanout-on-write at size; rely on hot post pull-on-read and per-viewer merge caches

I: Notifications in brief?

C:
- Notifications
  - Write lightweight events on comment/like/reply; batch/coalesce; per-user notif log with read markers
  - Mobile push via dedicated service; rate limits and quiet hours; privacy-aware payloads

I: If you had time to evolve ranking?

C:
- Ranking Evolution
  - Multi-stage: candidate generation → lightweight pre-ranker → heavy ranker with richer features
  - Feature store: consistent online/offline features; backfills for training
  - Feedback loops: negative feedback (hide, snooze) incorporated; exploration vs exploitation
  - Integrity constraints: cap low-quality content; diversity and freshness guardrails

I: Summarize the key tradeoffs you chose.

C:
- Hybrid candidate strategy reduces write amplification while preserving personalization
- Strong privacy enforcement with read-time checks sacrifices some latency for correctness
- Approx counters + durable reconciliation offer low latency without strict transactional cost
- Active-active reads with async replication accept bounded staleness for availability
- Degradation paths (recency ranker) maintain UX under model or stream failures

I: Looks comprehensive. Let’s stop here.
