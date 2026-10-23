---
name: source-rights-check
description: 'Reads data/sources.yaml. Decides fetch/index/evidence eligibility. Never infers permission from government hosting.'
---
# source-rights-check Skill

Use when deciding whether a source can be fetched, indexed, or used as answer evidence.

## Rules (from AGENTS.md and docs/decisions.md)

1. Only `licence_status == "confirmed open"` with a quoted license quote may be fetched freely.
2. `legacy: true` → never index; `answer_evidence: false`.
3. `local_only: true` + `answer_evidence: true` + `approval_note` + `approved_on` + `approved_by` = only approved local path (e.g., `citizenship_kathmandu_requirements`).
4. `unclear` or `all rights reserved` → never index; never redistribute.
5. Never infer reuse from `.gov.np` URL.

## Quick check command

```bash
.\.venv\Scripts\python.exe -c "
import yaml
s = yaml.safe_load(open('data/sources.yaml'))['sources']
for src in s:
    eligible = False
    if src.get('licence_status') == 'confirmed open' and src.get('answer_evidence'):
        eligible = True
    elif src.get('answer_evidence') and src.get('approval_note') and src.get('local_only'):
        eligible = True
    print(f\"{src['id']}: service={src.get('service')} legacy={src.get('legacy')} eligible={eligible}\")
"
```

Expected for current registry: all 12 `palika_guide` sources show `eligible=False`; 1 reference (`opendatanepal_environment_statistics_2019`) shows `eligible=False` (reference, not civic); legacy sources (`citizenship_kathmandu_requirements`) show `eligible=True` only if `approval_note` present.
