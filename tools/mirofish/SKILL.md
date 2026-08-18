---
name: mirofish
description: Operate the MiroFish swarm-intelligence prediction engine locally — start the backend, prepare, launch, monitor, stop, and generate reports for multi-agent social simulations (Twitter/Reddit/parallel) via its Flask REST API. Use whenever the user mentions MiroFish, swarm simulation, agent prediction, or a sim_* ID.
---

# MiroFish — swarm simulation runner

Operate a MiroFish multi-agent social simulation end to end: start the Flask
backend, verify preparation, launch a run, monitor both platforms, stop it
cleanly, inspect artefacts, and generate the prediction report.

---

## 1. When to use

- Launch, monitor, or stop a MiroFish multi-agent social simulation.
- Generate a prediction report from a completed simulation.
- Inspect simulation artefacts (actions, posts, timeline, agent stats).
- The user says "MiroFish", "swarm simulation", "agent prediction", or
  references a `sim_*` ID.

---

## 2. Prerequisites

**Essential (API operation):**
- Python ≥3.11, ≤3.12 (NOT 3.13+). The venv at `backend/.venv` was created with
  3.12.x — use `uv run` which picks it up automatically.
- `uv` package manager.
- `.env` file at project root with `LLM_API_KEY`, `LLM_BASE_URL`,
  `LLM_MODEL_NAME`, `ZEP_API_KEY`. MiroFish uses any OpenAI-compatible endpoint.
  `load_dotenv(override=True)` runs at import time in `config.py`, so `.env`
  wins over environment variables — but changes require a backend restart.
- A prepared simulation (profiles + config already generated).

**Optional:**
- Node.js 18+ (frontend only; not needed for API-only operation).

---

## 3. Project layout

```
mirofish-project/
├── backend/
│   ├── app/
│   │   ├── api/            # Flask blueprints: simulation.py, report.py, graph.py
│   │   ├── services/       # simulation_manager.py, simulation_runner.py, report_agent.py, ...
│   │   └── utils/          # llm_client.py, zep.py, ...
│   ├── uploads/simulations/<sim_id>/
│   │   ├── simulation_config.json
│   │   ├── state.json
│   │   ├── twitter/actions.jsonl
│   │   ├── twitter_simulation.db
│   │   ├── reddit/actions.jsonl
│   │   ├── reddit_simulation.db
│   │   └── simulation.log
│   └── run.py             # Entry point
├── .env                   # LLM_API_KEY + ZEP_API_KEY
└── package.json
```

---

## 4. Quick start (experienced users)

```bash
# 1. Start backend (background, stays alive)
cd <mirofish>/backend && exec uv run python run.py
# 2. Health check (wait ~6-8s)
curl -s http://localhost:5001/health --max-time 10
# 3. Launch
curl -s -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"simulation_id":"sim_xxxx","platform":"parallel","max_rounds":20,"force":true}'
# 4. Poll until both platforms complete
curl -s http://localhost:5001/api/simulation/sim_xxxx/run-status
# 5. Stop
curl -s -X POST http://localhost:5001/api/simulation/stop \
  -H "Content-Type: application/json" -d '{"simulation_id":"sim_xxxx"}'
# 6. Generate report
curl -s -X POST http://localhost:5001/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{"simulation_id":"sim_xxxx","prediction_requirements":"Summarize key opinions and sentiment trends"}'
# 7. Poll report status with task_id, then download
curl -s http://localhost:5001/api/report/<report_id>/download
```

For full details on each step, see §5 (Workflow). For troubleshooting, see §7.

---

## 5. Workflow

### Step 1 — Start the backend

```bash
cd <mirofish-backend-dir>
exec uv run python run.py
```

Run as a **background process** — it's a Flask server that stays alive.
Do NOT use `nohup … &` (see §7-P1). Verify after ~6-8 seconds:

```bash
curl -s http://localhost:5001/health --max-time 10
# Expect: {"service":"MiroFish Backend","status":"ok"}
```

If the health check fails, check:
- Backend log output (import errors, missing `.env`, port conflict).
- `.env` file exists at project root with all required keys (§2).

### Step 2 — Verify the simulation is prepared

```bash
curl -s -X POST http://localhost:5001/api/simulation/prepare/status \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxx"}'
```

Look for `"status": "ready"` and `prepare_info.profiles_count > 0`.

If not prepared, the preparation flow (`/api/simulation/prepare`,
`/api/simulation/generate-profiles`) is **out of scope** for this skill — ask
the user to prepare it first.

### Step 3 — Launch the simulation

```bash
curl -s -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{
    "simulation_id": "sim_xxxx",
    "platform": "parallel",
    "max_rounds": 20,
    "force": true
  }'
```

Parameters:

| Parameter | Required | Values | Notes |
|-----------|----------|--------|-------|
| `simulation_id` | yes | `sim_*` | From prepare step. |
| `platform` | yes | `parallel`, `twitter`, `reddit` | `parallel` = Twitter + Reddit. |
| `max_rounds` | no | int (default 20) | Cap to control LLM cost. 20 is a good default. |
| `force` | no | bool | `true` cleans old run logs/config (not profiles). **Always use `true` when re-running.** |
| `enable_graph_memory_update` | no | bool | Default `false`. |

Response: `process_pid`, `runner_status: "running"`, per-platform flags.

### Step 4 — Monitor progress

```bash
curl -s http://localhost:5001/api/simulation/sim_xxxx/run-status
```

Poll every 10-15 seconds (avoid tight loops — each round takes 30-90s due to
LLM calls). Watch:

| Field | Meaning |
|-------|---------|
| `runner_status` | Stays `"running"` until `/stop` is called (even after both platforms finish). |
| `twitter_completed` / `reddit_completed` | Individual completion flags. |
| `twitter_current_round` / `reddit_current_round` | Per-platform progress. |
| `progress_percent` | Overall — both platforms must reach 100%. |

**Typical timing:** Reddit finishes first (fewer actions per round). Twitter
takes longer. A 20-round parallel simulation runs ~15-30 minutes total.

### Step 5 — Stop the simulation

Once **both** `twitter_completed` and `reddit_completed` are `true`:

```bash
curl -s -X POST http://localhost:5001/api/simulation/stop \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxx"}'
```

This sets `runner_status: "stopped"` and the `completed_at` timestamp.
See §7-P2 if runner stays stuck at `"running"`.

### Step 6 — Inspect results

| Endpoint | Purpose |
|----------|---------|
| `GET /api/simulation/<sim_id>/posts?limit=N` | Full post content with text. **Preferred for text.** |
| `GET /api/simulation/<sim_id>/actions?limit=N` | Action log (types + agents, content often empty — see §7-P5). |
| `GET /api/simulation/<sim_id>/timeline` | Round-by-round timeline summary. |
| `GET /api/simulation/<sim_id>/agent-stats` | Per-agent action counts. |
| `GET /api/simulation/<sim_id>/comments?limit=N` | Comment content (Reddit). |

For raw data, parse the JSONL files at
`uploads/simulations/<sim_id>/{twitter,reddit}/actions.jsonl` — see
`references/actions-jsonl-format.md` for the event schema and a Python parsing
snippet.

### Step 7 — Generate the prediction report

> **Cost warning:** `/api/report/generate` makes LLM calls. Verify quota first
> (see §7-P3). A failed report wastes the task slot.

```bash
curl -s -X POST http://localhost:5001/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{
    "simulation_id": "sim_xxxx",
    "prediction_requirements": "Summarize key opinions, sentiment trends, and conclusions..."
  }'
```

Capture `task_id` from the response. Poll with `task_id` (NOT `report_id` — see
§7-P4):

```bash
curl -s -X POST http://localhost:5001/api/report/generate/status \
  -H "Content-Type: application/json" \
  -d '{"task_id": "<task_id>"}'
```

Status: `"generating"` → `"completed"` or `"failed"`. Poll every 5-10s. Once
completed, retrieve:

```bash
curl -s http://localhost:5001/api/report/<report_id>/download
curl -s http://localhost:5001/api/report/<report_id>/sections
```

### Step 8 — Deep interaction (optional)

```bash
# Chat with the report agent
curl -s -X POST http://localhost:5001/api/report/chat \
  -H "Content-Type: application/json" \
  -d '{"report_id": "report_xxxx", "message": "What was the dominant sentiment among teenagers?"}'

# Interview a specific agent
curl -s -X POST http://localhost:5001/api/simulation/interview \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxx", "agent_name": "Teenagers", "question": "How do you feel about the regulation bill?"}'

# Batch interview all agents
curl -s -X POST http://localhost:5001/api/simulation/interview/all \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxx"}'
```

For the full API surface (30+ routes), see `references/api-endpoint-map.md`.

---

## 6. Golden rules

1. **Backend as process principal.** Start with `exec uv run python run.py` in
   the backend dir. Do NOT wrap in `nohup` or `&` — child processes get cleaned
   up by the orchestrator. Run it as a background process.
2. **Health-check before anything else.** `curl http://localhost:5001/health`
   must return 200 before calling any API.
3. **Always `force: true` when re-running.** Cleans old logs and restarts fresh.
4. **Monitor both platforms separately.** `parallel` mode runs Twitter and
   Reddit independently; Twitter often finishes later. Check both
   `*_completed` flags.
5. **Call `/stop` after both platforms complete.** The runner status stays
   `"running"` even when both platforms show `completed=true`.
6. **Report generation costs LLM quota.** Verify quota before launching. Error
   messages may be in Chinese (e.g. `用户额度不足`) even if the provider is
   not Chinese — they can come from an upstream proxy.
7. **`generate/status` needs `task_id`, not `report_id`.** The status endpoint
   requires the `task_id` returned by `/generate`. `simulation_id` also works.
8. **Restart backend after `.env` changes.** `load_dotenv(override=True)` runs
   at import time, not per-request.

---

## 7. Pitfalls

### P1 — Backend dies silently after nohup
**Symptoms:** Health check fails; backend process not in `ps`.
**Cause:** `nohup … &` makes the orchestrator clean up child processes when
the wrapper terminates.
**Fix:** Use `exec uv run python run.py` as a background process. No
`nohup`, no `&`.
**Related:** §5-Step 1.

### P2 — Runner stuck at "running" after both platforms complete
**Symptoms:** `runner_status` stays `"running"` even when both platforms show
`completed=true`; no `completed_at` timestamp.
**Fix:** POST to `/api/simulation/stop` with the simulation_id.
**Related:** §5-Step 5.

### P3 — Report generation fails with a quota error
**Symptoms:** `/api/report/generate/status` returns `failed` with e.g.
`insufficient_user_quota` or `用户额度不足`.
**Cause:** The LLM provider (or its upstream proxy) is out of credit. The error
may name a different provider than the one in `.env` (the proxy forwards the
upstream error verbatim; each account has independent quota).
**Fix:** Diagnose directly:
```bash
source .env
curl -s -X POST "${LLM_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer $LLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"'"${LLM_MODEL_NAME}"'","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
```
Top up the proxy account or switch `LLM_BASE_URL` / `LLM_API_KEY` /
`LLM_MODEL_NAME`. Simulation data is NOT lost — regenerate the report later.
**Restart the backend** after editing `.env` (§6-Rule 8).
**Related:** §5-Step 7.

### P4 — generate/status rejects report_id
**Symptoms:** `/api/report/generate/status` with `{"report_id": "..."}`
returns `"请提供 task_id 或 simulation_id"`.
**Fix:** Use `"task_id"` (returned by `/generate`), not `"report_id"`.
`"simulation_id"` also works.
**Related:** §5-Step 7, §6-Rule 7.

### P5 — Actions API returns empty content
**Symptoms:** `/api/simulation/<sim_id>/actions` returns types and agent names
but blank content fields.
**Fix:** Use `/posts` for text, or read the raw JSONL files directly (see
`references/actions-jsonl-format.md`).
**Related:** §5-Step 6.

### P6 — Python version mismatch
**Symptoms:** Import errors, syntax errors, or `uv run` fails.
**Cause:** System Python is 3.13+ but MiroFish requires ≥3.11, ≤3.12.
**Fix:** The venv at `backend/.venv` was created with 3.12.x. Use `uv run`,
which uses the project venv. Do NOT recreate it with system Python 3.13+.
**Related:** §2.

### P7 — Port 5001 already in use
**Symptoms:** Backend fails to start with `Address already in use`.
**Fix:** Find and kill the stale process:
```bash
lsof -ti :5001 | xargs kill -9
```
Then restart the backend.

### P8 — Backend started but `.env` not loaded
**Symptoms:** LLM calls fail with auth errors; `LLM_API_KEY` not picked up.
**Cause:** `.env` file missing, or backend started before `.env` was created.
**Fix:** Ensure `.env` exists at project root, then restart the backend.
`load_dotenv(override=True)` runs only at import time.
**Related:** §2, §6-Rule 8.

---

## 8. Typical simulation dynamics

From a completed 20-round parallel simulation (subject: social media regulation
bill):

**Timeline:**
- **Rounds 1-9** — Warmup/graph-building; first actions start around round 10.
- **Round 10** — Initial wave: 6-8 agents publish opening posts (CREATE_POST),
  setting narrative frames.
- **Round 11** — Amplification: round-10 posts get quoted, reposted, liked;
  newcomers join. Expect 8-12 Twitter actions, 5-8 Reddit.
- **Round 12** — Riposte: institutional actors (Government, Big Tech) respond.
- **Rounds 13-20** — Diminishing returns; mostly DO_NOTHING or repeated likes.

**Platform differences:**
- Twitter: more volume (~23 actions), more action types (posts, reposts,
  quotes, likes).
- Reddit: fewer actions (~11), discussion-oriented (CREATE_POST +
  CREATE_COMMENT).

**Other observations:**
- Content language follows the seed material language.
- Most-replayed post: typically the most emotional framing; 5+ reposts/
  quotes/likes across rounds 11-12.
- `agents_count` in `simulation_start` may differ from agents that actually
  acted — not all agents act every round.

---

## 9. Verification

After a full run, verify:

1. `runner_status` is `"stopped"` (not `"running"`).
2. `completed_at` is set.
3. `total_actions_count` > 0.
4. Both `twitter_completed` and `reddit_completed` are `true`.
5. `actions.jsonl` files exist with line counts matching the action counts.
6. (If generated) report sections are retrievable.

---

## 10. Reference files

| File | Content |
|------|---------|
| `references/api-endpoint-map.md` | All 30+ routes across simulation, report, and graph blueprints. Key parameter references for `/start`, `/generate`, `/generate/status`. Raw artefact file locations. |
| `references/actions-jsonl-format.md` | Event types (`simulation_start`, `round_start`, `round_end`, `simulation_end`), action schema by type, parsing tips with Python snippet. |

---

## 11. Out of scope

- Setting up a fresh MiroFish installation from scratch.
- Configuring Zep Cloud or LLM provider keys.
- Building or modifying the frontend.
- Simulation preparation flow (`/prepare`, `/generate-profiles`,
  `/create`) — check preparation status (§5-Step 2), but if not prepared,
  ask the user to prepare it first.
- OASIS social media simulation internals (camel-ai library).
