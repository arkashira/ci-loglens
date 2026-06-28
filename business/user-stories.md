## 📄 `user-stories.md`

### Epic 1 – **Log Ingestion & Normalization**
| # | User Story (Connextra) | Acceptance Criteria | Complexity |
|---|------------------------|---------------------|------------|
| 1.1 | **As a CI pipeline engineer, I want the tool to automatically pull logs from my CI provider (GitHub Actions, GitLab CI, Jenkins, CircleCI), so that I never have to manually export log files.** | - Connectors exist for the 4 most‑used CI services.<br>- OAuth / PAT authentication is supported and stored securely.<br>- Logs are fetched in real‑time after each job finishes.<br>- Ingestion succeeds for logs up to 50 MB without truncation.<br>- Failure to fetch logs produces a clear error message and retry option. | **M** |
| 1.2 | **As a DevOps manager, I want all incoming logs to be normalized into a common JSON schema, so that downstream analysis works uniformly across providers.** | - Each log line is stored with fields: `timestamp`, `level`, `message`, `source`, `ci_job_id`.<br>- Provider‑specific metadata (e.g., GitHub Action step name) is mapped to generic fields.<br>- Schema version is versioned and backward‑compatible.<br>- Validation step rejects malformed logs and logs the rejection reason.<br>- Normalized logs are stored in an indexed store (e.g., Elasticsearch) within 5 seconds of ingestion. | **S** |
| 1.3 | **As a security auditor, I want sensitive data (tokens, passwords) automatically redacted from ingested logs, so that logs can be safely stored and shared.** | - Regex‑based and ML‑based secret detection runs on every line.<br>- Detected secrets are replaced with `***REDACTED***` before storage.<br>- Redaction logs which secrets were removed (without revealing them).<br>- Option to whitelist custom patterns.<br>- Redaction passes OWASP secret‑leak test suite. | **M** |

---

### Epic 2 – **AI‑Powered Error Detection & Classification**
| # | User Story (Connextra) | Acceptance Criteria | Complexity |
|---|------------------------|---------------------|------------|
| 2.1 | **As a developer, I want the system to automatically surface the top‑3 probable error causes for a failed job, so that I can focus my debugging effort.** | - An LLM (e.g., Claude‑3.5 Sonnet) processes the normalized log and returns up to 3 ranked error hypotheses.<br>- Each hypothesis includes a confidence score ≥ 70 % and a short justification.<br>- Results appear in the UI within 8 seconds of log upload.<br>- Hypotheses can be expanded to view supporting log excerpts.<br>- Accuracy ≥ 80 % on a held‑out validation set of 1 k failed jobs. | **L** |
| 2.2 | **As a QA lead, I want recurring error patterns to be automatically grouped into “error signatures”, so that we can track flaky tests over time.** | - The system clusters similar failure messages using semantic similarity (> 0.85 cosine).<br>- Each signature receives a unique ID and a summary (e.g., “npm install timeout”).<br>- Dashboard shows frequency trend per signature (daily/weekly).<br>- New logs that match an existing signature are auto‑tagged.<br>- Ability to merge or split signatures manually. | **M** |
| 2.3 | **As a site reliability engineer, I want the AI to suggest a concrete remediation step (e.g., “increase timeout to 300s”), so that I can apply fixes faster.** | - For each error hypothesis, the model proposes at most one actionable recommendation.<br>- Recommendation is sourced from a curated knowledge base (e.g., official CI docs) or generated with citation links.<br>- Recommendation is marked “verified” only after a human reviewer approves it.<br>- UI shows “Apply” button that copies a ready‑to‑paste snippet to the clipboard.<br>- Post‑remediation, the system tracks whether the same error recurs. | **L** |

---

### Epic 3 – **Visualization & Interactive Debugging**
| # | User Story (Connextra) | Acceptance Criteria | Complexity |
|---|------------------------|---------------------|------------|
| 3.1 | **As a developer, I want a timeline view that highlights error spikes and correlates them with CI stages, so I can quickly locate the failing step.** | - Timeline shows stages (checkout, build, test, deploy) as colored bands.<br>- Log lines are plotted; error lines are highlighted in red.<br>- Hovering a point shows the raw log excerpt.<br>- Zoom/pan works smoothly for logs up to 100 k lines.<br>- Exportable as PNG or JSON. | **M** |
| 3.2 | **As a team lead, I want to filter logs by severity, keyword, or custom tag, so that I can focus on the most relevant information.** | - UI provides multi‑select filters for `level`, `keyword`, `signature ID`.<br>- Filter state is reflected in the URL for sharing.<br>- Filtered view updates within 300 ms.<br>- Ability to save filter presets per project.<br>- Filters work in combination (AND logic). | **S** |
| 3.3 | **As a DevOps engineer, I want to compare two runs side‑by‑side (e.g., before/after a config change), so that I can see what changed in the logs.** | - User can select any two job IDs from the same pipeline.<br>- UI aligns logs by timestamp and highlights added/removed lines.<br>- Diff view supports collapsing unchanged blocks.<br>- Exportable diff as markdown code block.<br>- Works for logs up to 200 MB. | **L** |

---

### Epic 4 – **Collaboration, Alerts & Integrations**
| # | User Story (Connextra) | Acceptance Criteria | Complexity |
|---|------------------------|---------------------|------------|
| 4.1 | **As a developer, I want the tool to post a concise error summary to my Slack channel when a job fails, so the whole team is instantly aware.** | - Configurable Slack webhook per project.<br>- Message includes job ID, error signature, confidence, and a link to the detailed view.<br>- Delivered within 5 seconds of failure detection.<br>- Ability to mute alerts for a configurable window (e.g., 30 min).<br>- Retry logic for failed webhook deliveries. | **S** |
| 4.2 | **As a product manager, I want to assign a failed job to a teammate directly from the UI, so that ownership is clear.** | - “Assign” button appears on each error view.<br>- Assignment creates a ticket in the linked issue tracker (GitHub Issues, Jira).<br>- Ticket includes log excerpt, AI hypothesis, and a link back to ci‑loglens.<br>- Assignee receives email and in‑app notification.<br>- Assignment status is visible on the dashboard. | **M** |
| 4.3 | **As a security compliance officer, I want audit logs of who accessed which CI logs and when, so that we can meet governance requirements.** | - Every UI view, export, or API call is logged with user ID, timestamp, and action type.<br>- Logs are immutable and stored for at least 90 days.<br>- Exportable in CSV/JSON format.<br>- Role‑based access control (RBAC) restricts log view permissions.<br>- Audit logs themselves are tamper‑evident (hash‑chained). | **M** |

--- 

*All stories are scoped for the MVP release of **ci‑loglens**. Complexity estimates follow the internal S/M/L scale (S ≈ 1‑2 person‑days, M ≈ 3‑5 person‑days, L ≈ 6‑10 person‑days).*