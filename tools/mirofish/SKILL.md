---
name: mirofish
description: Operate the MiroFish swarm-intelligence prediction engine locally — start the backend, prepare, launch, monitor, stop, and generate reports for multi-agent social simulations (Twitter/Reddit/parallel) via its Flask REST API. Use whenever the user mentions MiroFish, swarm simulation, agent prediction, or a sim_* ID.
---

# MiroFish — swarm simulation runner

Operate a MiroFish multi-agent social simulation end to end: start the Flask
backend, verify preparation, launch a run, monitor both platforms, stop it
cleanly, inspect the artefacts, and generate the prediction report.

---

## 1. When to use

- Launch, monitor, or stop a MiroFish multi-agent social simulation.
- Generate a prediction report from a completed simulation.
- Inspect simulation artefacts (actions, posts, timeline, agent stats).
- The user says "MiroFish", "swarm simulation", "agent prediction", or
  references a `sim_*` ID.

---

## 2. Prerequisites

MiroFish requires:

- Python ≥3.11, ≤3.12 (NOT 3.13+ — the venv must be 3.12.x).
- `uv` package manager.
- Node.js 18+ (frontend only; not needed for API-only operation).
- A `.env` file with `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL_NAME`, and
  `ZEP_API_KEY`. MiroFish uses any OpenAI-compatible endpoint; the default
  `.env` may point to a proxy (e.g. `api.example-proxy.com/v1`) wrapping a
  backend model. `LLMClient` reads `Config.LLM_BASE_URL` and
  `Config.LLM_MODEL_NAME` from `.env` with `override=True`, so `.env` wins.
- A prepared simulation (profiles + config already generated).

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

## 4. Golden rules

1. **Backend as process principal.** Start with `exec uv run python run.py` in
   the backend dir. Do NOT wrap in `nohup` or `&` — child processes get cleaned
   up by the orchestrator.
2. **Health-check before anything else.** `curl http://localhost:5001/health`
   must return 200 before calling any API.
3. **Always `force: true` when re-running.** If a simulation already has run
   artefacts, use `"force": true` on `/start` to clean old logs and restart
   fresh.
4. **Monitor both platforms.** `parallel` mode runs Twitter and Reddit
   independently; Twitter often finishes later. Check `twitter_completed` and
   `reddit_completed` separately.
5. **Call `/stop` after both platforms complete.** The runner status stays
   `"running"` even when both platforms show `completed=true`. POST to
   `/api/simulation/stop` to finalise and set `completed_at`.
6. **Report generation costs LLM quota.** `/api/report/generate` makes LLM calls
   via the configured provider. Verify quota before launching — a failed report
   wastes the task slot. Error messages may be in Chinese (e.g. `用户额度不足`)
   even if the provider is not Chinese — it can come from an upstream proxy.
7. **`generate/status` needs `task_id`, not `report_id`.** The status endpoint
   requires the `task_id` returned by `/generate`, not the `report_id`.

---

## 5. Workflow

### Step 1 — Start the backend

```bash
cd <mirofish-backend-dir>
exec uv run python run.py
```

Run as a background process (it's a Flask server). Verify after ~6-8 seconds:

```bash
curl -s http://localhost:5001/health --max-time 10
# Expect: {"service":"MiroFish Backend","status":"ok"}
```

### Step 2 — Verify the simulation is prepared

```bash
curl -s -X POST http://localhost:5001/api/simulation/prepare/status \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxx"}'
```

Look for `"status": "ready"` and `prepare_info.profiles_count > 0`.

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

Key parameters:

- `platform`: `"parallel"` (Twitter + Reddit), `"twitter"`, or `"reddit"`.
- `max_rounds`: cap to control LLM cost. 20 rounds is a good default.
- `force`: `true` cleans old run logs/config (not profiles or simulation_config).

The response returns `process_pid`, `runner_status: "running"`, and per-platform
flags.

### Step 4 — Monitor progress

```bash
curl -s http://localhost:5001/api/simulation/sim_xxxx/run-status
```

Poll every 10-15 seconds. Watch:

- `runner_status` → should stay `"running"` until both platforms done.
- `twitter_completed` / `reddit_completed` → individual completion flags.
- `twitter_current_round` / `reddit_current_round` → per-platform progress.
- `progress_percent` → overall (both platforms must reach 100%).

Reddit typically finishes first; Twitter takes longer per round.

### Step 5 — Stop the simulation

Once both platforms show `completed=true`:

```bash
curl -s -X POST http://localhost:5001/api/simulation/stop \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxx"}'
```

This sets `runner_status: "stopped"` and the `completed_at` timestamp.

### Step 6 — Inspect results

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/simulation/<sim_id>/actions?limit=N` | GET | Action log (CREATE_POST, REPOST, LIKE_POST, QUOTE_POST...) |
| `/api/simulation/<sim_id>/posts?limit=N` | GET | Full post content with text |
| `/api/simulation/<sim_id>/timeline` | GET | Round-by-round timeline summary |
| `/api/simulation/<sim_id>/agent-stats` | GET | Per-agent action counts |
| `/api/simulation/<sim_id>/comments?limit=N` | GET | Comment content |

Note: the `actions` endpoint returns types and agent names but content fields are
often empty. Use `posts` for actual text, or read the raw JSONL files at
`uploads/simulations/<sim_id>/{twitter,reddit}/actions.jsonl`.

### Step 7 — Generate the prediction report

```bash
curl -s -X POST http://localhost:5001/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{
    "simulation_id": "sim_xxxx",
    "prediction_requirements": "Summarize key opinions, sentiment trends, and conclusions..."
  }'
```

Capture `task_id` from the response, then poll:

```bash
curl -s -X POST http://localhost:5001/api/report/generate/status \
  -H "Content-Type: application/json" \
  -d '{"task_id": "<task_id>"}'
```

Status flows: `"generating"` → `"completed"` or `"failed"`. Once completed:

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
```

---

## 6. Pitfalls

### P1 — Backend dies silently after nohup
**Problem:** starting with `nohup … &` makes the orchestrator clean up child
processes when the wrapper terminates, killing the Flask server.
**Fix:** use `exec uv run python run.py` (no nohup, no `&`).

### P2 — Runner stuck at "running" after both platforms complete
**Problem:** `runner_status` stays `"running"` even when both platforms show
`completed=true`; no `completed_at` timestamp.
**Fix:** POST to `/api/simulation/stop` with the simulation_id.

### P3 — Report generation fails with a quota error
**Problem:** `/api/report/generate/status` returns `failed` with e.g.
`insufficient_user_quota` or `用户额度不足`.
**Fix:** the LLM provider (or its upstream proxy) is out of credit. The error
may name a *different* provider than the one in `.env` (the proxy forwards the
upstream error verbatim; each account has independent quota). Diagnose directly:

```bash
source .env
curl -s -X POST "${LLM_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer $LLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"'"${LLM_MODEL_NAME}"'","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
```

Top up the proxy account or switch `LLM_BASE_URL` / `LLM_API_KEY` /
`LLM_MODEL_NAME`. Simulation data is NOT lost — regenerate the report later.
**You MUST restart the backend** after editing `.env`: `load_dotenv(override=True)`
runs once at import time in `config.py`, not per-request.

### P4 — generate/status rejects report_id
**Problem:** `/api/report/generate/status` with `{"report_id": "..."}` returns
`"请提供 task_id 或 simulation_id"`.
**Fix:** use `"task_id"` (returned by `/generate`), not `"report_id"`.
`"simulation_id"` also works.

### P5 — Actions API returns empty content
**Problem:** `/api/simulation/<sim_id>/actions` returns types and agent names
but blank content fields.
**Fix:** use `/posts` for text, or read the raw JSONL files directly.

### P6 — Python version mismatch
**Problem:** system Python is 3.13+ but MiroFish requires ≥3.11, ≤3.12.
**Fix:** the venv at `backend/.venv` was created with 3.12.x. Use `uv run`, which
uses the project venv. Do NOT recreate it with system Python 3.13+.

---

## 7. Typical simulation dynamics

From a completed 20-round parallel simulation (subject: social media regulation
bill):

- **Rounds 1-9** — warmup/graph-building; first actions typically start around
  round 10.
- **Round 10** — initial wave: 6-8 agents publish opening posts (CREATE_POST),
  setting the narrative frames.
- **Round 11** — amplification: round-10 posts get quoted, reposted, liked;
  newcomers join. Expect 8-12 Twitter actions, 5-8 Reddit.
- **Round 12** — riposte: institutional actors (Government, Big Tech) respond.
- **Rounds 13-20** — diminishing returns; mostly DO_NOTHING or repeated likes.
- **Twitter vs Reddit** — Twitter has more volume (23 vs 11) and more action
  types; Reddit is discussion-oriented (CREATE_POST + CREATE_COMMENT).
- **Content language** — the seed material language determines output language.
- **Most-replayed post** — typically the most emotional framing; 5+ reposts/
  quotes/likes across rounds 11-12.
- **agent_count discrepancy** — `simulation_start` may report 13 agents while
  only 12 appear in action stats; not all agents act every round.

---

## 8. Verification

After a full run, verify:

1. `runner_status` is `"stopped"` (not `"running"`).
2. `completed_at` is set.
3. `total_actions_count` > 0.
4. Both `twitter_completed` and `reddit_completed` are `true`.
5. `actions.jsonl` files exist with line counts matching the action counts.
6. (If generated) report sections are retrievable.

---

## 9. Reference files

- `references/api-endpoint-map.md` — all 30+ routes across simulation, report,
  and graph blueprints.
- `references/actions-jsonl-format.md` — event types, `action_args` schema,
  parsing tips.

---

## 10. Out of scope

- Setting up a fresh MiroFish installation from scratch.
- Configuring Zep Cloud or LLM provider keys.
- Building or modifying the frontend.
- Custom entity/persona generation (covered by the `prepare` flow).
- OASIS social media simulation internals (camel-ai library).
