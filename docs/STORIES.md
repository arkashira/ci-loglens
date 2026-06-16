# STORIES.md – ci‑loglens

## Overview
**ci‑loglens** is an AI‑powered log analysis and error‑identification tool for Continuous Integration (CI) pipelines.  
The backlog below is organized into **Epics**, each containing concrete **User Stories** written in the *“As a \<role\>, I want \<goal\>, so that \<benefit\>”* format, with clear **Acceptance Criteria**. Stories are ordered to support a Minimum Viable Product (MVP) and subsequent incremental releases.

---

## EPIC 1 – Core AI Parsing Engine  
*Enable reliable, language‑agnostic extraction of errors, warnings, and actionable insights from CI logs.*

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| 1 | **As a CI Engineer, I want the system to ingest raw CI logs automatically, so that I don’t have to manually upload files.** | - The service accepts log streams via HTTP POST and via a CLI `ci-loglens ingest`. <br> - Supports gzip‑compressed and plain‑text logs up to 100 MB. <br> - Returns a 202 response with an ingestion ID. |
| 2 | **As a Data Scientist, I want the AI parser to identify error signatures and stack traces, so that downstream analysis can focus on real failures.** | - Uses the vetted `vLLM` inference engine to run the pre‑trained log‑analysis model. <br> - Returns a JSON payload with: <br> • `error_type`, `message`, `file`, `line`, `stack_trace` (if present). <br> • Confidence score ≥ 0.85 for each extracted item. |
| 3 | **As a QA Lead, I want the parser to classify log entries into “Error”, “Warning”, “Info”, and “Success”, so that I can filter noise.** | - Each log line receives a `category` field. <br> - Classification accuracy ≥ 92 % on the internal `auto` dataset (validated on a hold‑out set). |
| 4 | **As a DevOps Manager, I want the parsing results to be stored in a searchable datastore, so that I can query historic failures.** | - Parsed results are persisted in PostgreSQL with full‑text search enabled. <br> - Indexes on `ingestion_id`, `error_type`, `timestamp`. <br> - Query latency ≤ 200 ms for 1 M records. |

---

## EPIC 2 – CI System Integration  
*Provide seamless hooks for major CI providers to feed logs into ci‑loglens.*

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| 5 | **As a GitHub Actions user, I want a ready‑to‑use action that sends job logs to ci‑loglens, so that I can automate analysis.** | - Published as `axentx/ci-loglens-action`. <br> - Action accepts `api_key` and optional `run_id`. <br> - On success, logs a summary URL in the workflow output. |
| 6 | **As a GitLab CI user, I want a CI job template that streams logs in real‑time, so that analysis begins before the job finishes.** | - Provides a Docker image `axentx/ci-loglens-runner`. <br> - Streams logs via WebSocket to the ingestion endpoint. <br> - Emits a `loglens_report_url` artifact. |
| 7 | **As a Jenkins administrator, I want a plugin that adds a “Publish to ci‑loglens” post‑build step, so that existing pipelines need minimal changes.** | - Plugin compatible with Jenkins 2.462+. <br> - Configurable API endpoint, auth token, and optional tags. <br> - Shows parsing summary on the build page. |

---

## EPIC 3 – Visualization & Dashboard  
*Present parsed insights in an intuitive UI for rapid debugging.*

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| 8 | **As a Developer, I want a web dashboard that lists recent CI failures with highlighted error lines, so that I can locate the root cause quickly.** | - Dashboard page `/dashboard` shows a table of the last 50 ingestions. <br> - Each row displays: pipeline name, status badge, top error message, confidence, and a “View Details” link. |
| 9 | **As a Team Lead, I want a timeline view of error frequency per project, so that I can spot regressions.** | - Interactive chart (Chart.js) plotting daily error count for selected project. <br> - Hover shows breakdown by error type. |
| 10 | **As an Engineer, I want to drill‑down from a summary to the full parsed JSON and original log snippet, so that I can verify AI output.** | - Clicking “View Details” opens a modal with: <br> • Original log excerpt (highlighted). <br> • Parsed JSON tree. <br> • Confidence scores. |
| 11 | **As a Security Officer, I want role‑based access to the dashboard, so that only authorized users can view sensitive CI logs.** | - Integration with OAuth2 (Google, GitHub, SAML). <br> - RBAC matrix: `viewer`, `analyst`, `admin`. <br> - Unauthorized attempts return 403. |

---

## EPIC 4 – Alerting & Reporting  
*Notify stakeholders when critical failures are detected.*

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| 12 | **As a DevOps Engineer, I want configurable alerts (Slack, Email, Webhook) for high‑confidence errors, so that I can react instantly.** | - Alert rules
