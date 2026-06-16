# REQUIREMENTS.md  

**Project:** ci‑loglens  
**Owner:** Axentx – AI‑Powered CI Log Analysis  
**Version:** 1.0.0  
**Last Updated:** 2026‑06‑16  

---  

## 1. Overview  

ci‑loglens is a SaaS tool that ingests continuous‑integration (CI) logs, applies AI‑enhanced parsing, classifies errors, and presents actionable visualizations. The goal is to reduce mean‑time‑to‑resolution (MTTR) for failed pipelines by ≥ 30 % for target customers (software teams using GitHub Actions, GitLab CI, Azure Pipelines, etc.).  

---  

## 2. Functional Requirements  

| ID | Description | Acceptance Criteria |
|----|-------------|----------------------|
| **FR‑1** | **Log Ingestion** – Accept log streams from supported CI providers (GitHub Actions, GitLab CI, Azure Pipelines, Jenkins). | • API endpoint `/ingest` accepts `multipart/form-data` or raw text.<br>• Returns `202 Accepted` with ingestion ID.<br>• Supports batch upload of up to **10 GB** per request (streamed). |
| **FR‑2** | **Source Metadata Extraction** – Capture CI run metadata (repo, branch, commit SHA, workflow name, job ID, timestamps). | • Metadata stored alongside raw log.<br>• Queryable via `/runs/{id}`. |
| **FR‑3** | **AI‑Powered Parsing** – Tokenize, segment, and classify log lines using the in‑house LLM (vLLM backend). | • ≥ 95 % line‑level classification accuracy on validation set (error, warning, info, stack‑trace).<br>• Processing latency ≤ 200 ms per MiB. |
| **FR‑4** | **Error Identification & Root‑Cause Suggestion** – Detect failure points and propose probable causes. | • Top‑3 suggestions returned with confidence scores.<br>• Precision ≥ 0.90 on held‑out test suite. |
| **FR‑5** | **Visualization Dashboard** – Interactive UI showing timeline, error hotspots, and correlation graphs. | • Users can filter by repo, branch, date range.<br>• Exportable as PNG / PDF.<br>• Responsive design (desktop ≥ 1024 px, mobile ≥ 600 px). |
| **FR‑6** | **Alerting & Notification** – Push notifications to Slack, Teams, or email when critical errors are detected. | • Configurable severity thresholds.<br>• Delivery latency ≤ 60 s from detection. |
| **FR‑7** | **Search & Query** – Full‑text search across logs with boolean operators and regex. | • Results returned within 1 s for ≤ 10 M log lines.<br>• Highlight matched terms. |
| **FR‑8** | **User Management** – Role‑based access control (Admin, Viewer, Analyst). | • JWT‑based auth, token expiry ≤ 24 h.<br>• Admin can create/delete users, assign roles. |
| **FR‑9** | **Data Retention & Export** – Store logs for configurable period (default 90 days) and allow CSV/JSON export. | • Automatic purge after retention period.<br>• Export job completes ≤ 5 min for 1 GB dataset. |
| **FR‑10** | **API Documentation** – OpenAPI 3.0 spec automatically generated and hosted. | • Docs accessible at `/docs` and kept in sync with code. |

---  

## 3. Non‑Functional Requirements  

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | • Ingestion throughput ≥ 500 MiB/min per node.<br>• End‑to‑end latency (ingest → dashboard view) ≤ 5 s for logs ≤ 50 MiB. |
| **NFR‑2** | **Scalability** | • Horizontal scaling via Kubernetes Deployment (stateless workers, stateful PostgreSQL + object storage).<br>• Auto‑scale based on CPU > 70 % or queue depth > 2000 jobs. |
| **NFR‑3** | **Reliability** | • 99.9 % uptime SLA (excluding scheduled maintenance).<br>• Data durability ≥ 99.999 % (replicated storage across 3 zones). |
| **NFR‑4** | **Security** | • All traffic TLS 1.3.<br>• At‑rest encryption (AES‑256) for logs and metadata.<br>• Role‑based access control enforced on every endpoint.<br>• Regular vulnerability scans (weekly) and patching within 48 h. |
| **NFR‑5** | **Compliance** | • Support for GDPR “right to be forgotten” – delete all data for a user on request within 24 h.<br>• SOC‑2 Type II readiness. |
| **NFR‑6** | **Observability** | • Export metrics to Prometheus (ingest rate, parse latency, error rate).<br>• Centralized logging via Loki/ELK.<br>• Health‑check endpoint `/healthz`. |
| **NFR‑7** | **Maintainability** | • Code coverage ≥ 80 % (unit + integration).<br>• CI pipeline with linting, static analysis, and automated security checks.<br>• Modular architecture: ingestion, parsing, storage, UI, notification. |
| **NFR‑8** | **Portability** | • Deployable on any Kubernetes‑compatible cloud (AWS EKS, GCP GKE, Azure AKS) using Helm chart. |
| **NFR‑9** | **Usability** | • UI onboarding wizard for first‑time users.<br>• Contextual help tooltips for each dashboard component. |
| **NFR‑10** | **Internationalization** | • UI strings externalized; support EN (default) and optional locale files. |

---  

## 4. Constraints  

1. **Technology Stack** – Must use the verified C‑frameworks listed in the company knowledge base (vLLM for inference, SGLang for structured generation).  
2. **Data Limits** – Raw logs stored no longer than the configured retention period; archival to cold storage (e.g., S3 Glacier) after 90 days.  
3. **Budget** – Initial cloud spend capped at **$12,000/month** for compute, storage, and third‑party services.  
4. **Compliance** – No third‑party services that store data outside of the EU for EU customers.  
5. **Version Compatibility** – Must support CI provider APIs as of their latest stable releases (GitHub Actions v2026‑06, GitLab 16.x, Azure Pipelines 2026‑06).  

---  

## 5. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Customers have a CI system that can forward logs via HTTP or write them to an object bucket accessible by ci‑loglens. |
| **A‑2** | The in‑house LLM model (vLLM) is already fine‑tuned on CI log data and can be queried via a gRPC endpoint. |
| **A‑3** | Users will provide API keys for Slack/Teams integrations; ci‑loglens does not need to manage OAuth flows. |
| **A‑4** | Existing Axentx authentication service (JWT) will be reused; no custom auth implementation required. |
| **A‑5** | The product will launch in English first; localization will be added in a later release. |
| **A‑6** | The underlying PostgreSQL instance will be provisioned with logical replication for high availability. |
| **A‑7** | The visualisation library (e.g., Apache ECharts) is compatible with the target browsers (Chrome ≥ 108, Edge ≥ 108, Firefox ≥ 107). |

---  

## 6. Acceptance Criteria Summary  

- All functional requirements FR‑1 – FR‑10 are implemented and pass automated integration tests.  
- Non‑functional thresholds (NFR‑1 – NFR‑10) are verified in staging with load‑testing scripts.  
- Documentation (API spec, user guide, deployment Helm chart) is complete and version‑controlled.  
- Security audit (internal) yields no critical findings.  

---  

*Prepared by:* Senior Product/Engineering Lead – ci‑loglens  
*Date:* 2026‑06‑16
