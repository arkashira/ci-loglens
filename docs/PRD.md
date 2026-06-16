# ci‑loglens – Product Requirements Document (PRD)

**Document Version**: 1.0  
**Last Updated**: 2026‑06‑16  
**Owner**: Senior Product/Engineering Lead – ci‑loglens  
**Stakeholders**:  
- **Engineering** – Architecture, Backend, Front‑end, DevOps  
- **QA** – Test Automation, Release Validation  
- **Customer Success** – Early‑adopter support, feedback loop  
- **Sales / Business Development** – Market positioning, pricing  

---

## 1. Problem Statement

Continuous Integration (CI) pipelines generate massive, unstructured log streams. Teams spend **30‑45 %** of their debugging time manually sifting through these logs to locate the root cause of failures. Existing CI dashboards provide only coarse‑grained status (pass/fail) and limited search capabilities, leading to:

| Pain Point | Impact |
|------------|--------|
| **Noise** – logs contain repetitive boilerplate, making the real error hard to spot. | Increases MTTR (Mean Time To Resolve) by ~2 h per failure. |
| **Fragmentation** – logs are spread across multiple agents (Jenkins, GitHub Actions, GitLab CI, Azure Pipelines). | Requires context‑switching and manual aggregation. |
| **Lack of insight** – no automated classification of error types or suggested remediation. | Engineers rely on trial‑and‑error, slowing release cycles. |
| **Poor visualization** – raw text is not searchable or filterable in real time. | Reduces productivity and hampers post‑mortem analysis. |

**Result:** Slower release velocity, higher operational cost, and reduced developer satisfaction.

---

## 2. Target Users & Personas

| Persona | Role | Primary Goals | Pain Points Addressed |
|---------|------|---------------|-----------------------|
| **CI Engineer** | Maintains CI pipelines, configures agents. | Quickly locate failures, reduce false‑positive alerts. | Noise, fragmentation |
| **Software Engineer** | Writes code, runs tests locally & in CI. | Understand why a build failed without digging through raw logs. | Lack of insight, poor visualization |
| **Team Lead / Manager** | Oversees delivery cadence. | Reduce MTTR, improve release predictability. | High debugging overhead |
| **Site Reliability Engineer (SRE)** | Ensures reliability of CI infrastructure. | Detect systemic issues across pipelines, generate actionable reports. | Fragmentation, lack of insight |

---

## 3. Goals & Success Metrics

| Goal | Success Metric | Target (12 mo) |
|------|----------------|----------------|
| **Reduce MTTR for CI failures** | Avg. time from failure to root‑cause identification | ≤ 30 min (↓ 50 % vs baseline) |
| **Increase debugging efficiency** | % of failures resolved without manual log grep | ≥ 70 % |
| **Adoption** | Number of active CI pipelines using ci‑loglens | 150+ pipelines across ≥ 10 orgs |
| **Revenue** | ARR from ci‑loglens subscription | $1.2 M |
| **Customer satisfaction** | NPS for ci‑loglens | ≥ 55 |
| **Operational cost** | Avg. compute cost per analyzed log batch | ≤ $0.02 per 10 k lines |

---

## 4. Key Features (Prioritized)

| Priority | Feature | Description | MVP Acceptance Criteria |
|----------|---------|-------------|--------------------------|
| **P1** | **AI‑powered Log Parsing Engine** | Uses the company’s `vLLM` inference stack to classify log lines into *Info / Warning / Error / StackTrace* and extract structured fields (timestamp, component, error code). | - 95 % classification accuracy on a held‑out validation set (≥ 100 k log lines). <br> - Real‑time processing ≤ 200 ms per 10 k lines. |
| **P1** | **Unified Log Ingestion API** | Agent‑side SDKs (Jenkins, GitHub Actions, GitLab, Azure) push logs via a secure HTTP endpoint; supports batch & streaming modes. | - SDKs available for the 4 major CI providers.<br> - End‑to‑end test: a failing pipeline’s logs appear in the UI within 5 s. |
| **P1** | **Error Identification & Recommendation UI** | Dashboard shows top‑ranked error clusters per run, with AI‑generated remediation suggestions (e.g., “Missing environment variable X”). | - UI displays at least 3 suggestions per failure with ≥ 80 % relevance (human reviewer rating). |
| **P2** | **Cross‑Pipeline Correlation** | Detects recurring error patterns across multiple pipelines and surfaces trend graphs. | - Correlation engine groups ≥ 80 % of similar failures across pipelines. |
| **P2** | **Interactive Log Visualization** | Rich, searchable view with collapsible sections, syntax highlighting, and filter by severity, component, or time range. | - Users can locate a specific error line within 2 s of typing a keyword. |
| **P3** | **Alerting & Integration** | Configurable webhook/Slack/email alerts when new error types appear or error frequency spikes. | - Alert delivered within 30 s of detection. |
| **P3** | **Export & Reporting** | Generate PDF/HTML post‑mortem reports with charts and root‑cause summary. | - Export completes within 10 s for a typical 1‑day log window. |
| **P4** | **Self‑Hosted / On‑Prem Deployment** | Docker‑compose + Helm charts for customers with strict data residency requirements. | - Deployment guide passes CI test suite on Kubernetes 1.28+. |

---

## 5. Scope

### In‑Scope
- End‑to‑end pipeline: log ingestion → AI parsing → storage → UI visualization.
- Integration with the four most‑used CI platforms (Jenkins, GitHub Actions, GitLab CI, Azure Pipelines).
- Cloud‑native SaaS deployment (AWS/EKS) plus optional on‑prem Helm chart.
- Role‑based access control (admin, viewer, read‑only API key).
- Basic usage analytics (pipeline count, error frequency) for internal product insights.

### Out‑of‑Scope (Phase 1)
- Direct integration with non‑CI log sources (e.g., application runtime logs, Kubernetes pod logs) – planned for Phase 2.
- Deep code‑level static analysis linking errors to source lines – deferred to a future “ci‑code‑lens” product.
- Multi‑language natural‑language query interface – slated for Phase 3 after core AI parsing is stable.

---

## 6. Assumptions & Dependencies

| Assumption | Rationale |
|------------|-----------|
| Sufficient compute quota for `vLLM` inference (GPU‑A100) is available in the cloud environment. | Required for low‑latency parsing. |
| CI providers allow outbound HTTPS calls from agents (standard). | Enables SDK log push. |
| Customers are comfortable sending logs to a SaaS endpoint (TLS 1.3, at‑rest encryption). | Aligns with security policy; optional on‑prem for regulated sectors. |
| Existing internal datasets (`auto`, `instr‑resp`, `messages`) contain enough CI‑related log examples to fine‑tune the parser. | Reduces need for external data acquisition. |

**External Dependencies**
- `vLLM` repository (vLLM‑project/vllm) – for inference server.
- `SGLang` (sgl-project/sglang) – optional structured generation for suggestions.
- CI provider SDKs (open‑source or internal wrappers).

---

## 7. Milestones & Timeline (12 mo)

| Milestone | Deliverable | Owner | Target Date |
|-----------|-------------|-------|--------------|
| **M1 – Foundations** | Architecture design, data schema, ingestion API spec | Architecture Lead | 2026‑07‑15 |
| **M2 – AI Parsing Prototype** | Fine‑tuned vLLM model, unit tests, 95 % accuracy benchmark | ML Engineer | 2026‑08‑30 |
| **M3 – SDK & Ingestion** | Agent SDKs for Jenkins & GitHub Actions, CI pipeline demo | DevOps Engineer | 2026‑09‑20 |
| **M4 – Core UI MVP** | Dashboard with error list, suggestions, basic search | Front‑end Lead | 2026‑10‑15 |
| **M5 – Cross‑Pipeline Correlation** | Backend service for error clustering across pipelines | Backend Lead | 2026‑11‑10 |
| **M6 – Beta Release** | Private beta with 3 early‑adopter customers, feedback loop | PM / Customer Success | 2026‑12‑05 |
| **M7 – Public SaaS Launch** | Production SaaS, billing integration, documentation | Release Engineer | 2027‑02‑01 |
| **M8 – On‑Prem Helm Chart** | Helm chart + Docker images, validation tests | DevOps Lead | 2027‑03‑15 |
| **M9 – Success Review** | Metric collection, NPS survey, roadmap refinement | Product Ops | 2027‑04‑01 |

---

## 8. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Model drift / low parsing accuracy** | Medium | High (user trust) | Continuous fine‑tuning pipeline using newly ingested logs; automated regression tests. |
| **Log volume spikes overwhelm service** | Low | High | Autoscaling policies on inference pods; back‑pressure queue with durable storage (Kafka). |
| **Security/compliance concerns** | Medium | Medium | End‑to‑end TLS, at‑rest encryption, optional on‑prem deployment, SOC‑2 audit. |
| **SDK adoption friction** | Low | Medium | Provide clear docs, sample CI configs, and a CLI fallback. |
| **Vendor lock‑in perception** | Low | Low | Open‑source SDKs, data export APIs, transparent privacy policy. |

---

## 9. Acceptance Criteria (MVP)

- **Functional**: A failing CI run in any supported platform appears in the ci‑loglens UI within 5 seconds, with parsed error categories and at least one AI‑generated remediation suggestion.
- **Performance**: System processes ≥ 10 k log lines per second with ≤ 200 ms latency per batch.
- **Reliability**: 99.9 % uptime SLA for the SaaS endpoint; graceful degradation (fallback to raw log view) if AI service is unavailable.
- **Security**: All data in transit encrypted TLS 1.3; at‑rest encrypted with customer‑managed keys; RBAC enforced.
- **Usability**: New user can install SDK, configure a pipeline, and view a parsed error within 15 minutes (guided onboarding flow).

---

## 10. Open Questions

1. **Pricing model** – usage‑based (log volume) vs tiered (pipelines). Need finance input.
2. **Data retention policy** – default 30 days? Must align with GDPR/CCPA.
3. **Support for self‑hosted inference** – evaluate demand for on‑prem GPU clusters.

---

*Prepared by the ci‑loglens product team. This document serves as the definitive source of truth for all downstream design, development, and delivery activities.*
