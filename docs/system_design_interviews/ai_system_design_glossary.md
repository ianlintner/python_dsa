Title: AI System Design — Current Topics, Patterns, and Terms (Interview Cheat Sheet)

Purpose: A concise, staff-level reference to modern AI/LLM system design topics commonly asked in interviews. Includes patterns, tradeoffs, failure modes, and terms to drop in conversation.

1) Core LLM Concepts
- Tokenization: BPE/WordPiece; tokens/sec as primary throughput metric; context window (e.g., 4k–200k tokens) determines max prompt+response length.
- Latency anatomy:
  - TTFB (time-to-first-byte): dominated by prefill and scheduling.
  - TTFT (time-to-first-token) vs end-to-end latency (includes streaming).
  - Streaming responses reduce perceived latency.
- Throughput units: requests/sec, tokens/sec per GPU, cost/token; utilization matters more than raw FLOPs in production.
- Determinism controls: temperature/top-k/top-p; affects reproducibility and evals.
- Model families: decoder-only (GPT-style), encoder-decoder (T5), multimodal (vision-language, audio).

2) Inference Serving and Optimization
- Batching:
  - Static vs dynamic vs continuous batching (merge requests arriving within a small time window).
  - Tradeoff: larger batches → better GPU utilization but higher tail latency; use max batch delay and SLA-aware schedulers.
- KV cache:
  - Cache attention key/value tensors for previously generated tokens; reuse across steps.
  - Speculative decoding (draft with small model, verify with large model) to reduce latency.
- Attention optimizations:
  - FlashAttention, PagedAttention (vLLM), RoPE optimizations; memory locality.
- Quantization:
  - INT8/INT4/NF4, AWQ/GPTQ; reduces memory and increases throughput at possible quality loss.
  - QLoRA for fine-tuning (low-rank adapters on quantized base).
- Parallelism:
  - Tensor parallelism (intra-layer), pipeline parallelism (inter-layer), sequence parallelism, ZeRO sharding.
  - Use tensor/pipeline when model > single GPU memory; balance bubbles/comm overhead.
- CUDA/TensorRT:
  - TensorRT-LLM kernels, CUDA graphs; kernel fusion; compiled graphs for stable workloads.
- Continuous batching + prefix caching:
  - Reuse overlapping prompts; instruction-caching for RAG with frequent system prompts.

Serving stacks to know:
- vLLM (PagedAttention, continuous batching, OpenAI-compatible API)
- TGI (Text Generation Inference)
- TensorRT-LLM (NVIDIA-optimized)
- Ray Serve, Kubernetes + Triton Inference Server; MIG partitioning on A100/H100.

3) Retrieval-Augmented Generation (RAG)
- Ingestion pipeline:
  - Parsing (PDF/HTML), chunking (semantic/sentence-aware), deduplication, metadata tagging, PII scrubbing.
  - Embeddings generation (model choice matters; e5, bge, NV-Embed, text-embedding-3, jina, Instructor); track embedding version.
- Indexing:
  - Vector DBs: FAISS, Milvus, Weaviate, Qdrant; pgvector for Postgres; Elasticsearch/OpenSearch + kNN.
  - Hybrid search: combine dense (ANN) + sparse (BM25) + filters; re-ranking (cross-encoders).
- Query pipeline:
  - Retrieve top-k; filter by tenant/access control; re-rank to top-n; build context window with structured prompt.
  - Context control: chunk size/stride; map-reduce for long docs; citation tracking (doc spans).
  - Query rewriting: multi-query (HyDE), decomposition for complex queries.
- Patterns:
  - Caching: vector search results and per-user context summaries.
  - Freshness: incremental ingestion + background re-embed; hybrid timestamp-aware search.
  - Guardrails: retrieval-time content filters (leaks, PII); prompt-injection-resistant templates.

4) Prompt Engineering and Orchestration
- System prompts: role, constraints, output format (JSON schema), tool-use instructions.
- Few-shot vs zero-shot; chain-of-thought (cot) and constrained decoding; self-consistency.
- Tool use/function calling:
  - Defining tools with JSON schema; model chooses tools; orchestrator enforces rate limits and safety.
- Agents:
  - Reactive (single step) vs deliberative (multi-step planning), ReAct pattern (reason + act), state management, memory (short-term vs long-term vectors).
- Output constraints:
  - JSON mode / grammar-constrained decoding; reduce post-parse errors.

5) Fine-tuning and Adaptation
- SFT (supervised fine-tuning): task-specific data; risk of overfitting instructions.
- Preference optimization: RLHF, DPO, IPO; align with human preferences; evaluation drift risk.
- LoRA/PEFT/QLoRA for parameter-efficient fine-tuning; adapters per tenant to isolate behavior.
- Distillation: smaller student model mimics teacher; latency/cost reductions.
- Safety fine-tuning: augment refusal behavior; jailbreak resistance.

6) Multi-Tenancy, Privacy, and Governance
- Isolation:
  - Per-tenant rate limits, quotas, model configs; request tagging; per-tenant adapters/prompts.
- Data privacy:
  - No-training-on-customer-data policies; redact logs; on-by-default data minimization; DP if needed.
- Governance:
  - Content policies; age-appropriateness; regional compliance; audit trails; consent for training.
- Model routing:
  - Router service selects best model (quality/cost/latency) per request; maintains SLOs and budgets.

7) Evals and Quality Assurance
- Offline evals:
  - Golden sets, rubric grading (LLM-as-judge + calibrations), pass@k, hallucination/faithfulness metrics, citation accuracy for RAG.
- Online evals:
  - A/B tests, interleaving; guardrail regression tests; canary rollouts.
- Observability:
  - Token usage, cost per request, latency histograms, refusal rates, tool-failure rates, jailbreak attempts.
- Hallucination mitigation:
  - Retrieval grounding, constrained decoding, post-generation verifiers, entailment checks.

8) Safety, Security, and Abuse
- Prompt injection defenses:
  - Instruction isolation, system prompt hardening, content sanitization, tool call whitelists, no direct tool outputs into system prompts.
- Output filtering:
  - Blocklists, policy classifiers, structured safety reasons; redaction of PII; regional policies.
- Model supply chain:
  - Model provenance, checksum; secure model weights storage; access controls.
- Threats:
  - Data exfiltration via RAG (prompt injection) → remediate with source whitelisting, allowlists, retrieval filters, signed documents.

9) Cost and Capacity Planning
- GPU economics:
  - $/tok as primary unit; utilization via continuous batching; max batch delay tuning, SLA tiers.
  - Autoscaling: queue-depth, pending tokens, GPU duty cycle; cold-start mitigation with warm pools.
- CPU offload:
  - Small models on CPU for routing/filters; GPU reserved for heavy gen.
- Mixed precision/quant: Fused kernels; calibrate quality loss vs gains.
- Caching strategies:
  - Prompt prefix cache; response cache for deterministic prompts; docID cache in RAG.

10) MLOps and Lifecycle
- Data lifecycle:
  - Labeling, feedback loops; red teams; drift detection (content, embeddings).
- Versioning:
  - Model/version/embedding-version; experiment tracking; rollback plan.
- CI/CD:
  - Safety/eval gates; shadow deployments; control planes for prompts.

11) Multimodal Extensions
- Vision-language:
  - OCR vs visual Q&A; image-grounded safety; region-sensitive redaction.
- Speech:
  - Streaming ASR, low-latency TTS; chunked streaming; voice activity detection; diarization.
- Video:
  - Keyframe sampling; scene understanding; cost/latency tradeoffs.

12) Interview Playbook: Patterns to Mention
- Inference:
  - Continuous batching, KV cache reuse, speculative decoding, quantization, TensorRT-LLM, vLLM.
- RAG:
  - Hybrid ANN+BM25, cross-encoder re-rank, query rewriting, citation verification, metadata filters, incremental ingestion.
- Safety:
  - Prompt injection defenses, output classifiers, policy guards, PII redaction.
- Evals:
  - Golden sets + LLM-as-judge with calibration, online A/B, guardrail regression.
- Multi-tenant:
  - Model routing per tenant, adapters, quotas, isolation, usage billing.
- Observability:
  - Cost/latency dashboards by token stage; refusal/hallucination metrics; tool success rate.

13) Glossary (Rapid-Fire)
- KV Cache: cached attention key/value tensors enabling fast decode steps.
- Continuous Batching: merge requests dynamically to keep GPUs busy.
- PagedAttention: memory management for long contexts (vLLM).
- Speculative Decoding: small “draft” model proposed tokens verified by large model.
- LoRA/QLoRA: low-rank adapter fine-tuning; QLoRA uses quantized base.
- RAG: retrieval-augmented generation; ground outputs with external knowledge.
- Hybrid Search: combine dense vector search with sparse/BM25 and filters.
- Re-ranker: cross-encoder model rescoring retrieved passages.
- Guardrails: policies and classifiers to constrain prompts/outputs.
- DPO/RLHF: preference optimization methods aligning model behavior.
- Model Router: service selecting best model per request given SLO/cost.

Appendix A — Example AI Interview Prompts (use with these notes)
- Design a multi-tenant low-latency LLM inference platform (autoscaling, batching, KV-cache, cost).
- Design a production RAG system for enterprise knowledge with strict access controls.
- Design an eval harness and safety pipeline (guardrails, jailbreak detection, online A/B).
- Design an AI agent that uses tools and memory at scale (observability, failure recovery).

Use this document to sprinkle precise, modern terms and to structure tradeoff discussions crisply.
