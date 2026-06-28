**tech-spec.md**  
*Version: 1.0 – ci‑loglens*  

---  

## 1. Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | **Python 3.11** | Rich ecosystem for NLP/LLM inference (spaCy, transformers), fast prototyping, strong DevOps tooling. |
| **Web Framework** | **FastAPI** (async, OpenAPI auto‑gen) | Low latency, built‑in validation, easy to expose REST + WebSocket for streaming logs. |
| **AI/ML** | **HuggingFace Transformers** (distil‑roberta‑base‑log‑parser) + **spaCy** custom pipeline | Provides out‑of‑the‑box token classification for error pattern extraction; model size < 150 MB fits free tier. |
| **Visualization** | **React 18** + **Vite** (frontend) + **Recharts** for charts & **Logflare** style log stream UI | Modern, lightweight dev server; can be served as static assets from CDN. |
| **Database** | **PostgreSQL 15** (managed) + **TimescaleDB extension** for time‑series log storage | Strong relational model for users/projects + efficient time‑based queries for log windows. |
| **Cache / Queue** | **Redis 7** (managed) – used for rate‑limiting, short‑term token cache, and background job queue (RQ). |
| **Background Workers** | **RQ (Redis Queue)** + **Python workers** | Simple, zero‑config async processing of heavy log parsing jobs. |
| **Container Runtime** | **Docker 24** (multi‑stage builds) | Guarantees reproducible environments; used for both API and worker containers. |
| **Orchestration** | **Docker Compose** for local dev; **Fly.io** for production (free tier includes 3 VMs, 256 MiB RAM each). |
| **Testing** | **Pytest**, **Playwright** (E2E) | Unit + integration coverage > 80 %. |
| **CI/CD** | **GitHub Actions** (free tier) – lint → test → build → deploy to Fly.io staging → manual promote to prod. |

---

## 2. Hosting (Free‑Tier‑First)

| Component | Provider | Free‑Tier Details | Deployment Target |
|-----------|----------|-------------------|-------------------|
| **API + Workers** | **Fly.io** | 3 shared‑CPU VMs, 256 MiB RAM each, 3 GB outbound traffic/mo, 1 TB storage (via attached volume) | `api.ci-loglens.fly.dev` |
| **PostgreSQL** | **Supabase** (or **Neon.tech**) | 500 MB DB, 20 k rows/s, 2 GB storage, free tier includes built‑in authentication & row‑level security | `postgres.supabase.co` |
| **Redis** | **Upstash** | 10 MB memory, 10 k ops/s, serverless pricing (free tier) | `redis.upstash.io` |
| **Static Frontend** | **Vercel** | Unlimited preview deployments, 100 GB bandwidth/mo, 12 GB storage | `ci-loglens.vercel.app` |
| **Object Storage (log uploads)** | **Wasabi** (free tier 1 TB) or **AWS S3** (Free tier 5 GB) | Used for raw log file blobs; signed URLs for upload/download. | `s3.amazonaws.com/ci-loglens-uploads` |
| **Domain** | **Namecheap** (existing company domain) | CNAME to Fly.io & Vercel endpoints. | `loglens.axentx.com` |

*All services are selected to stay within free‑tier limits for a modest MVP (≤ 5 k active users/mo). Scaling to paid tiers is a single‑click config change.*

---

## 3. Data Model  

### 3.1 Relational Tables (PostgreSQL)

| Table | Primary Key | Key Fields | Description |
|-------|--------------|------------|-------------|
| **users** | `id` (UUID) | `email`, `hashed_password`, `role` (`admin`, `member`), `created_at` | Account management; IAM ties to projects. |
| **organizations** | `id` (UUID) | `name`, `owner_id`, `created_at` | Multi‑tenant grouping of projects. |
| **projects** | `id` (UUID) | `org_id`, `name`, `ci_provider` (`github_actions`, `gitlab_ci`, `jenkins`), `repo_url`, `created_at` | Logical CI pipelines. |
| **log_sessions** | `id` (UUID) | `project_id`, `run_id` (CI run identifier), `started_at`, `ended_at`, `status` (`pending`,`processing`,`completed`,`failed`) | One upload + analysis cycle. |
| **log_chunks** | `id` (UUID) | `session_id`, `chunk_index`, `blob_key` (object storage), `size_bytes` | Large logs are split for streaming. |
| **analysis_results** | `id` (UUID) | `session_id`, `summary_json`, `error_counts` (JSON), `created_at` | Output of AI parser. |
| **api_keys** | `id` (UUID) | `user_id`, `key_hash`, `created_at`, `revoked_at` | For programmatic access. |

### 3.2 Time‑Series Extension (TimescaleDB)

| Hypertable | Columns | Indexes |
|------------|---------|---------|
| **log_events** | `session_id` (UUID), `timestamp` (TIMESTAMPTZ), `level` (`INFO`,`WARN`,`ERROR`), `message` (TEXT), `metadata` (JSONB) | Primary index on `(session_id, timestamp DESC)`. |

*Log events are ingested from parsed chunks for fast window queries (e.g., “last 5 min errors”).*

---

## 4. API Surface  

| # | Method | Path | Auth | Purpose | Typical Response |
|---|--------|------|------|---------|------------------|
| 1 | **POST** | `/api/v1/auth/login` | – | Email/password login → JWT (access 15 min, refresh 7 d) | `{access_token, refresh_token}` |
| 2 | **POST** | `/api/v1/auth/refresh` | Refresh token | Issue new access token | `{access_token}` |
| 3 | **GET** | `/api/v1/projects` | Bearer | List projects user belongs to | `[{id,name,ci_provider}]` |
| 4 | **POST** | `/api/v1/projects` | Bearer | Create new CI project | `{id, name, ...}` |
| 5 | **POST** | `/api/v1/logs/{project_id}/upload` | Bearer | Initiate a log upload (multipart/form‑data or signed URL) → returns `session_id` and `upload_url` | `{session_id, upload_url}` |
| 6 | **GET** | `/api/v1/logs/{session_id}/status` | Bearer | Poll processing status (`pending/processing/completed`) | `{status, progress_pct}` |
| 7 | **GET** | `/api/v1/logs/{session_id}/summary` | Bearer | Retrieve AI‑generated error summary (JSON) | `{errors:[{type, count, snippet}], suggestions:[...]}` |
| 8 | **GET** | `/api/v1/logs/{session_id}/events` | Bearer | Stream parsed log events (supports `?since=ISO8601`) | NDJSON or SSE |
| 9 | **GET** | `/api/v1/visualization/{session_id}` | Bearer | Returns pre‑baked chart data (error trends, latency) | `{charts:{error_rate:[...], duration:[...]}}` |
|10| **POST** | `/api/v1/api-keys` | Bearer (admin) | Create programmatic API key | `{key_id, key_secret}` (secret shown once) |

*All endpoints return standard error envelope `{code, message, details?}` and follow OpenAPI 3.1 spec (auto‑generated by FastAPI).*

---

## 5. Security Model  

| Aspect | Implementation |
|--------|----------------|
| **Authentication** | JWT (HS256) signed with rotating secret stored in Fly.io secrets. Access token 15 min, refresh token 7 days (httpOnly, Secure, SameSite=Strict). |
| **Authorization (IAM)** | Row‑level security (RLS) policies in PostgreSQL enforce `org_id`/`project_id` ownership. FastAPI dependencies check `user.role` and project membership. |
| **Secrets Management** | All credentials (DB URL, Redis URL, AI model API keys, JWT secret) stored as **Fly.io secrets** and **Supabase env vars**; never in repo. |
| **API Keys** | Hash (`sha256`) stored; plain key shown only on creation. Used via `Authorization: Bearer <api_key>` header; rate‑limited (100 req/min per key). |
| **Data Encryption** | - At rest: PostgreSQL Transparent Data Encryption (managed by Supabase), S3/Wasabi server‑side encryption (AES‑256). - In transit: TLS 1.3 enforced everywhere (Fly.io edge certs, Cloudflare CDN for static assets). |
| **Input Validation** | Pydantic models for all request bodies; size limits on uploads (max 100 MB per log file). |
| **CORS** | Strict whitelist: `https://loglens.axentx.com`, `https://*.vercel.app`. |
| **Audit Logging** | Critical actions (login, API key creation, project deletion) written to `audit_events` table with user_id, timestamp, IP. |

---

## 6. Observability  

| Signal | Tooling | Retention |
|--------|---------|-----------|
| **Application Logs** | **Logflare** (free tier) via stdout → Fly.io log drain; structured JSON (`level, request_id, user_id, path`). |
| **Metrics** | **Prometheus** (embedded in Fly.io) + **Grafana Cloud** (free tier) – expose `/metrics` (request latency, error rates, queue depth). |
| **Traces** | **OpenTelemetry** SDK (Python) → **Jaeger** (self‑hosted on Fly.io free VM). |
| **Health Checks** | `/healthz` (ready/live) – returns DB, Redis, model load status. |
| **Alerting** | Grafana alerts → Slack channel `#ci-loglens-ops` for > 5 % error rate or queue backlog > 100. |
| **Dashboards** | Pre‑built Grafana dashboards for API latency, worker queue time, DB connection pool usage. |

---

## 7. Build / CI  

| Stage | GitHub Action | Description |
|-------|---------------|-------------|
| **Lint** | `python -m flake8 . && npm run lint` | Enforce code style (flake8, eslint). |
| **Test** | `pytest --cov=ci_loglens` + `playwright test` | Unit + integration + UI E2E. |
| **Security Scan** | `safety check -r requirements.txt` + `npm audit` | Fail on high‑severity vulnerabilities. |
| **Docker Build** | Multi‑stage Dockerfile → `docker buildx` for linux/amd64,linux/arm64. |
| **Publish** | Push image to **GitHub Container Registry** (public for demo, private for prod). |
| **Deploy Staging** | Fly.io `flyctl deploy --config fly.staging.toml` (auto‑trigger on `main` push). |
| **Manual Promote** | Workflow `workflow_dispatch` to promote `staging` image to `production`. |
| **Rollback** | `flyctl releases rollback` command available via Ops Slack bot. |

*All secrets accessed via GitHub Encrypted Secrets; Fly.io token stored as `FLY_API_TOKEN`.*  

---  

**End of tech-spec.md**  