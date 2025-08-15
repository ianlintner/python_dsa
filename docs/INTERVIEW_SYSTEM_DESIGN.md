# System Design and Engineering Interview Guide

A practical, interview-focused guide that helps you structure answers, make tradeoffs explicit, and communicate clearly. Includes frameworks, cheat sheets, worked examples, and question banks spanning system design, microservices, load balancing, consistency, and distributed systems.

Contents:
- 1. Interview Strategy
- 2. System Design Framework
- 3. Capacity Estimation Cheat Sheet
- 4. Core Building Blocks
- 5. Microservice Design
- 6. Load Balancing
- 7. Consistency and CAP
- 8. Data Partitioning and Storage
- 9. Caching
- 10. Messaging and Streaming
- 11. Observability, Reliability, and Operations
- 12. Security Basics
- 13. Common Design Templates
- 14. Question Bank (Prompts and Follow-ups)
- 15. Glossary
- 16. References
- 17. Distributed Systems Fundamentals
- 18. Apache Kafka and Event Streaming
- 19. Kubernetes Essentials
- 20. Cloud Services Cheat Sheet (AWS, GCP, Azure)

---

## 1) Interview Strategy

- Clarify requirements
  - Functional: core features, APIs, data flows, SLAs.
  - Non-functional: scale (RPS/QPS), latency budgets (p95/p99), availability target, durability, cost constraints, data privacy/regulations.
  - Access patterns: read/write ratios, skew (hot keys), geographic distribution.
- Define constraints and scope
  - Back-of-the-envelope estimates.
  - Prioritize must-have vs nice-to-have.
- Propose a high-level design
  - Draw components: client, CDN, LB, API, services, storage, cache, queue, analytics.
  - Define data flow and control flow.
- Drill into key challenges
  - Bottlenecks; consistency vs latency; partitioning; failure modes; backpressure.
  - Alternatives with tradeoffs.
- Deep dive on one or two subsystems
  - Pick the riskiest/highest impact subsystem and go deep.
- Address operational concerns
  - Observability, rollouts, incident response, cost, security.
- Summarize tradeoffs and next steps
  - “We optimized for X at the cost of Y. If requirements change to Z, we can pivot to …”

Signals interviewers look for:
- Structured thinking, clear tradeoffs, pragmatic decisions, correct use of concepts, realistic estimations, and strong communication.

---

## 2) System Design Framework

- APIs and Contracts
  - Public APIs (HTTP/gRPC), input validation, idempotency keys, pagination, error semantics.
- Data Modeling
  - Entities, relationships, indexes, normalization vs denormalization, schema evolution.
- Storage
  - SQL vs NoSQL; consistency needs; OLTP vs OLAP; hot/cold tiers; durability needs.
- Compute
  - Stateless vs stateful services; synchronous vs asynchronous; CPU vs I/O bound.
- Caching
  - Where: client, CDN, edge, service, DB.
  - What: objects, query results, computed views.
  - How: TTL, invalidation strategies, write policies.
- Partitioning and Replication
  - Hash-based, range-based, geo-sharding; replication factors and placement.
- Consistency Model
  - Strong vs eventual; session/RYW; quorum math; isolation levels.
- Load Balancing and Routing
  - L4 vs L7; algorithms; sticky sessions; circuit breaking; retries and timeouts.
- Messaging
  - Queues vs streams; at-least-once vs exactly-once patterns; outbox/inbox.
- Reliability and SLOs
  - Error budgets, backpressure, autoscaling, degradation strategies.
- Observability
  - Metrics, logs, traces, SLO dashboards, alerting.
- Security and Privacy
  - AuthN/Z, mTLS, token scopes, PII handling, encryption at rest/in transit.
- Deployment and Operations
  - Blue/green, canary, feature flags, rollbacks, disaster recovery (RPO/RTO).

---

## 3) Capacity Estimation Cheat Sheet

Common conversions:
- 1 KB ≈ 10^3 bytes; 1 MB ≈ 10^6; 1 GB ≈ 10^9; 1 TB ≈ 10^12
- 1 day ≈ 86,400 seconds

Back-of-the-envelope steps:
- Requests per second (RPS) = daily active users × requests per user per day ÷ 86,400
- Data rate = event size × events per second
- Storage per day = data rate × 86,400
- Network egress cost often dominates at scale; be mindful.

Latency budget example (p95 target 200 ms end-to-end):
- CDN/cache: 5-20 ms
- LB + TLS: 5-10 ms
- App logic: 20-50 ms
- DB read: 2-10 ms (cache hit) or 10-50 ms (miss)
- Cross-region adds 50-150 ms

---

## 4) Core Building Blocks

- CDN
  - Offload static content; edge caching; signed URLs; cache-control headers.
- API Gateway
  - Routing, auth, rate limiting, request/response transformations.
- Service Mesh
  - mTLS, retries, timeouts, circuit breaking, observability sidecars.
- Databases
  - SQL (Postgres/MySQL): transactions, joins, strong consistency.
  - NoSQL (Cassandra/DynamoDB): horizontal scale, tunable consistency.
  - Search (Elasticsearch/OpenSearch), Analytics (ClickHouse, BigQuery).
- Object Storage
  - Durable blob storage (S3/GCS); lifecycle policies; CDN fronting.
- Caches
  - Redis/Memcached; eviction policies; distributed locks carefully.
- Queues/Streams
  - SQS/RabbitMQ (queues), Kafka/Pulsar (streams); ordering, partitioning.
- Compute
  - Containers/K8s; autoscaling; serverless for bursty workloads.

---

## 5) Microservice Design

- Service boundaries
  - Domain-driven design (DDD) bounded contexts; avoid chatty RPC between services.
- Contracts and versioning
  - Backward-compatible schemas; consumer-driven contracts; API versioning.
- Data ownership
  - Each service owns its data; avoid shared DB across many services.
- Communication patterns
  - Sync: gRPC/HTTP; Async: events/queues for decoupling and resilience.
- Distributed transactions
  - Avoid 2PC across services; use Saga pattern (choreography or orchestration).
- Resilience
  - Retries with jittered backoff; timeouts; circuit breakers; idempotency.
- Service discovery
  - DNS, Consul, Kubernetes services; health checks; TTLs.
- API Gateway/BFF
  - Backend-for-Frontend to tailor APIs per client; aggregate calls; caching.
- Observability
  - Trace context propagation; RED/USE metrics; structured logging; exemplars.
- Deployment
  - Independent deployability; canary releases; feature flags; schema evolution.

Tradeoffs:
- Microservices improve team autonomy and scale-out but increase complexity, operational overhead, and consistency challenges. Start simple, split only when justified.

---

## 6) Load Balancing

- Layers
  - L4 (TCP/UDP) vs L7 (HTTP/gRPC) load balancing.
- Algorithms
  - Round robin, weighted round robin, least connections, least response time, power of two choices, consistent hashing (sticky to partitions).
- Health checking
  - Active (probes) and passive (error rate-based); outlier detection.
- Session affinity
  - Cookie-based or IP-based; minimize stateful affinity by making services stateless.
- Global load balancing
  - GeoDNS, anycast, GSLB; route to nearest healthy region; failover plans.
- TLS termination
  - At edge or at service; offload vs end-to-end encryption.
- Retry and timeout policies
  - Prevent retry storms; use hedged requests sparingly; enforce budgets.
- Rate limiting
  - Token bucket/leaky bucket; per-client/per-route; global vs local counters.

---

## 7) Consistency and CAP

- CAP theorem
  - Under partition, choose between availability and consistency. Most internet-scale systems are AP with tunable consistency.
- Consistency models
  - Strong (linearizable), sequential, causal, eventual, read-your-writes, monotonic reads/writes.
- Quorums (for N replicas)
  - Read quorum R + write quorum W > N to achieve strong consistency for reads.
  - Example: N=3, W=2, R=2 gives R+W=4>3.
- Isolation levels (DB)
  - Read uncommitted, read committed, repeatable read, serializable.
- Conflict resolution
  - Last write wins (with caveats), vector clocks, CRDTs, app-specific merges.
- Idempotency
  - Use idempotency keys; put operations behind unique request IDs.

---

## 8) Data Partitioning and Storage

- Partitioning strategies
  - Hash-based (uniform, hard to range scan), range-based (good for range scans, hot ranges risk), directory/lookup (flexible, metadata overhead).
- Hot keys and skew
  - Mitigate with time-bucketed keys, random suffixes, or consistent hashing with virtual nodes.
- Replication
  - Synchronous (lower RPO, higher latency) vs asynchronous (higher RPO risk).
  - Leader-follower vs leaderless (Dynamo-style).
- Secondary indexes
  - Local vs global secondary indexes; write amplification; consistency implications.
- Schema evolution
  - Backward-compatible changes; dual writes/migrations; online backfills.

---

## 9) Caching

- Layers
  - Client cache, CDN/edge, service-level cache (Redis), DB cache (buffer pool).
- Patterns
  - Read-through, write-through, write-back, cache-aside.
- Invalidation
  - TTLs, explicit invalidation on writes, versioned keys.
- Pitfalls
  - Thundering herd: add jitter, request coalescing, locks, stale-while-revalidate.
  - Inconsistent cache + DB: accept eventual consistency or enforce write-through.
- Key design
  - Namespacing, include version/schema hash; avoid unbounded cardinality.

---

## 10) Messaging and Streaming

- Queues vs streams
  - Queues: competing consumers, at-least-once, work distribution.
  - Streams: ordered partitions, replays, multiple consumer groups, event sourcing.
- Delivery semantics
  - At-most-once, at-least-once (most common), effectively-exactly-once (with idempotency and transactional outbox).
- Outbox pattern
  - Write data and outbox in same transaction; relay to stream asynchronously.
- Backpressure
  - Consumer lag, dynamic concurrency, dead-letter queues; circuit breaking upstream.

---

## 11) Observability, Reliability, and Operations

- SLI/SLO/Error budgets
  - Define latency, availability, throughput. Track p50/p95/p99, saturation.
- Metrics
  - RED (Rate, Errors, Duration), USE (Utilization, Saturation, Errors).
- Tracing
  - Propagate context; sample smartly; link to logs; analyze critical paths.
- Logging
  - Structured JSON; correlation IDs; PII scrubbing; retention policies.
- Resilience patterns
  - Timeouts, retries with jitter, circuit breakers, bulkheads, load shedding.
- Rollouts
  - Blue/green, canary, feature flags, progressive delivery; rollback plans.
- DR and backups
  - RPO/RTO objectives; multi-AZ/region; backup verification; chaos testing.

---

## 12) Security Basics

- AuthN/AuthZ
  - OAuth2/OIDC, JWT, short-lived tokens, scopes; ABAC/RBAC.
- Transport security
  - TLS everywhere, mTLS between services; cert rotation.
- Data security
  - Encryption at rest (KMS); key rotation; field-level encryption for PII.
- Secrets management
  - Vault/KMS/SM; never bake secrets into images.
- Threat modeling
  - OWASP Top 10; input validation; WAF; rate limiting; audit logging.

---

## 13) Common Design Templates

Each template lists: API, data model, architecture, scale, and key challenges.

A) URL Shortener
- API
  - POST /shorten {long_url} -> {short_code}
  - GET /{short_code} -> 301 redirect to long_url
- Data model
  - short_code (PK), long_url, created_at, owner_id, ttl (optional), visit_count
- Architecture
  - CDN + edge cache for GET
  - API service (stateless)
  - DB: KV or SQL with unique index on short_code
  - Cache: short_code -> long_url
  - ID generation: base62 from sequence or hash(long_url)
- Scale
  - Heavy read, moderate write
  - Pre-warm hot codes; Bloom filter to reduce DB misses
- Challenges
  - Custom aliases collisions; abuse detection; TTL/purge; analytics separate

B) News Feed (Fan-out)
- API
  - POST /post; GET /feed?user_id
- Data model
  - posts, user_follows, user_feed (denormalized)
- Architecture
  - Write path: enqueue fan-out to followers’ feeds (asynchronous)
  - Read path: merge user_feed + recency + personalization
  - Storage: posts in object store + metadata in DB; user_feed in KV
  - Cache: user_feed pages
- Scale
  - Hot users with millions of followers: partial fan-out, on-read merge
- Challenges
  - Ordering, dedupe, pagination, privacy, spam

C) Chat/Messaging
- API
  - WebSocket for realtime; REST for history
- Data model
  - conversations, messages (conversation_id, sender_id, seq_no, timestamp)
- Architecture
  - Gateway (sticky by conversation), message broker, storage (append-only)
  - Presence service; delivery receipts; typing indicators (ephemeral)
- Scale
  - Partition by conversation_id; global ordering per conversation only
- Challenges
  - Mobile offline, end-to-end encryption (optional), spam, abuse

D) Rate Limiter
- Algorithms
  - Token bucket/leaky bucket, fixed/sliding window
- Architecture
  - Local limiter in gateway + global counter in Redis; Lua for atomic ops
  - Consistent hashing of keys; approximate counters for large scale
- Challenges
  - Cluster-wide sync vs eventual; fairness; burst handling

E) File Storage Service
- API
  - POST /upload; GET /download; signed URLs; multipart
- Architecture
  - CDN + object storage; metadata DB; background virus scan
  - Deduplication via content hash; lifecycle to cold storage
- Challenges
  - Large files, resumable uploads, encryption, egress costs

F) Notifications (Email/SMS/Push)
- Architecture
  - Producer -> queue -> worker pools -> provider fan-out with retries
  - Idempotency per user+template+dedupe window
- Challenges
  - Provider failures, deliverability, rate limits, opt-outs, compliance

---

## 14) Question Bank

System Design Prompts:
- Design a URL shortener for 1B URLs and 1M RPS reads.
- Design Twitter timeline with hot celebrities and 50M DAU.
- Design WhatsApp-like chat with end-to-end encryption and 100M MAU.
- Design a globally available file sharing service with 99.99% availability.
- Design a realtime ride-hailing dispatch system with surge pricing.
- Design a globally distributed configuration service with low-latency reads.

Microservices:
- When to split a monolith; identify service boundaries.
- How to implement Saga for order -> payment -> inventory -> shipping.
- Design API gateway + service mesh architecture.
- Versioning strategy for breaking API changes.

Load Balancing:
- Choose between least-connections vs power-of-two choices.
- Global LB across three regions; failover plan under partition.
- Sticky sessions vs stateless services; when and how.

Consistency:
- Choose consistency model for cart checkout; read-your-writes requirements.
- Quorum configuration for N=5 replicas targeting high availability.
- Handling conflicting updates with CRDTs vs LWW vs app-level merges.

Data:
- Partitioning strategy for time-series metrics with hot tenants.
- Designing global secondary indexes with write-heavy workload.
- Schema evolution with rolling deployments and online backfills.

Caching:
- Prevent thundering herd under cache miss for hot keys.
- Cache invalidation strategies for profile updates.
- Layered caching for product catalog and pricing.

Messaging:
- Exactly-once pipeline design; outbox pattern; deduplication.
- Choosing Kafka vs RabbitMQ; consumer lag management; dead-letter queues.

Observability/Operations:
- Define SLOs for an API; error budget policy.
- Incident response flow for a cascading failure.
- Safe rollout plan for a high-risk change.

Follow-up Probes:
- Failure modes and mitigation.
- Tradeoffs if requirement X changes.
- Cost awareness and optimizations.
- Testing strategies (property tests, chaos experiments).

---

## 15) Glossary

- CAP: Consistency, Availability, Partition tolerance.
- RPO/RTO: Recovery Point/Time Objective.
- Quorum: Minimum number of replicas participating to accept an operation.
- SLO/SLI/SLA: Objective/Indicator/Agreement for reliability.
- Saga: Sequence of local transactions with compensations across services.
- Idempotency: Replaying an operation yields same effect.
- Backpressure: Mechanism to slow producers when consumers lag.
- Hedged requests: Duplicate requests to reduce tail latency (use sparingly).

---

## 16) References

- Designing Data-Intensive Applications (Kleppmann)
- Site Reliability Engineering (Google SRE)
- The Art of Scalability (Abbott, Fisher)
- Papers: Dynamo, Spanner, Raft
- Production Ready Microservices (Newman)
- Architecture blogs: AWS Builders, Google Cloud, ACM Queue

---

Usage in interviews:
- Start with the framework (Section 2), do quick estimates (Section 3), assemble blocks (Section 4), and go deep on the hardest parts (Sections 5–12). Use templates (Section 13) to accelerate common designs and the question bank (Section 14) to practice.

---

## 17) Distributed Systems Fundamentals

Key concepts:
- Failure models: process crash, network partitions, slow nodes (the common case), split brain, correlated failures (AZ outage).
- Time and clocks:
  - Wall vs monotonic clocks; NTP drift; don’t rely on exact time ordering across nodes.
  - Logical clocks: Lamport clocks (causal ordering), vector clocks (conflict detection).
- Consensus and membership:
  - Raft/Paxos for leader election and log replication; Single-writer (leader) simplifies invariants.
  - Failure detectors, heartbeats, quorum-based membership, gossip protocols.
- Quorums and replication:
  - For N replicas, choose R/W such that R + W > N for read-write strong reads.
  - Anti-entropy, hinted handoff, read repair for AP systems.
- Idempotency and exactly-once:
  - Exactly-once delivery is a system-level illusion; implement idempotent handlers with request IDs/outbox/inbox.
- Backpressure and flow control:
  - Bounded queues, shedding load, circuit breakers; push back to callers with retry-after.
- Data movement:
  - Rebalancing on scale-out/in; consistent hashing with virtual nodes; directory/lookup services.
- Testing and resilience:
  - Chaos experiments, fault injection; steady-state SLO verification.

Interview prompts:
- Explain why wall-clock timestamps can’t ensure total order. How do you detect/resolve conflicts?
- When to choose leader-based vs leaderless replication?
- Design a membership service with gossip and failure suspicion.

---

## 18) Apache Kafka and Event Streaming

Core model:
- Topics split into partitions; ordering is guaranteed within a partition.
- Producers choose partitions (by key hashing or custom strategy).
- Consumer groups: each partition assigned to one consumer per group; parallelism = partitions.
- Offsets: consumers control position; commits are how you checkpoint.

Storage/retention:
- Append-only log; retention by time/size; log compaction keeps latest record per key (good for changelog tables).
- Tiered storage (in some distributions/clouds) extends retention at lower cost.

Delivery semantics:
- At-least-once by default: handle duplicates via idempotent consumers or dedupe tables.
- Idempotent producer + transactions enable effectively exactly-once (EOS) with careful design.
- Producer configs: enable.idempotence=true, acks=all, appropriate retries/backoff.

Schema and evolution:
- Use a schema registry (Avro/Protobuf/JSON-Schema); enforce compatibility (backward/forward/full).
- Version events; avoid breaking changes; prefer additive evolution.

Partitioning and keys:
- Choose keys to balance load and preserve locality (e.g., user_id).
- Hot keys: add random suffixes or bucketization; handle skew.

Rebalancing and availability:
- Rebalance triggers on membership change; tune session/heartbeat timeouts; cooperative rebalancing to minimize disruption.
- Replication factor ≥ 3; min.insync.replicas ≥ 2 for durability under broker failure.

Multi-region and DR:
- Disaster recovery via MirrorMaker 2 / cluster linking; accept RPO > 0 unless synchronous stretch (high latency).
- Geo-local consumers to reduce egress; consider per-region topics + async replication.

Ecosystem:
- Kafka Connect for source/sink connectors; Single Message Transforms.
- Stream processing: Kafka Streams, ksqlDB, Apache Flink/Spark Structured Streaming.
- Observability: lag metrics per consumer group/partition; broker health, ISR, request latency.

Interview pitfalls:
- “Exactly-once” claims without idempotency or transactions.
- Mis-sized partitions (too few limits parallelism; too many wastes resources).
- Using time-based ordering across partitions instead of per-key ordering.

---

## 19) Kubernetes Essentials

Core resources:
- Pod (smallest unit), Deployment (stateless), StatefulSet (stable identity/storage), DaemonSet (per-node).
- Service (ClusterIP/NodePort/LoadBalancer/Headless), Ingress/Ingress Controller for L7 routing.
- ConfigMap/Secret for config; RBAC for authZ; ServiceAccount for identity.

Reliability and scaling:
- Probes: liveness, readiness, startup. Use readiness to gate traffic; liveness for self-heal.
- HPA (CPU/memory/custom metrics); PDB to protect against voluntary disruptions.
- Requests/limits to get proper QoS; avoid CPU throttling and OOMKills.
- Node autoscaling (cluster autoscaler); prioritize via PriorityClass and preemption.

Networking and security:
- CNI provides pod networking; NetworkPolicies for east-west controls; mTLS via service mesh (Istio/Linkerd).
- PodSecurity admission; image scanning; secrets mounted via CSI/KMS.

Stateful workloads (e.g., Kafka/ZooKeeper):
- Use StatefulSets with PersistentVolumeClaims; set PodDisruptionBudgets and ordered updates.
- Headless Service for stable DNS; rack/zone awareness via topology spread constraints.

Rollouts and ops:
- RollingUpdate, Blue/Green, Canary (Argo Rollouts/Flagger); set maxSurge/maxUnavailable.
- Troubleshooting: kubectl describe/get/logs/exec; common issues: CrashLoopBackOff, ImagePullBackOff, OOMKilled, Evicted.
- Observability: metrics-server, Prometheus/Grafana, OpenTelemetry, events; set SLOs per service.

Interview prompts:
- Design a multi-tenant K8s platform with resource isolation and network policies.
- Deploy Kafka on K8s safely—what would you configure for storage, disruption, and upgrades?

---

## 20) Cloud Services Cheat Sheet (AWS, GCP, Azure)

Compute and orchestration:
- Containers: AWS EKS, GCP GKE, Azure AKS.
- Serverless: AWS Lambda, GCP Cloud Functions/Cloud Run, Azure Functions/Container Apps.
- Batch/queues: AWS ECS/Fargate, GCP Cloud Run Jobs, Azure Container Instances.

Storage:
- Object: AWS S3, GCP Cloud Storage (GCS), Azure Blob Storage.
- Block: AWS EBS, GCP Persistent Disk, Azure Managed Disks.
- Files: AWS EFS/FSx, GCP Filestore, Azure Files.

Databases:
- Relational: AWS RDS/Aurora, GCP Cloud SQL/AlloyDB, Azure SQL Database.
- NoSQL KV/Wide-column: AWS DynamoDB/Keyspaces, GCP Bigtable/Firestore, Azure Cosmos DB (multiple APIs).
- Search/Analytics: AWS OpenSearch/Redshift, GCP BigQuery/Dataproc, Azure Synapse/Data Explorer.

Messaging/streaming:
- Kafka: AWS MSK/Confluent Cloud, GCP Confluent Cloud, Azure Event Hubs for Kafka API.
- Native: AWS Kinesis + SQS/SNS, GCP Pub/Sub, Azure Service Bus/Event Hubs.

Networking and delivery:
- LB/Proxy: AWS ALB/NLB, GCP External/Internal LBs, Azure Application Gateway/Front Door.
- CDN: AWS CloudFront, GCP Cloud CDN, Azure CDN.
- DNS: Route 53, Cloud DNS, Azure DNS.
- VPC/VNet, PrivateLink/Private Service Connect/Private Link Service for private connectivity.

Security and identity:
- IAM: AWS IAM, GCP IAM, Azure RBAC.
- Secrets/KMS: AWS Secrets Manager + KMS, GCP Secret Manager + KMS, Azure Key Vault.
- mTLS/service identity: SPIRE, mesh integrations.

Observability:
- AWS CloudWatch/X-Ray, GCP Cloud Monitoring/Trace/Logging, Azure Monitor/App Insights.
- Managed OpenTelemetry collectors available across clouds.

Data governance and DR:
- Cross-region replication (S3/Cloud Storage/Blob); multi-region DB options (DynamoDB Global Tables, Spanner, Cosmos DB).
- RTO/RPO planning; backups and point-in-time recovery.

Cost and egress:
- Data egress charges between regions/clouds can dominate; colocate consumers with producers; use CDNs to reduce origin egress.
- Pick managed services where possible to reduce ops toil; compare SLAs.

Interview prompts:
- Design a multi-region read-local/write-global service on AWS—how do you use DynamoDB Global Tables and Route 53?
