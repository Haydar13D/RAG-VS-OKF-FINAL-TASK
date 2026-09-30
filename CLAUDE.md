# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A thesis (skripsi) research project: a head-to-head comparison of two retrieval strategies behind the same "Sora Assistant" customer-support chatbot for the Sora Seventh POS system. Code comments, docs, prompts, and test queries are in Indonesian.

- **system-rag/**: vector RAG using ChromaDB, `paraphrase-multilingual-MiniLM-L12-v2` embeddings, and a cosine-distance guardrail (`MAX_DISTANCE_THRESHOLD = 0.60`, `TOP_K = 5`). Port **8000**.
- **system-okf/**: "Open Knowledge Format" with **no vector DB, embeddings, or similarity search** (this is a hard methodological rule stated in `okf_navigator.py`). It scores documents by keyword overlap with frontmatter `category`/`tags`/`title`, keeps entry docs at or above `MIN_ENTRY_SCORE`, then expands one link hop via `prerequisites`/`related`, capped at `MAX_TOTAL_DOCS`. Port **8001**. `POST /chat?variant=stuffing` sends the whole corpus instead (`okf_context_stuffing.py`) as a baseline.
- **Root `app.py`, `ingest.py`, `docs/`, `chroma_db/`, `ollama_provider.py`, `tests/`, `test_query_app.py`**: the original single production chatbot the experiment grew out of. The root `README.md` and `CHANGELOG.md` mostly describe this legacy app. Some file lists in the README are stale; for example, `tests/*.py` now live under `tests/`.

## Experimental-control invariants (do not break)

The comparison is only valid if the two systems differ **only** in their retrieval mechanism:

- Both systems must use `shared/query_normalizer.normalize_query()` (typo map plus query expansion). Don't add preprocessing to one system only.
- The two `app.py` files deliberately duplicate `SYSTEM_PROMPT`, `REFUSAL_MESSAGE`, `_sanitize_answer()`, and `call_llm_with_failover()`. A change to one must be mirrored in the other.
- LLM chain order is the same in both: Ollama self-hosted (primary, `OLLAMA_DEFAULT_MODEL`, used for determinism), then Gemini, then OpenRouter, then Groq.
- Security fix from the 2026-08-29 changelog entry: **never put document titles, categories, or `[Sumber: ...]` labels into the context sent to the LLM.** Only the raw body/chunk text is sent. Titles stay in metadata (`nav_metadata`) for logging. Output is also regex-sanitized as defense in depth.
- `system-rag/docs/` and `system-okf/docs/` hold the same 36 docs with the same body text. The only difference is that the OKF copies add `prerequisites`/`related` link fields to the frontmatter. Keep the text identical ("informational parity"). Both must satisfy `docs-shared-schema/knowledge_schema.yaml`, which requires `id` (`DOC-..`), `title`, `category` enum, `target_role` enum, and `tags`. Root `docs/` is the legacy corpus and is not part of the experiment.
- Response contract used by the eval scripts: `{answer, sources, status: ANSWERED|KNOWLEDGE_GAP|ERROR, provider_used, min_distance_score (RAG), nav_metadata (OKF)}`.

## Commands

Dependencies are managed with **uv**. `pyproject.toml` and `uv.lock` are the source of truth, and Python is pinned to 3.12 in `.python-version`. Run `uv sync` to set up, `uv add <pkg>` to add a dependency, and `uv run ...` to execute anything. Don't use pip or `requirements.txt`. Secrets and Ollama settings come from the root `.env`.

```bash
# Rebuild the RAG vector index (deletes and recreates the "pos_knowledge" collection) after editing system-rag/docs
uv run python system-rag/ingest.py

# Validate the doc corpora: schema, count == 36, OKF link targets exist, RAG/OKF text parity
uv run python validate_docs.py
uv run python audit_docs.py              # frontmatter/link audit report

# Run the two servers (each app imports siblings via sys.path, so launch from inside its folder)
cd system-rag && uv run uvicorn app:app --port 8000
cd system-okf && uv run uvicorn app:app --port 8001
curl localhost:8000/health; curl localhost:8001/health

# Evaluation (servers must be running). Run once per system with matching label/output.
uv run python eval/run_eval.py          --target-url http://localhost:8000/chat --system-label RAG --output eval/results_rag.json
uv run python eval/run_eval_advanced.py --target-url http://localhost:8001/chat --system-label OKF --output eval/results_okf_N40.json
uv run python eval/leak_rate_tester.py  --target-url http://localhost:8000/chat --system-label RAG --runs 20 --output eval/leak_rate_rag.json
uv run python eval/system_profiler.py   --target-url http://localhost:8000/chat --system-label RAG --output eval/profile_rag.json
uv run python eval/statistical_analysis.py   # Wilcoxon + rank-biserial on profile_rag.json vs profile_okf.json

# Calibrate the OKF MIN_ENTRY_SCORE (prints navigator scores for in-domain vs out-of-domain queries)
uv run python calibrate_okf_score.py
```

There is no pytest suite. Files under `tests/` are standalone benchmark scripts for the legacy root app (threshold calibration, prompt-injection runs, analysis of the gap queries in the log).

## Eval data

- Test sets: `eval/accuracy_test_set_FINAL.json`, `eval/injection_scenarios_FINAL.json`, `eval/test_dataset_extended_N40.json`.
- Result files (`results_*`, `profile_*`, `leak_rate_*`, `statistical_results.json`) are committed thesis evidence. Don't overwrite them casually. Use a new output path unless you are intentionally re-running.
- Methodology, the fix plan, and the manual Likert scoring rubric are in `dokumentasi testing/`.
- Conversation logs go to `logs/rag_conversations.jsonl` and `logs/okf_conversations.jsonl`.

## Known inconsistencies

- In `okf_navigator.py`, the calibration comment recommends `MIN_ENTRY_SCORE = 5`, but the code uses `3`. Check which one is intended before relying on either.
- Distances in the RAG system shift after every re-ingest (see `CHANGELOG.md`). Re-run the threshold benchmarks after changing the docs.
