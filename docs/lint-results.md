# Static Analysis Results (Centralized Lint)

**Generated:** 2026-07-21  
**Branch:** ttran @ 67f937e  
**Regenerate:** `npm run lint:report`

## Summary

| Repo | ESLint | Pylint | Flake8 | Overall |
|------|--------|--------|--------|---------|
| alexandria | N/A | 992 issues, score 7.35/10 (Fail) | 682 issues (Fail) | Fail |
| wayfinder | N/A | 353 issues, score 7.07/10 (Fail) | 180 issues (Fail) | Fail |
| VeriFi | 1 issue (Fail) | 29 issues, score 7.26/10 (Fail) | 2 issues (Fail) | Fail |
| Lens | 4 issues (Fail) | 38 issues, score 3.47/10 (Fail) | 23 issues (Fail) | Fail |
| SlugSync | 0 issues (Pass) | N/A | N/A | Pass |
| CsLife | N/A | N/A | N/A | Not covered |
| Examples | 0 issues (Pass) | 0 issues, score 10.00/10 (Pass) | 0 issues (Pass) | Pass |

## alexandria

**Python paths:** `repos/alexandria/src`

- **Pylint:** 992 issues, score 7.35/10 (Fail)
- **Flake8:** 682 issues (Fail)

**Sample Pylint findings:**

- `repos\alexandria\src\alexandria\ir\registry.py:11:15: E0001: Parsing failed: 'invalid syntax (alexandria.ir.registry, line 11)' (syntax-error)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:46:0: C0301: Line too long (96/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:49:0: C0301: Line too long (95/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:51:0: C0301: Line too long (98/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:55:0: C0301: Line too long (114/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:63:0: C0301: Line too long (114/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:68:0: C0301: Line too long (95/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:71:0: C0301: Line too long (98/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:227:0: C0301: Line too long (105/88) (line-too-long)`
- `repos\alexandria\src\alexandria\cli\browser_review.py:228:0: C0301: Line too long (99/88) (line-too-long)`
- _…truncated (10 shown)_

**Sample Flake8 findings:**

- `repos/alexandria/src\alexandria\cli\browser_review.py:46:89: E501 line too long (96 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:49:89: E501 line too long (95 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:51:89: E501 line too long (98 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:55:89: E501 line too long (114 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:63:89: E501 line too long (114 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:68:89: E501 line too long (95 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:71:89: E501 line too long (98 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:227:89: E501 line too long (105 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review.py:228:89: E501 line too long (99 > 88 characters)`
- `repos/alexandria/src\alexandria\cli\browser_review_test.py:27:89: E501 line too long (95 > 88 characters)`
- _…truncated (10 shown)_

## wayfinder

**Python paths:** `repos/wayfinder/backend/app`

- **Pylint:** 353 issues, score 7.07/10 (Fail)
- **Flake8:** 180 issues (Fail)

**Sample Pylint findings:**

- `repos\wayfinder\backend\app\main.py:53:0: C0301: Line too long (93/88) (line-too-long)`
- `repos\wayfinder\backend\app\main.py:6:0: E0401: Unable to import 'fastapi' (import-error)`
- `repos\wayfinder\backend\app\main.py:7:0: E0401: Unable to import 'fastapi.middleware.cors' (import-error)`
- `repos\wayfinder\backend\app\main.py:8:0: E0401: Unable to import 'fastapi.responses' (import-error)`
- `repos\wayfinder\backend\app\main.py:9:0: E0401: Unable to import 'sqlalchemy' (import-error)`
- `repos\wayfinder\backend\app\main.py:10:0: E0401: Unable to import 'sqlalchemy.exc' (import-error)`
- `repos\wayfinder\backend\app\main.py:11:0: E0401: Unable to import 'sqlalchemy.ext.asyncio' (import-error)`
- `repos\wayfinder\backend\app\main.py:39:19: W0621: Redefining name 'app' from outer scope (line 62) (redefined-outer-name)`
- `repos\wayfinder\backend\app\main.py:52:11: W0718: Catching too general exception Exception (broad-exception-caught)`
- `repos\wayfinder\backend\app\main.py:47:12: C0415: Import outside toplevel (app.services.dev_seed.ensure_dev_test_user) (import-outside-toplevel)`
- _…truncated (10 shown)_

**Sample Flake8 findings:**

- `repos/wayfinder/backend/app\core\config.py:1:89: E501 line too long (91 > 88 characters)`
- `repos/wayfinder/backend/app\core\config.py:16:89: E501 line too long (92 > 88 characters)`
- `repos/wayfinder/backend/app\core\config.py:42:89: E501 line too long (92 > 88 characters)`
- `repos/wayfinder/backend/app\core\config.py:63:89: E501 line too long (92 > 88 characters)`
- `repos/wayfinder/backend/app\core\config.py:82:89: E501 line too long (92 > 88 characters)`
- `repos/wayfinder/backend/app\db\session.py:1:89: E501 line too long (91 > 88 characters)`
- `repos/wayfinder/backend/app\main.py:53:89: E501 line too long (93 > 88 characters)`
- `repos/wayfinder/backend/app\models\travel.py:28:89: E501 line too long (99 > 88 characters)`
- `repos/wayfinder/backend/app\models\travel.py:30:89: E501 line too long (98 > 88 characters)`
- `repos/wayfinder/backend/app\models\travel.py:46:89: E501 line too long (97 > 88 characters)`
- _…truncated (10 shown)_

## VeriFi

**ESLint paths:** `repos/VeriFi/frontend/src`

- **ESLint:** 1 issue (Fail)
  - Errors: 1, Warnings: 0

**Python paths:** `repos/VeriFi/backend/retrieval`, `repos/VeriFi/backend/src`

- **Pylint:** 29 issues, score 7.26/10 (Fail)
- **Flake8:** 2 issues (Fail)

**Sample ESLint findings:**

- `C:\Users\woofy\cse15\repos\VeriFi\frontend\src\pages\ChatPage.tsx:92:5 error Definition for rule 'react-hooks/exhaustive-deps' was not found. (react-hooks/exhaustive-deps)`

**Sample Pylint findings:**

- `repos\VeriFi\backend\retrieval\embedder.py:5:0: E0401: Unable to import 'sentence_transformers' (import-error)`
- `repos\VeriFi\backend\retrieval\vector_client.py:28:0: C0301: Line too long (90/88) (line-too-long)`
- `repos\VeriFi\backend\src\main.py:114:0: C0301: Line too long (110/88) (line-too-long)`
- `repos\VeriFi\backend\src\main.py:16:0: E0401: Unable to import 'fastapi' (import-error)`
- `repos\VeriFi\backend\src\main.py:17:0: E0401: Unable to import 'fastapi.middleware.cors' (import-error)`
- `repos\VeriFi\backend\src\main.py:18:0: E0401: Unable to import 'pydantic' (import-error)`
- `repos\VeriFi\backend\src\main.py:30:0: C0413: Import "from retrieval import embedder, fallback_search, mapper, vector_client" should be placed at the top of the module (wrong-import-position)`
- `repos\VeriFi\backend\src\main.py:31:0: C0413: Import "from retrieval.config import CHUNKS_PATH, SEARCH_CLI_PATH" should be placed at the top of the module (wrong-import-position)`
- `repos\VeriFi\backend\src\main.py:32:0: E0401: Unable to import 'rag_pipeline' (import-error)`
- `repos\VeriFi\backend\src\main.py:32:0: C0413: Import "from rag_pipeline import generate_rag_response" should be placed at the top of the module (wrong-import-position)`
- _…truncated (10 shown)_

**Sample Flake8 findings:**

- `repos/VeriFi/backend/retrieval\vector_client.py:28:89: E501 line too long (90 > 88 characters)`
- `repos/VeriFi/backend/src\main.py:114:89: E501 line too long (110 > 88 characters)`

## Lens

**ESLint paths:** `repos/Lens/frontend`

- **ESLint:** 4 issues (Fail)
  - Errors: 4, Warnings: 0

**Python paths:** `repos/Lens/backend/app`

- **Pylint:** 38 issues, score 3.47/10 (Fail)
- **Flake8:** 23 issues (Fail)

**Sample ESLint findings:**

- `C:\Users\woofy\cse15\repos\Lens\frontend\app\page.tsx:84:10 error 'incidents' is assigned a value but never used. (@typescript-eslint/no-unused-vars)`
- `C:\Users\woofy\cse15\repos\Lens\frontend\app\page.tsx:84:21 error 'setIncidents' is assigned a value but never used. (@typescript-eslint/no-unused-vars)`
- `C:\Users\woofy\cse15\repos\Lens\frontend\app\page.tsx:140:17 error Unexpected any. Specify a different type. (@typescript-eslint/no-explicit-any)`
- `C:\Users\woofy\cse15\repos\Lens\frontend\app\page.tsx:202:5 error Definition for rule 'react-hooks/exhaustive-deps' was not found. (react-hooks/exhaustive-deps)`

**Sample Pylint findings:**

- `repos\Lens\backend\app\main.py:1:0: E0401: Unable to import 'fastapi' (import-error)`
- `repos\Lens\backend\app\main.py:3:0: E0401: Unable to import 'app.api.incidents' (import-error)`
- `repos\Lens\backend\app\main.py:4:0: E0401: Unable to import 'app.api.lens' (import-error)`
- `repos\Lens\backend\app\main.py:5:0: E0401: Unable to import 'app.api.neighborhoods' (import-error)`
- `repos\Lens\backend\app\api\incidents.py:65:0: C0301: Line too long (96/88) (line-too-long)`
- `repos\Lens\backend\app\api\incidents.py:12:0: E0401: Unable to import 'psycopg2' (import-error)`
- `repos\Lens\backend\app\api\incidents.py:13:0: E0401: Unable to import 'psycopg2.extras' (import-error)`
- `repos\Lens\backend\app\api\incidents.py:14:0: E0401: Unable to import 'fastapi' (import-error)`
- `repos\Lens\backend\app\api\incidents.py:15:0: E0401: Unable to import 'pydantic' (import-error)`
- `repos\Lens\backend\app\api\incidents.py:37:0: C0115: Missing class docstring (missing-class-docstring)`
- _…truncated (10 shown)_

**Sample Flake8 findings:**

- `repos/Lens/backend/app\api\incidents.py:65:89: E501 line too long (96 > 88 characters)`
- `repos/Lens/backend/app\api\lens.py:81:14: E221 multiple spaces before operator`
- `repos/Lens/backend/app\api\lens.py:90:89: E501 line too long (89 > 88 characters)`
- `repos/Lens/backend/app\api\lens.py:134:89: E501 line too long (89 > 88 characters)`
- `repos/Lens/backend/app\api\lens.py:137:89: E501 line too long (89 > 88 characters)`
- `repos/Lens/backend/app\api\lens.py:154:14: E221 multiple spaces before operator`
- `repos/Lens/backend/app\api\lens.py:172:89: E501 line too long (108 > 88 characters)`
- `repos/Lens/backend/app\api\lens.py:174:89: E501 line too long (89 > 88 characters)`
- `repos/Lens/backend/app\api\lens.py:195:18: E221 multiple spaces before operator`
- `repos/Lens/backend/app\api\lens.py:195:89: E501 line too long (98 > 88 characters)`
- _…truncated (10 shown)_

## SlugSync

**ESLint paths:** `repos/SlugSync/supabase/functions`

- **ESLint:** 0 issues (Pass)

_No issues reported._

## CsLife

Not covered by centralized lint (no paths in `scripts/lint.mjs`).

## Examples (`typescript/`, `python/`)

**ESLint paths:** `typescript`

- **ESLint:** 0 issues (Pass)

**Python paths:** `python`

- **Pylint:** 0 issues, score 10.00/10 (Pass)
- **Flake8:** 0 issues (Pass)

_No issues reported._

_No issues reported._

_No issues reported._

