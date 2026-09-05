# Graph Report - Razorpay  (2026-09-03)

## Corpus Check
- Corpus is ~44,089 words - fits in a single context window. You may not need a graph.

## Summary
- 268 nodes · 404 edges · 36 communities (34 shown, 2 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14

## God Nodes (most connected - your core abstractions)
1. `decide_action_node()` - 12 edges
2. `RecoveryState` - 12 edges
3. `classify_reason_node()` - 9 edges
4. `Dashboard()` - 9 edges
5. `run_batch_recovery()` - 8 edges
6. `Transaction` - 8 edges
7. `execute_retry_node()` - 7 edges
8. `BatchSummary` - 7 edges
9. `export_recovery_pdf()` - 6 edges
10. `reset_database_endpoint()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `save_recovery_attempt()` --uses--> `RecoveryState`  [INFERRED]
  backend/app/db/repositories/recovery_attempt_repo.py → backend/app/agents/state.py
- `build_recovery_graph()` --indirect_call--> `classify_reason_node()`  [INFERRED]
  backend/app/agents/graph.py → backend/app/agents/nodes/classify_reason.py
- `build_recovery_graph()` --indirect_call--> `decide_action_node()`  [INFERRED]
  backend/app/agents/graph.py → backend/app/agents/nodes/decide_action.py
- `build_recovery_graph()` --indirect_call--> `execute_retry_node()`  [INFERRED]
  backend/app/agents/graph.py → backend/app/agents/nodes/execute_retry.py
- `build_recovery_graph()` --uses--> `RecoveryState`  [INFERRED]
  backend/app/agents/graph.py → backend/app/agents/state.py

## Import Cycles
- None detected.

## Communities (36 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (31): api, downloadReportPDF(), getLatestSummary(), getRecoveryAttempts(), getReviewQueue(), getTransactionDetail(), injectPayments(), resolveReview() (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (33): build_recovery_graph(), classify_reason_node(), decide_action_node(), execute_retry_node(), RecoveryState, call_llm(), Mocked for now — in production this would trigger an SMS/WhatsApp/email with a…, Attempts to retry a failed payment in test mode. Razorpay doesn't have a direct… (+25 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (22): export_recovery_pdf(), get_latest_summary(), get_summary_history(), get, Returns the most recent batch summary — the dashboard headline numbers., All batch summaries over time — this powers your 'recovery maturing over runs'…, Generates and downloads the executive recovery PDF report., generate_transactions_endpoint() (+14 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (21): get_db(), Get the Supabase client instance., get_pending_review_queue(), list_recovery_attempts(), BaseModel, get, post, Runs the recovery flow for every transaction currently due (UI / manual… (+13 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (24): axios, date-fns, dependencies, axios, date-fns, react, react-dom, recharts (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (19): eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks (+11 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (13): Integration Tests for Razorpay RecoverAI APIs and Recovery Flow. Tests end-to-…, Verifies that the core API server starts and responds healthy., Verifies that synthetic failed payments can be injected., Verifies that batch recovery executes and returns a valid summary., Verifies that the summary headline and ROI metrics are returned correctly., Verifies that the PDF export endpoint returns valid application/pdf binary…, Verifies the Human-in-the-Loop review queue and manual approval flow., test_export_pdf_report_endpoint() (+5 more)

### Community 7 - "Community 7"
Cohesion: 0.31
Nodes (8): generate_mock_transactions(), main(), Database Seeding CLI Tool for Razorpay RecoverAI. Populates the Supabase…, Wipes all recovery attempts, transactions, and batch summaries., Generates synthetic failed transactions with realistic Indian pricing tiers., Seeds the Supabase database with mock transactions in batches., seed(), wipe_database()

### Community 8 - "Community 8"
Cohesion: 0.40
Nodes (5): Any, generate_transactions(), main(), Synthetic Transaction Generator Module & CLI Tool. Generates realistic payment…, Generates a list of synthetic failed payment payloads. Args: count: Number of…

### Community 9 - "Community 9"
Cohesion: 0.40
Nodes (5): client(), Generates a standard test state dictionary for agent node tests., Shared FastAPI test client for integration tests., sample_transaction_state(), fixture

### Community 10 - "Community 10"
Cohesion: 0.50
Nodes (4): main(), Time-Travel / Clock Simulation Utility for Recovery Schedules. Adjusts…, Shifts all future retry schedules backwards by `hours` to trigger retry queues.…, simulate_time_passing()

### Community 11 - "Community 11"
Cohesion: 0.67
Nodes (3): BatchSummaryOut, BaseModel, RunBatchResponse

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (3): Config, Settings, BaseSettings

## Knowledge Gaps
- **28 isolated node(s):** `Config`, `name`, `private`, `version`, `type` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RecoveryState` connect `Community 1` to `Community 3`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `run_batch_recovery()` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `decide_action_node()` (e.g. with `build_recovery_graph()` and `RecoveryState`) actually correct?**
  _`decide_action_node()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `RecoveryState` (e.g. with `build_recovery_graph()` and `classify_reason_node()`) actually correct?**
  _`RecoveryState` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `classify_reason_node()` (e.g. with `build_recovery_graph()` and `RecoveryState`) actually correct?**
  _`classify_reason_node()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `name`, `private` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.09254901960784313 - nodes in this community are weakly interconnected._