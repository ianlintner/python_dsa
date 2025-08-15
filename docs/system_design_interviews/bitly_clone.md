Title: Staff-level System Design Interview Script — Design Bitly (URL Shortener) Clone

Format: Full conversation transcript between Interviewer (I) and Candidate (C). The goal is to demonstrate senior/staff-level depth, tradeoff reasoning, capacity planning, and failure-handling.

I: Let’s design a Bitly-style URL shortener. Core features: create a short link that redirects to a long URL, support custom aliases/domains, and basic click analytics. You have ~40 minutes. How do you proceed?

C: I’ll clarify requirements and SLOs, propose APIs and scale assumptions, outline a high-level architecture, then deep-dive on code generation, redirect hot path, caching, analytics ingestion, and multi-region. I’ll close with abuse prevention, cost, and failure modes.

I: Start with functional and non-functional requirements.

C:
- Functional
  - Create short link for a given long URL
  - Redirect: GET /{code} should 301/302 to original URL
  - Custom aliases and custom domains
  - Basic analytics: total clicks, uniques, geo/device, time series
  - Admin: disable/takedown link; URL validation/normalization
- Non-Functional
  - Redirect latency from edge: P50 < 30ms, P99 < 150ms
  - Write latency (create): P99 < 250ms including validation
  - 4–5 nines availability for redirect path (read-mostly)
  - Global edge presence; multi-region serving; DDoS-resilient
  - Strong consistency for link creation (no duplicate alias); eventual for analytics

I: What scale assumptions will you use?

C:
- Assumptions (tunable)
  - Redirects/day: 500M → ~5.8k rps avg; peak 10–20x (60–120k rps) during events
  - New links/day: 5M → ~58 rps avg; peaks few hundred rps
  - Active links: 2B total; 10–20% actively clicked monthly, heavy power-law skew (viral hot keys)
  - Custom domains: 10–20% of customers; custom aliases: 5%
- Implications
  - Hot path is GET redirect; must be fully edge-cached or one network hop to memory cache
  - Writes are modest; can afford stronger validation, anti-abuse, malware scanning async

I: Define APIs and response codes.

C:
- Public APIs (behind API Gateway + WAF)
  - POST /v1/links
    - body: { long_url, domain?, alias?, expires_at?, utm? }
    - returns: { code, short_url, created_at }
    - errors: 400 invalid, 409 alias taken, 422 blocked/malware
  - POST /v1/domains (provision custom domain; ownership verification via DNS/CNAME)
  - GET /v1/links/{code}/stats?window=1d&tz=UTC (paginated analytics)
- Redirect
  - GET https://{domain}/{code}
    - returns: 301 or 302 with Location: long_url
    - headers: Cache-Control tuned; optional anti-bot headers
- Internal
  - Code Generation Service (KGS)
  - Anti-Abuse/Trust signals
  - Analytics Ingest (Kafka) and rollup jobs

I: High-level architecture?

C:
- Edge
  - Anycast DNS + CDN; Edge workers (compute@edge) terminate TLS, parse {domain,code}
  - Edge cache: mapping from (domain, code) → long_url (+flags)
- Control Plane (writes)
  - Link Service: validate/normalize URLs, anti-abuse check, reserve code/alias, persist link
  - Domain Service: custom domain onboarding, DNS verification
  - KGS: generate unique, unguessable codes
- Data Plane (reads)
  - Redirect Service: backing origin for misses; read-only path to cache/DB
- Analytics
  - Edge events → Kafka; stream processors → real-time counters (Redis) + OLAP (ClickHouse/Druid/BigQuery)
- Storage
  - Primary link store: partitioned KV/columnar (Cassandra/DynamoDB/Spanner/Bigtable)
  - Caches: multi-layer (Edge KV, Redis/Memory near regional POPs)
  - Metadata (customers, policies, blocklists): relational store
  - OLAP for analytics; object storage for raw logs

I: Deep-dive on code generation. How do you create short codes?

C:
- Goals: high entropy, short length (5–8 chars), collision-free, resistant to enumeration/guessing, horizontally scalable
- Strategies
  - Sequential ID + Base62: shortest codes, but predictable/guessable; mitigate by shuffling spaces (permutation with secret), which complicates, and still leaks volume
  - Random Token: 64-bit random, Base62-encode (up to 11 chars). Collision probability negligible; verify on insert; allows easy horizontal scaling
  - KGS (Key Generation Service): pre-allocates pools of random codes per shard/region; hand-out is lock-free, ensuring global uniqueness and steady throughput
- Choice
  - Use KGS with cryptographically secure RNG; Base62 length 7–8 for good balance
  - Partition code space per region (prefix/salt) to avoid cross-region contention; periodic global uniqueness audits
- Custom Aliases and Domains
  - Custom alias path bypasses KGS; requires strong uniqueness constraint scoped to domain
  - Domain namespace: uniqueness is (domain, code), not just code

I: How does the read path work for redirects?

C:
- Read (GET /{code})
  1) Edge worker extracts (domain, code). Lookup Edge KV cache: key=domain:code
  2) Cache HIT: emit analytics event asynchronously; return 301/302 immediately
  3) MISS: call regional Redirect Service
     - Redis/Memory cache lookup (TTL mins/hours for hot links)
     - If hit, repopulate Edge KV with short TTL; respond
     - If miss, read from primary link store by (domain, code) partition key
       - Validate link active/not disabled/not expired
       - Warm Redis and Edge KV; emit analytics event
       - Respond 301/302 with appropriate headers
- Headers/Cache
  - Use 302 (temporary) if analytics fidelity must be exact and URL may change; 301 (moved) for stable links but beware CDN/browser caching reducing analytics
  - Set short Edge TTL for hot links with revalidation; enable stale-while-revalidate to avoid tail lat spikes
- Bot/Previews
  - For known bot UAs (slack/discord/twitterbot), optionally serve unfurled preview; respect robots and noindex

I: And the write path?

C:
- Write (POST /v1/links)
  1) Normalize long_url (scheme, punycode, strip tracking if policy requires)
  2) Anti-abuse pre-check: domain reputation, URL patterns, allow/block lists
  3) If custom alias provided: check uniqueness within domain; reject on conflict
  4) Else request a code from KGS (region-local pool)
  5) Persist record to primary store with conditional write (IF NOT EXISTS) to guarantee uniqueness:
     - key: (domain, code); values: long_url, created_at, owner_id, flags, expires_at
  6) Warm Redis and Edge KV; enqueue malware scanning and link classification asynchronously
  7) Return short_url
- Updates
  - Mutations (change destination) are limited or versioned; strong write requires conditional update on version to avoid races

I: How do you design the data model?

C:
- Link Record
  - PK: (domain, code)
  - long_url (string, up to e.g., 4KB), owner_id, created_at
  - flags: disabled, malware_suspect, nsfw, noindex
  - expires_at (nullable)
  - meta: tags, campaign info, checksum of long_url
- Secondary Indexes
  - owner_id → recent links (for listing)
  - checksum → dedupe candidates (optional)
- Caching Keys
  - cache:link:{domain}:{code} → {long_url, flags, expires_at}
  - Negative cache for non-existent codes to prevent enumeration attacks

I: Talk about analytics: what do you capture and how?

C:
- Ingest
  - On redirect, edge emits event: { ts, code, domain, ip_hash, ua, referer, country/region/city (GeoIP), device, is_bot }
  - Fire-and-forget to Kafka with local disk buffer; do not block redirect
- Processing
  - Stream processors enrich (ASN, device map), filter bots via UA+heuristics, and write:
    - Real-time counters (Redis/Timeseries DB) for dashboards (last 24–48h)
    - OLAP store for time series rollups (per link per hour/day), geo/device breakdowns
  - Retention: raw logs in object storage; rollups retained longer; PII minimized (IP hashed)
- Query
  - GET /stats reads from Redis for recent windows; falls back to OLAP for historical
- Accuracy vs Latency
  - Eventual consistency; 1–5 minutes freshness target acceptable

I: Multi-region strategy and disaster recovery?

C:
- Serving
  - Edge POPs worldwide; regionally route to nearest healthy origin if cache miss
  - Active-active across regions for reads; redirect path must survive single-region loss
- Data
  - Primary link store with multi-region replication (async or bounded-staleness)
  - KGS partitions code space per region (e.g., region prefix or salted PRNG streams)
  - Edge KV is region-local; repopulated on demand; not a source of truth
- DR
  - Backups/snapshots of link store; Kafka cross-region mirroring; OLAP replicated
  - RPO: minutes; RTO: < 1 hour for control plane; data plane should remain up via caches even during control-plane outage

I: How do you handle hot keys and cache stampedes?

C:
- Hot Links
  - Cache at edge and Redis with higher TTL and soft TTL (serve-stale + async refresh)
  - Request coalescing: single flight per key at origin; others wait or serve stale
  - Pre-warm links immediately after creation and when velocity spikes are detected
- Stampede Protection
  - Randomized TTL jitter; background refresh daemons
  - Negative caching for misses (short TTL) to prevent brute-force enumeration

I: Discuss security and abuse mitigation.

C:
- Abuse
  - Malware/phishing scanning pipeline using threat intel feeds; quarantine/disable links on hits
  - Domain reputation scoring; block newly registered or known-bad TLDs by policy
  - Rate limiting: per user/app/IP; stricter for anonymous; captchas on suspicious velocity
- Security
  - Open redirect protections: validate long_url scheme/host against policy
  - Auth: OAuth2/OIDC; service-to-service mTLS and signed requests
  - Multi-tenant isolation; custom domains verified via DNS TXT/CNAME challenge
  - PII minimization: hash IPs, rotate salts; data retention windows; compliance (GDPR/CPRA)
- Enumeration Resistance
  - Random codes; block directory listings; detect scanners via behavior and tarpitting

I: Capacity planning quick math?

C:
- Redirect QPS
  - Peak 100k rps globally; with 95% edge cache hit, origin sees ~5k rps
  - Redis cluster sized for ~5k–10k rps per region with p99 < 1ms for GET; scale horizontally
- Storage
  - 2B links × avg 200B record (code, domain, url pointer, metadata) ≈ 400 GB raw (metadata only)
  - With 3x replication and overhead, O(1–2) TB for active; long_url bodies can be compressed; actual depends on store
- Analytics
  - 500M events/day → ~5.8k eps; peak 10x; Kafka with partitioning by code/domain; OLAP daily growth based on rollups

I: Failure modes and fallbacks?

C:
- Primary store outage: serve from Redis/Edge caches; raise TTLs via feature flag; disable link edits
- Kafka outage: buffer at edge/origin; drop non-critical fields; backpressure with circuit breakers
- Bad deploy: canary + fast rollback; feature flags for KGS and cache TTLs
- Poisoned cache: version keys with config hash; explicit purge on takedown
- Region loss: fail traffic to healthy regions; caches re-warm; KGS region partitioning avoids cross-region coupling

I: What about SEO and HTTP details?

C:
- Redirect Codes
  - 301 for permanent, but may reduce analytics fidelity; 302 or 307 to keep intermediaries from caching too aggressively
- Headers
  - Cache-Control and Surrogate-Control for edge; vary per user-agent if needed
- Robots
  - Disallow crawling short links if required; avoid indexing of spam

I: Summarize key tradeoffs.

C:
- Random code + KGS provides strong security and horizontal scale at slight code length cost vs sequential Base62
- Aggressive edge caching minimizes latency/egress; analytics become eventually consistent
- Strong consistency on creation with conditional writes avoids alias collisions
- Multi-region active-active introduces bounded staleness; acceptable for redirects, not for admin edits
- Anti-abuse pipelines add write latency if synchronous; we push deep scans async with quarantine hooks

I: Looks good. Let’s wrap here.
