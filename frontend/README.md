# 🎨 RecoupAI — Frontend Dashboard

A modern, responsive merchant dashboard for **RecoupAI**. Built with **React 19**, **TypeScript**, **Vite**, **TailwindCSS v4**, and **Recharts** to deliver real-time recovery analytics, interactive Human-in-the-Loop reviews, multi-run batch triggers, and instant executive PDF exports.

---

## 🌟 Key Features

1. **Headline Financial Metrics:**
   - Real-time **Recovery Rate (%)**, Total Amount at Risk, and Recovered Revenue.
   - **ROI Metrics Widget:** Calculates Annualized ARR Saved (`recovered × 12`), Penalty Fees Prevented from smart stopping rules, and Benchmark Uplift (3.2x vs. industry 22% baseline).
2. **Interactive Simulation Controls:**
   - **⚡ Inject 10 Payments:** Injects realistic payment failure scenarios into the backend.
   - **▶ Run Recovery Batch:** Triggers the LangGraph agent to process overdue transactions with temporal maturity.
   - **📄 Export PDF Report:** Direct binary download of an executive PDF report for stakeholders.
3. **Human-in-the-Loop (HITL) Review Modal:**
   - Surfaces alert banners when high-ticket (≥ ₹10,000) or fraud-flagged payments are paused.
   - Allows Risk Officers to review the AI agent's decision logic and click **[Approve Retry]** or **[Confirm Fraud Block]**.
4. **Transparent Audit Trail & Telemetry:**
   - Complete tabular breakdown of every recovery attempt, classified reason, action, and reasoning.
   - Visual breakdown chart of recovery rates across failure categories (Bank Timeout, Insufficient Funds, Expired Card, Fraud).
5. **Interactive In-App User Guide:**
   - Modal walkthrough guiding users through the 3-minute demo flow, UI glossary, and state machine architecture.

---

## 🏗️ Project Structure

```
frontend/src/
├── api/
│   ├── client.ts             # Axios instance with baseURL configuration
│   └── endpoints.ts          # Typed API query and mutation methods
├── components/
│   ├── dashboard/
│   │   ├── AuditTrailTable.tsx        # Granular attempt-by-attempt log
│   │   ├── HITLReviewModal.tsx        # Risk officer review & decision modal
│   │   ├── KeyHighlights.tsx          # Headline summary cards
│   │   ├── PendingReviewsBanner.tsx   # Urgent sign-off notification
│   │   ├── RecoveryMetricsCard.tsx    # Primary recovery rate stats
│   │   ├── RecoveryRateByReason.tsx   # Recharts failure distribution
│   │   ├── ROIMetricsWidget.tsx       # ARR saved & penalty fee metrics
│   │   └── UserGuideModal.tsx         # Embedded walkthrough & glossary
│   ├── transactions/                  # Transaction listing components
│   └── ui/                            # Reusable buttons, badges, modals
├── pages/
│   └── Dashboard.tsx                  # Main recovery control center
├── types/                             # TypeScript interfaces & API models
├── App.tsx                            # Root application entry
└── main.jsx                           # React DOM mount point
```

---

## 📦 Tech Stack

- **Framework:** React 19 + TypeScript
- **Bundler & Dev Server:** Vite 8
- **Styling:** TailwindCSS v4 with `@tailwindcss/vite`
- **Charts & Data Visualization:** Recharts 3
- **HTTP Client:** Axios
- **Date Utilities:** date-fns

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js 18+ (Node 20+ recommended)
- Running RecoupAI Backend API (locally on port `8000` or deployed on Render)

### 2. Environment Configuration
Create a `.env` file in the `frontend/` directory:
```bash
cp .env.example .env 2>/dev/null || touch .env
```

Add your backend API endpoint:
```ini
# Local backend
VITE_API_URL=http://localhost:8000/api/v1

# Or production deployed backend:
# VITE_API_URL=https://recoupai.onrender.com/api/v1
```

### 3. Installation
```bash
npm install
```

### 4. Running the Development Server
```bash
npm run dev
```
Open your browser at `http://localhost:5173`.

### 5. Building for Production
```bash
npm run build
npm run preview
```
---

## 🎯 3-Minute Demo Walkthrough

1. **Inject Data:** Click **⚡ Inject 10 Payments** in the header.
2. **Batch 1 (Instant Fixes):** Click **▶ Run Recovery Batch**. Bank timeouts will recover immediately (~35% recovery).
3. **Batch 2 (Temporal Maturity):** Click **▶ Run Recovery Batch** again. Second-attempt retries (salary dates, updated cards) resolve (~60% cumulative).
4. **Batch 3 (Stopping Rule):** Click **▶ Run Recovery Batch** a third time. Terminal stopping rules halt unrecoverable attempts (~75% final recovery).
5. **Human Review:** If the amber banner appears, click **Review Next** to inspect AI reasoning and approve/block the payment.
