Title: Staff-level System Design Interview Script — Design WhatsApp (Messaging) Clone

Format: Full conversation transcript between Interviewer (I) and Candidate (C). Focus on end-to-end encrypted messaging, delivery semantics, fanout, presence, groups, media, multi-device, abuse, and multi-region reliability.

I: Design a WhatsApp-like messaging system. Core: 1:1 and group messaging, delivery/read receipts, presence (online/typing), media, and end-to-end encryption (E2EE). Assume mobile-first with push notifications. You have ~45 minutes. How will you proceed?

C: I’ll clarify scope and SLOs, set scale assumptions, propose APIs and high-level architecture, then deep-dive on message delivery semantics, E2EE keys, group fanout, presence, push notifications, multi-device sync, storage/retention, and multi-region. I’ll end with capacity, failure modes, and abuse.

I: Start with requirements and non-goals.

C:
- Functional
  - Register/login; device linking
  - 1:1 messages (text, media, attachments)
  - Group chats (size up to K, e.g., 512–1024 members)
  - Delivery receipts (sent/server-acked, delivered to device, read)
  - Presence (online/last-seen), typing indicators
  - Push notifications (APNs/FCM)
  - Message search: on-device; server can’t read content (E2EE)
- Non-Functional
  - End-to-end encrypted payloads (server can’t decrypt)
  - Low latency: send→server-ack P99 < 150–200ms; intra-region delivery P99 < 500ms
  - High availability for delivery; tolerate intermittent mobile connectivity
  - Multi-region; mobile network variability; offline store-and-forward
- Non-goals (for this round)
  - Payments, status stories, calls/video, heavy server-side search on content

I: Give scale assumptions to justify design choices.

C:
- Assumptions (tunable)
  - DAU 1B; messages/day 100B → ~1.16M msg/sec avg, peaks 10–20x during events
  - Media messages: 30–40% with object store backing
  - Avg devices per user: 1.3–1.7 (linked devices); multi-device enabled
  - Group distribution: many small groups, some large broadcast-esque; heavy fanout skews
- Implications
  - At-least-once delivery with deduplication; idempotent queues
  - Per-device queues (not just per-user) to support multi-device and push notifications
  - E2EE adds client crypto cost; server handles metadata routing only

I: Define APIs and success criteria.

C:
- Public APIs (behind API Gateway + Auth + Rate limit)
  - POST /v1/messages
    - body: { chat_id, from_device_id, msg_id, ciphertext, headers{ device_pk, salt, sender_key_id? }, media_manifest? }
    - returns: { server_ts, ack_id } on durable enqueue
  - GET /v1/queue/poll?device_id=...&cursor=...
    - returns: encrypted envelopes destined for device; long-poll/websocket
  - POST /v1/receipts { chat_id, msg_id, type: sent|delivered|read }
  - POST /v1/groups { name, members[] }, POST /v1/groups/{id}/members (add/remove)
  - POST /v1/devices/link, DELETE /v1/devices/{id}
- Internal
  - Key Management Service (KMS): device key registration, sender keys for groups (server stores only encrypted public keys or metadata; no plaintext content)
  - Media Upload Service: get signed upload URLs; server stores encrypted blobs (client-side encrypted)
  - Presence Service: publish/subscribe ephemeral statuses; typing
- Success Criteria/SLOs
  - P99 send→server-ack < 200ms; delivery to online recipient P99 < 500ms within a region
  - Delivery durability across disconnects with retries and exponential backoff

I: High-level architecture?

C:
- Edge
  - Anycast + API Gateway (Auth, DoS protections, rate limiter), WebSocket gateway for long-lived connections
- Services (stateless autoscaled)
  - Messaging Ingress: authenticate, validate, assign routing, enqueue to per-chat/per-device queues
  - Fanout Router: resolves chat membership → per-device fanout; generates device-specific envelopes (E2EE aware)
  - Delivery Service: manages device connections, long-poll/WebSocket, push notifications; pulls from per-device queues
  - Receipt Service: processes client receipts, updates delivery/read states
  - Group Service: membership, roles, group metadata; sender key distribution (encrypted)
  - Presence Service: ephemeral presence/typing via pub/sub; no durable history
  - Media Service: signed URLs; store encrypted object; CDN delivery
  - Device/Identity Service: users, devices, key registration (public keys only)
- Async/Streaming
  - Kafka/PubSub: message events, receipts, metrics, abuse signals
- Storage
  - Queue Store: per-device durable queues (Cassandra/DynamoDB/Bigtable with time-ordered keys or Redis streams for hot tail + durable backing)
  - Chat Metadata Store: users, chats, membership (RDBMS or KV)
  - Receipt State Store: per-message state map (compact)
  - Media: object store (S3/GCS) with client-side encryption
- Observability
  - Tracing with correlation by msg_id; metrics on enqueue/dequeue latency; DLQs for poison messages

I: Deep-dive message delivery semantics. What guarantees?

C:
- Semantics
  - At-least-once delivery to each device; deduplication on client via msg_id + per-chat monotonic counters
  - Ordering: within a chat per-sender monotonic increasing sequence; best-effort merge ordering across multiple senders; clients reorder by (sender_seq, timestamp), tolerant of minor skew
  - Idempotency: server enforces idempotent enqueue on (chat_id, msg_id); duplicate submits are no-ops
- Flow
  1) Client generates msg_id and per-sender sequence number, encrypts payload (E2EE)
  2) POST /messages → Ingress validates rate limits, persists to Chat Log (optional) and enqueues “routing task”
  3) Fanout Router determines recipient devices and enqueues per-device envelopes into Device Queues
  4) Delivery Service:
     - If device online (WebSocket), push immediately
     - Else schedule push notification via APNs/FCM and keep in durable queue
  5) Recipients ACK receipt; client sends delivered/read receipts; server updates state and fanouts receipts
- Receipts
  - sent: server-ack on durable enqueue
  - delivered: recipient device confirms receipt; updates sender UI per-device
  - read: user opened message; fanout read receipts to chat (subject to privacy settings)

I: How do you implement E2EE, including groups?

C:
- 1:1 E2EE
  - Each device has identity key pair (long-lived) + signed prekeys; use Double Ratchet (Signal protocol) for per-conversation sessions
  - Server stores only public keys and prekeys; never sees plaintext
  - On first message or missing session, sender fetches recipient device prekeys, establishes session, then sends ciphertext envelopes per device
- Groups E2EE
  - Sender Keys (Signal group model): per-group symmetric “sender key” distributed to members’ devices, encrypted with each device’s public key; reduces O(N) per-message crypto
  - On membership change (join/leave), rotate sender keys; server distributes new encrypted sender key envelopes to current members
  - For large groups, optimize with lazy rekey or sub-grouping; ensure forward secrecy/backward secrecy guarantees
- Multi-device
  - Each device has its own session; sender produces per-device envelopes or uses sender-key plus per-device envelope headers
- Server Role
  - Blind relay: validates metadata but cannot decrypt; rejects malformed envelopes via signature checks on headers

I: Fanout strategy and queues?

C:
- Fanout
  - For 1:1: 1→D fanout where D is number of recipient devices
  - For groups: 1→(Σ devices of members). Use sender-keys to reduce compute on clients; server still pushes per-device envelope
- Queues
  - Per-device logical queue with partitions/shards by device_id; append-only with time-based keys
  - Backpressure: slow consumer detection; cap per-device queue length (e.g., last N messages or time window) with policy (drop oldest or block sender for that recipient on severe backlog)
  - Dequeue protocol: at-most-batch deliver; client ACK with checkpoint cursor; server GC acknowledged items with safety window

I: Presence and typing indicators?

C:
- Presence
  - Ephemeral in-memory state replicated across presence nodes; publish/subscribe channels per user
  - Client heartbeats on WebSocket; mobile background uses push “wake” + short poll
  - Last seen computed from disconnect events; privacy options (hide last seen)
- Typing
  - Short-lived pub/sub events scoped to chat; TTL a few seconds; never stored durably

I: Media handling with E2EE?

C:
- Media
  - Client generates symmetric media key, encrypts media locally; uploads encrypted blob to object store via signed URL
  - Message envelope contains media manifest (URL, size, MAC, encryption info) encrypted end-to-end
  - CDN serves encrypted blobs; clients download and decrypt with shared key
- Thumbnails/previews also encrypted; optionally included inline

I: Multi-device synchronization details?

C:
- Model
  - Each device is first-class; per-device queues ensure independent reliable delivery
  - Sync
    - Sender sends to all linked devices of recipient and to all of sender’s devices (for outbox consistency)
    - Devices use per-chat “clock” (vector or lamport-like with per-sender counters) to reconcile/order
  - History sync for newly linked device:
    - Sender (or another authorized device) shares recent history via encrypted transfer (out-of-band) or via server-stored encrypted backups (if user opted-in, zero-knowledge encryption)
  - Conflict handling
    - Edits/deletes (if supported) propagate as new events referencing msg_id; last-writer-wins per event type with timestamps

I: How do you run in multiple regions?

C:
- Strategy
  - Edge-local ingress; route to “home region” for chat/device metadata to ensure consistent membership; or use globally consistent metadata store (with performance tradeoffs)
  - Message queues are region-local to the home region of recipient device; cross-region replication only for failover
- Replication
  - Async replication of device queues to warm standby in paired region; RPO minutes
  - Presence is region-local; not replicated (ephemeral)
- Failover
  - If home region down: flip routing to standby; deliver from replicated queues; accept that some read receipts and presence drop temporarily; eventual reconciliation on recovery
- IDs
  - Snowflake-like IDs embed region/shard/time for ordering and routing

I: Capacity planning rough math?

C:
- Messaging
  - 100B/day → ~1.16M/sec avg; peak ~10–20M/sec
  - Fanout multiplier: average devices per user ~1.5; for groups average member devices could be ~50–200; cache group memberships aggressively
- Storage
  - If server stores only encrypted envelopes + metadata for 30 days: assume 100 bytes metadata + 300 bytes envelope avg → ~40 KB per 100 messages; at 100B/day → ~4 PB/day raw; must limit retention aggressively (e.g., 1–7 days) and rely on client storage; deduplicate media via manifests
  - Use tiered storage: hot queues in fast KV, older in cheaper blob as segments with compaction
- Throughput
  - Delivery Service must sustain 100k–500k concurrent WebSocket connections per node (OS tuning) with backpressure and message batching

I: Failure modes and mitigations?

C:
- Mobile connectivity flaps: exponential backoff, resume cursors on reconnect, outbox retries with idempotency keys
- Queue backlog/slow consumer: alerting, per-device throttles, sender warnings; optional back-pressure to senders for extreme cases
- Push provider failure (APNs/FCM): retry with exponential backoff; alternative wake strategies; degrade to pull-only
- Region outage: fail to standby; serve with degraded presence; reconcile receipts later
- Clock skew: rely on monotonic counters in chat; wall-clock only for UX
- Poison envelope: DLQ with inspection; block offending device; rotate keys as needed
- Hot groups: shard fanout workers; rate-limit sender; coalesce typing/presence events

I: Abuse and trust in an E2EE system?

C:
- Challenges
  - No server-side content scanning; rely on metadata, behavioral signals, and user reports
- Mitigations
  - Rate limits: per user/device/IP/app version; graduated friction (captcha, send limits)
  - Graph-velocity heuristics: new accounts sending to many recipients quickly → throttle
  - Client-side hash signaling (optional user-consented safety): perceptual hashes for known CSAM (with extreme care for privacy)
  - Report/Block workflows: upon report, allow voluntary client-side reupload of offending ciphertext with device-kept keys or server stores a hold for law-enforcement requests where applicable; strong legal/compliance framework
  - Spam detection via delivery failure rates, reply ratios, burst patterns
- Privacy
  - Minimize logs; IPs hashed/rotated; strict retention; transparency reports

I: Data model sketch?

C:
- User: { user_id, profile_meta, settings }
- Device: { device_id, user_id, device_pubkeys, capabilities, last_seen }
- Chat: { chat_id, type: 1:1|group, members[], roles[], sender_key_state }
- Message (server-visible metadata only):
  - { chat_id, msg_id, from_device_id, server_ts, routing_flags, envelope_ref (encrypted payload pointer), ttl, expiration }
- DeviceQueue:
  - Key: (device_id, bucket_ts, offset), Value: { msg_id, chat_id, envelope_ref, deliver_by, flags }
- Receipt:
  - { chat_id, msg_id, device_id, state: sent|delivered|read, ts }
- Presence:
  - In-memory maps { user_id → status }, replicated within region

I: Push notifications path?

C:
- When new message enqueued and device offline:
  - Delivery Service submits push via APNs/FCM: token per device; payload contains only minimal metadata (no content), optionally “new message in chat”
  - On app open or push-tap, client connects and pulls from queue

I: Summarize tradeoffs you made.

C:
- At-least-once + dedupe provides reliability with simpler server guarantees; ordering managed at client per-chat
- Per-device queues handle multi-device cleanly; increased fanout/storage but clear semantics
- E2EE via Signal/Double Ratchet and sender keys preserves privacy; server blind relay constrains server-side features like content search
- Region-local home for metadata reduces coordination latency; async replication accepts bounded staleness during failover
- Aggressive retention limits server storage; clients own history; optional user-consented encrypted backup covers restores

I: Solid. Let’s stop here.
