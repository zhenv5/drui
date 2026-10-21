# V1.4 — Strict multi-lens independent review

- DRUI remains a single Skill; added `review-tl`, `review-pm`, `review-user`, `review-triad`, `review-loop` (20 total workflows).
- Read-only role-specific audits with isolation guidance, evidence requirements, 5-axis rubrics, prioritized P0/P1/P2/P3 findings.
- Machine-checkable reports via `gamekit.py review prepare` / `review evaluate`. Blank/incomplete reports cannot pass; signoff requires role averages >=9, axes >=8, no unresolved P0/P1 and independent execution contexts.
- Triad decision matrix and implementation-only fix loop with fresh re-test evidence, max 3 cycles.
- Upgrade-safe; no new separate Agent skill; external original `oil-ui` unaffected.
- Limitations: no agent sessions or actual simulator runs performed by installing toolkit; validator checks report syntax/evidence files only, not their authenticity.
