# ROADMAP.md – ci‑loglens  

**Product:** *ci‑loglens* – AI‑powered log analysis & error identification for CI systems.  
**Owner:** Senior Product/Engineering Lead – AxentX  
**Last Updated:** 2026‑06‑16  

---  

## 1. Vision & Success Metrics  

| Goal | KPI | Target (12 mo) |
|------|-----|----------------|
| Reduce mean‑time‑to‑resolution (MTTR) for CI failures | Avg. MTTR per failed pipeline | **≤ 30 min** |
| Increase developer productivity | % of pipelines resolved without manual log digging | **≥ 80 %** |
| Drive revenue | Paid seats (teams) | **≥ 150** |
| Model quality | F1‑score on error‑type classification (internal test set) | **≥ 0.92** |

All roadmap items are prioritized against these metrics.

---  

## 2. MVP – “Launch‑Ready Core”  

> **MVP‑Critical** items are bolded. They must be shipped before the public launch (Q4 2026).

| Milestone | Feature | Description | Owner | MVP‑Critical |
|-----------|---------|-------------|-------|--------------|
| **Log Ingestion** | **CI Provider Connectors** (GitHub Actions, GitLab CI, Azure Pipelines, CircleCI) | Secure webhook / API pull of raw logs per job. | Backend | ✅ |
| **AI Parsing Engine** | **vLLM‑backed inference service** | Deploy a lightweight LLM (e.g., Llama‑3‑8B) fine‑tuned on `auto` + `instr‑resp` datasets to extract error signatures, stack‑traces, and root‑cause tags. | ML/Infra | ✅ |
| **Error Classification** | **Pre‑trained taxonomy** (build‑failure, test‑failure, infra‑error, flaky‑test, permission‑error, etc.) | Model outputs a top‑3 ranked error type with confidence scores. | ML | ✅ |
| **Visualization UI** | **Web dashboard** (React + D3) | • Timeline view of log streams<br>• Highlighted error blocks<br>• One‑click “Open in IDE” link | Front‑end | ✅ |
| **Search & Filter** | Full‑text + tag‑based search across ingested logs | Enables developers to locate similar failures across history. | Backend | ✅ |
| **Auth & Multi‑Tenant** | OAuth2 (GitHub/Google) + tenant isolation | Guarantees data privacy per organization. | Infra | ✅ |
| **Observability** | Metrics (Prometheus) & health checks | Track ingestion latency, inference latency, error‑rate. | Infra | ✅ |
| **Documentation & Quick‑Start** | README, API spec, sample CI config snippets | Reduces friction for early adopters. | Docs | ✅ |

**MVP Release Window:** Q4 2026 (Oct – Dec).  

---  

## 3. Phase 1 – v1 (Feature‑Rich Expansion)  

| Theme | Feature | Description | Target Quarter |
|-------|---------|-------------|----------------|
| **Deep Contextual Insight** | **Root‑Cause Explanation** | Generate natural‑language “Why did this fail?” paragraphs using SGLang structured generation. | Q1 2027 |
| | **Log Diff & Regression Detection** | Compare current failure logs with historical runs to surface regressions. | Q1 2027 |
| **Collaboration** | **Comment & Annotation Layer** | Teams can add notes to highlighted error blocks; persisted per tenant. | Q2 2027 |
| | **Slack / Teams Bot** | Push concise failure summaries to configured channels with a link to the dashboard. | Q2 2027 |
| **Performance & Scale** | **Batch Inference Queue** | Process large log archives overnight using vLLM’s distributed scheduler. | Q2 2027 |
| | **Edge‑Cache for Frequent Errors** | Memoize inference results for recurring error patterns (≈ 80 % of failures). | Q2 2027 |
| **Data Enrichment** | **Link to External Knowledge Bases** (GitHub Issues, JIRA, StackOverflow) via LLM‑driven entity linking. | Q3 2027 |
| | **Custom Taxonomy Builder** | UI for orgs to define/extend error categories; auto‑re‑train on‑demand. | Q3 2027 |
| **Security & Compliance** | **Audit Logging** | Immutable record of who accessed which logs and when. | Q3 2027 |
| | **GDPR / SOC‑2 Controls** | Data‑retention policies, encryption‑at‑rest, role‑based access. | Q4 2027 |

---  

## 4. Phase 2 – v2 (Enterprise & Automation)  

| Theme | Feature | Description | Target Quarter |
|-------|---------|-------------|----------------|
| **Automation** | **Auto‑Remediation Playbooks** | Trigger predefined scripts (e.g., cache‑clear, dependency‑upgrade) based on error type. | Q1 2028 |
| | **CI‑Gate Integration** | Fail or block PR merges automatically if error severity > threshold. | Q1 2028 |
| **Advanced AI** | **Few‑Shot Prompt Library** | Leverage SGLang to produce actionable fix suggestions per error taxonomy. | Q2 2028 |
| | **Continuous Model Improvement Loop** | Feed validated developer corrections back into the training pipeline (using `messages` & `conversations` datasets). | Q2 2028 |
| **Enterprise Ops** | **Self‑Hosted / On‑Prem Deployment** | Docker‑Compose + Helm charts for isolated customer environments. | Q3 2028 |
| | **SLA Dashboard** | Real‑time SLA
