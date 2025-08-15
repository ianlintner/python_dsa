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
  - post_id (Snowflake),
