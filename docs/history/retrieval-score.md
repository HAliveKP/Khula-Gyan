# Retrieval score

`src/retrieval/search.py` returns a `score` in the range **0–1**. Chroma stores
cosine distance, where smaller is closer; the search adapter reports
`clamp(1 - distance, 0, 1)` so higher scores mean closer matches. A score is a
similarity, **not** a probability that the answer is correct.

The configured `guard_min_score` is only a starting value. Calibrate it using
verified answerable and out-of-scope questions after the embedding test and
index are available. Dense search is the current implementation; BM25, RRF, and
reranking remain later retrieval improvements in the blueprint.

## Municipality filter (Palika Guide)

`search(query, k=5, service=None, municipality=None)` accepts an optional
`municipality` parameter. When provided, only chunks from that municipality
are returned. This enforces the safety rule: **never answer from another
municipality's charter**. If a question names a municipality with no indexed
charter, or names none and the UI selector is empty, the pipeline returns
`not_found` with a clarification message; it never answers from another
municipality's chunks.