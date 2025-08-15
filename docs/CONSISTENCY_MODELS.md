# Consistency Models: Deep Dive for Interviews

A practical reference to reason about data correctness, latency, and availability across distributed systems and databases. Use this to structure tradeoffs and avoid common pitfalls.

Contents:
- 1. Why Consistency Matters
- 2. CAP and PACELC
- 3. Consistency Models (with examples)
- 4. Replication, Quorums, and Tunable Consistency
- 5. Database Isolation Levels (OLTP)
- 6. Conflict Detection and Resolution
- 7. Idempotency, Fencing, and Exactly-Once Illusion
- 8. Eventual Consistency Design Patterns
- 9. Global Consistency (TrueTime, Global Clocks)
- 10. Testing and Validation
- 11. Interview Playbook
- 12. Sample Questions

---

## 1) Why Consistency Matters

- Correctness: Users expect up-to-date views (read-your-writes) and durable outcomes (no double charges).
- Latency/Availability: Stronger guarantees often cost more latency and reduce availability under partitions.
- Cost and Complexity: Relaxed models can scale better but push complexity into application logic (retries, reconciliation).

---

## 2) CAP and PACELC

- CAP theorem: Under a partition (P), choose consistency (C) or availability (A).
  - CP systems prefer consistent responses or errors/unavailability during partitions.
  - AP systems prefer serving responses even if not the latest.
- PACELC (extended):
  - If Partition (P), choose A or C; Else (E) when normal operation, choose Latency (L) or Consistency (C).
  - Many systems choose AP/EL (availability under partition, low latency otherwise).

---

## 3) Consistency Models (with examples)

- Linearizability (strong consistency)
  - Each operation appears to take effect atomically at a single point in time.
  - If write(X=1) completes before read(X), read must see 1 globally.
  - Example: Single-leader DB with synchronous replication and quorum reads.
- Serializability (transactional)
  - Transactions appear as if executed in some serial order (not necessarily real-time order).
  - Stronger than linearizable single operations; applies to multi-op transactions.
- Sequential consistency
  - All operations appear in the same order across processes, respecting per-process order; not tied to real time.
- Causal consistency
  - If A happens-before B, everyone agrees on A before B; concurrent ops may be seen in different orders.
  - Practical for social feeds, collaborative apps.
- Read-your-writes (RYW)
  - A client sees its own writes subsequently; can be provided via session stickiness.
- Monotonic reads/writes
  - Reads: once you see a value, you don’t see older values later.
  - Writes: a client’s writes are serialized in order.
- Eventual consistency
  - In absence of new writes, replicas converge; no guarantee on staleness windows.

Notes:
- Linearizability ≠ Serializability: linearizability is per operation; serializability is per transaction schedule.
- Client-centric consistency (RYW, monotonic) can be layered over eventual stores with sessions.

---

## 4) Replication, Quorums, and Tunable Consistency

- Replication factor N (number of replicas for a partition).
- Quorum rules:
  - Write quorum W, read quorum R; to get linearizable reads: R + W > N, and W > N/2.
  - Example: N=3 → typical W=2, R=2 (R+W=4>3).
- Leader-based vs leaderless:
  - Leader-based: simpler invariants (single writer), but leader failover adds complexity.
  - Leaderless (Dynamo-style): writes and reads go to multiple replicas; conflicts resolved on read/repair.
- Hinted handoff, read repair, anti-entropy:
  - Mechanisms to handle temporarily down replicas and eventual convergence.

Tuning examples:
- Fast reads: N=3, W=2, R=1 → AP-leaning, risk stale reads.
- Stronger reads: N=3, W=2, R=2 → CP-leaning for reads, higher latency.

---

## 5) Database Isolation Levels (OLTP)

- Read Uncommitted: dirty reads possible.
- Read Committed: no dirty reads; non-repeatable reads and phantoms possible.
- Repeatable Read: no dirty/non-repeatable reads; phantoms may occur (depends on DB).
- Serializable: appears as if transactions ran one-by-one (may be via locking or SSI).

Common DB notes:
- PostgreSQL: Repeatable Read uses MVCC (no non-repeatable reads; phantom avoidance differs); Serializable Snapshot Isolation (SSI) prevents anomalies with predicate locks.
- MySQL/InnoDB: Repeatable Read often prevents phantom reads with next-key locking, but semantics vary with settings.
- Spanner: External consistency (global serializability) via TrueTime.

Interview angle:
- Map app requirements to minimal isolation level (e.g., payments → serializable; analytics → read committed).

---

## 6) Conflict Detection and Resolution

- Detection methods:
  - Last-Write-Wins (LWW) via timestamps (danger with clock skew).
  - Vector clocks (detect concurrency, require merge policy).
  - Application-level constraints (e.g., per-key monotonic counters).
- Conflict-free Replicated Data Types (CRDTs):
  - Commutative/associative structures that converge (G-Counter, PN-Counter, OR-Set, LWW-Register with caveats).
- Merge strategies:
  - Commutative operations (additive counters).
  - Business-rule merges (e.g., cart: union of items, latest quantity per SKU).
  - Human-in-the-loop for irreconcilable conflicts.

---

## 7) Idempotency, Fencing, and Exactly-Once Illusion

- Exactly-once delivery is not guaranteed end-to-end across unreliable networks.
- Idempotency:
  - Use idempotency keys (request_id) so retries have no side effects.
  - Store processed IDs (inbox table) to dedupe.
- Outbox pattern:
  - Write DB row and outbox in same transaction; a relay publishes events to the log/queue.
- Fencing tokens:
  - For leader/lock scenarios, issue monotonically increasing tokens; reject stale writers (protects against “split brain”).
- Two-phase commit (2PC)
  - Consistent across participants but fragile under coordinator failure; high latency; often avoided in microservices. Prefer Sagas.

---

## 8) Eventual Consistency Design Patterns

- Read-your-writes via sessions:
  - Sticky sessions to a replica or read-after-write with per-client routing.
- Write-through vs write-behind caches:
  - Write-through for stronger consistency; write-behind for lower latency (risk of loss).
- Versioned keys:
  - Include version in key to force readers to fetch latest; clean up old versions async.
- Compensating transactions (Sagas):
  - For business workflows across services; define compensations on failure.
- De-duplication and Ordering:
  - Per-aggregate ordering via partition keys; application-level de-dup tables.

Pitfalls:
- Cache incoherence: ensure invalidation or TTLs; add jitter to avoid thundering herds.
- Clock skew: avoid LWW based purely on wall time; prefer logical clocks or fencing.

---

## 9) Global Consistency (TrueTime, Global Clocks)

- Google Spanner:
  - TrueTime API exposes bounded clock uncertainty [ε]. Transactions wait out uncertainty (commit-wait) to achieve external consistency.
- Hybrid Logical Clocks (HLC):
  - Combine physical and logical clocks; preserve causality with minimal skew sensitivity.
- Global transactions:
  - High-latency due to geo round-trips; consider per-region writes with asynchronous replication unless strict global order is required.

---

## 10) Testing and Validation

- Jepsen-style tests:
  - Inject partitions, clock skew, crashes; verify invariants (no lost updates, monotonicity).
- Property-based tests:
  - Define invariants and generate random event sequences to detect anomalies.
- Shadow traffic and canaries:
  - Validate consistency changes before full rollout.

---

## 11) Interview Playbook

- Step 1: Classify the workload
  - Per-key invariants? Cross-entity transactions? SLA (p95/p99)? Multi-region?
- Step 2: Choose model minimally sufficient
  - Cart/checkout: RYW + per-user session consistency may suffice.
  - Financial transfers: serializable or per-ledger linearizable writes with idempotent operations.
- Step 3: Sketch replication and quorum
  - RF=3; W=2, R=2 for strong reads; mention failure behavior.
- Step 4: Handle retries and duplicates
  - Idempotency keys; outbox/inbox; dedupe tables.
- Step 5: Operational plan
  - Monitoring for staleness, lag, replica health; backpressure policies.

---

## 12) Sample Questions

- Explain linearizability vs serializability with examples.
- For RF=5, what (R, W) provide linearizable reads? Tradeoffs of (R=3, W=3) vs (R=2, W=4).
- How to provide read-your-writes in a globally distributed app with CDNs and caches?
- Design idempotent payment processing with retries and “exactly-once” claim.
- Choose between CRDTs and application-level merges for collaborative editing.
- How does Spanner achieve external consistency? What is commit-wait and TrueTime ε?
