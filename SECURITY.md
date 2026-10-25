# Security Policy

## Supported versions

This is a prototype with no versioned releases yet. Only the latest commit on `main` receives fixes.

| Version | Supported |
|---|---|
| `main` (latest) | Yes |
| older commits, other branches | No |

## Reporting a vulnerability

Please **do not open a public issue** for a security problem.

Report it privately through GitHub's private vulnerability reporting: open the repository's **Security** tab, then **Report a vulnerability** (or go to `https://github.com/HAliveKP/Khula-Gyan/security/advisories/new`). If that option is not shown, open a public issue that asks the maintainers for a private contact. Do not include any details of the problem in that issue.

Please include:

- what is affected (file, function, command) and the commit you tested;
- steps to reproduce, and what an attacker could do;
- whether any secret or private data was exposed.

This is a volunteer student project, so there is no guaranteed response time. We will acknowledge the report, keep you updated and credit you in the fix if you wish.

Examples of what is in scope: leaking API keys (in logs, errors, cache files or the UI), bypassing the spend cap, prompt injection through document text that makes the app present uncited or fabricated content as a cited answer, and dependency vulnerabilities that affect this project.

## Handling secrets

- API keys live only in a local `.env` file. `.env` and `.env.*` are ignored by Git, except the placeholder file `.env.example`. **Never commit `.env`**, and never paste a key into an issue, PR, prompt, screenshot or source file.
- The code never prints a whole key: `src/generation/llm.py` `mask()` shows only the last 4 characters.
- `MAX_API_SPEND_USD` (default `1.00`) caps the estimated spend per process. Every request is reserved against the cap and stopped before sending if it would exceed it. Real calls are refused until `LLM_INPUT_COST_PER_1M_USD` and `LLM_OUTPUT_COST_PER_1M_USD` are set. The estimate is not an invoice, so also set limits with your provider.
- LLM replies are cached in `artifacts/llm_cache/` (ignored). The cache contains prompts and document passages but no keys. Delete it if it may hold anything sensitive.
- If a key is ever exposed, revoke it with the provider immediately. Removing it from Git history alone is not enough.

## Data rights

The municipal charters used in development are **not** in this repository, because none of the municipalities has granted reuse or redistribution rights. Never commit source documents (`data/raw/`), extracted text (`data/processed/`, `data/readable/`) or the search index (`chroma_db/`). Record a document's rights in `data/sources.yaml`, and do not assume that public hosting on a government site grants permission. If you find copyrighted or personal data committed by mistake, report it privately as described above.
