import { useState } from "react";

interface UserGuideModalProps {
  onClose: () => void;
}

export function UserGuideModal({ onClose }: UserGuideModalProps) {
  const [activeTab, setActiveTab] = useState<"testing" | "glossary" | "architecture">("testing");

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-3xl max-h-[90vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex justify-between items-center bg-slate-800/40">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-xl text-indigo-400">
              📖
            </div>
            <div>
              <h2 className="font-bold text-slate-100 text-lg flex items-center gap-2">
                RecoverAI User Guide & UI Walkthrough
              </h2>
              <p className="text-xs text-slate-400">
                How to test the application and understand every dashboard metric
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-lg font-bold p-1.5 rounded-lg hover:bg-slate-800 transition cursor-pointer"
          >
            ✕
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800 bg-slate-950/40 px-5 pt-2 gap-2 text-xs font-semibold">
          <button
            onClick={() => setActiveTab("testing")}
            className={`pb-2.5 px-3 border-b-2 transition cursor-pointer ${
              activeTab === "testing"
                ? "border-indigo-500 text-indigo-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            🚀 How to Test (3-Minute Demo)
          </button>
          <button
            onClick={() => setActiveTab("glossary")}
            className={`pb-2.5 px-3 border-b-2 transition cursor-pointer ${
              activeTab === "glossary"
                ? "border-indigo-500 text-indigo-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            💡 What Means What in UI
          </button>
          <button
            onClick={() => setActiveTab("architecture")}
            className={`pb-2.5 px-3 border-b-2 transition cursor-pointer ${
              activeTab === "architecture"
                ? "border-indigo-500 text-indigo-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            ⚙️ How the Agent Works
          </button>
        </div>

        {/* Scrollable Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-300 text-sm">
          {/* TAB 1: HOW TO TEST */}
          {activeTab === "testing" && (
            <div className="space-y-4">
              <div className="p-3.5 bg-indigo-950/30 border border-indigo-500/30 rounded-xl text-xs text-indigo-200">
                <strong>🎯 Quick Pitch for Judges/Interviewers:</strong> "Traditional systems either blindly retry failed payments (wasting bank fees) or lose revenue entirely. RecoverAI uses LangGraph agents to diagnose failure reasons, apply smart timing policies, and recover up to ~75% of lost revenue."
              </div>

              <div className="space-y-3">
                {/* Step 1 */}
                <div className="p-4 bg-slate-800/40 border border-slate-700/60 rounded-xl flex gap-3.5 items-start">
                  <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                    1
                  </span>
                  <div>
                    <h4 className="font-bold text-slate-100 text-sm">Inject Failed Payments</h4>
                    <p className="text-xs text-slate-400 mt-1">
                      Click <strong className="text-emerald-400">⚡ Inject 10 Payments</strong> in the top header. This randomly creates 10 realistic failed payment scenarios (insufficient funds, expired card, bank timeout, or fraud) in your database.
                    </p>
                  </div>
                </div>

                {/* Step 2 */}
                <div className="p-4 bg-slate-800/40 border border-slate-700/60 rounded-xl flex gap-3.5 items-start">
                  <span className="w-6 h-6 rounded-full bg-indigo-500/20 text-indigo-400 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                    2
                  </span>
                  <div>
                    <h4 className="font-bold text-slate-100 text-sm">Run 1st Recovery Batch (Instant Fixes)</h4>
                    <p className="text-xs text-slate-400 mt-1">
                      Click <strong className="text-indigo-400">▶ Run Recovery Batch</strong>.
                    </p>
                    <ul className="text-xs text-slate-400 mt-1 list-disc list-inside space-y-0.5">
                      <li>Bank timeouts recover immediately (transient fix).</li>
                      <li>Insufficient funds get scheduled for Attempt 2 (waiting for salary credit).</li>
                      <li>Expired cards send customer update reminders.</li>
                      <li><strong>Expected result:</strong> ~35% recovery rate.</li>
                    </ul>
                  </div>
                </div>

                {/* Step 3 */}
                <div className="p-4 bg-slate-800/40 border border-slate-700/60 rounded-xl flex gap-3.5 items-start">
                  <span className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                    3
                  </span>
                  <div>
                    <h4 className="font-bold text-slate-100 text-sm">Run 2nd Recovery Batch (Temporal Resolution)</h4>
                    <p className="text-xs text-slate-400 mt-1">
                      Click <strong className="text-indigo-400">▶ Run Recovery Batch</strong> a second time.
                    </p>
                    <ul className="text-xs text-slate-400 mt-1 list-disc list-inside space-y-0.5">
                      <li>The agent processes 2nd attempts (simulating salary deposits & customers updating their cards).</li>
                      <li><strong>Expected result:</strong> Cumulative recovery climbs to ~60%.</li>
                    </ul>
                  </div>
                </div>

                {/* Step 4 */}
                <div className="p-4 bg-slate-800/40 border border-slate-700/60 rounded-xl flex gap-3.5 items-start">
                  <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                    4
                  </span>
                  <div>
                    <h4 className="font-bold text-slate-100 text-sm">Run 3rd Recovery Batch (Stopping Rule)</h4>
                    <p className="text-xs text-slate-400 mt-1">
                      Click <strong className="text-indigo-400">▶ Run Recovery Batch</strong> a third time.
                    </p>
                    <ul className="text-xs text-slate-400 mt-1 list-disc list-inside space-y-0.5">
                      <li>Final retries resolve; remaining unrecoverable cases are safely stopped (marked "exhausted").</li>
                      <li><strong>Expected result:</strong> Overall recovery reaches ~75%.</li>
                    </ul>
                  </div>
                </div>

                {/* Step 5 */}
                <div className="p-4 bg-slate-800/40 border border-slate-700/60 rounded-xl flex gap-3.5 items-start">
                  <span className="w-6 h-6 rounded-full bg-rose-500/20 text-rose-400 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                    5
                  </span>
                  <div>
                    <h4 className="font-bold text-slate-100 text-sm">Human-in-the-Loop Risk Review</h4>
                    <p className="text-xs text-slate-400 mt-1">
                      If an amber banner appears (<strong className="text-amber-400">⚠️ Payments Awaiting Risk Sign-Off</strong>), click <strong>"Review Next"</strong> to inspect the AI's risk explanation and click <strong>[Approve Retry]</strong> or <strong>[Confirm Fraud Block]</strong>.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: UI GLOSSARY */}
          {activeTab === "glossary" && (
            <div className="space-y-4">
              <p className="text-xs text-slate-400">
                Here is a simple explanation of every section and number you see on the dashboard:
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div className="p-3.5 bg-slate-800/50 border border-slate-700/60 rounded-xl space-y-1">
                  <div className="font-bold text-emerald-400 text-xs flex items-center gap-1.5">
                    <span>📈</span> Annualized ARR Saved
                  </div>
                  <p className="text-xs text-slate-300">
                    Calculates the yearly subscription revenue saved from involuntary churn (<code className="text-emerald-300 font-mono">recovered_revenue × 12</code>).
                  </p>
                </div>

                <div className="p-3.5 bg-slate-800/50 border border-slate-700/60 rounded-xl space-y-1">
                  <div className="font-bold text-indigo-400 text-xs flex items-center gap-1.5">
                    <span>🛡️</span> Penalty Fees Prevented
                  </div>
                  <p className="text-xs text-slate-300">
                    Banks charge ₹15–₹25 per bounced card retry. Our stopping rules eliminate blind retries on dead cards, saving processing fees.
                  </p>
                </div>

                <div className="p-3.5 bg-slate-800/50 border border-slate-700/60 rounded-xl space-y-1">
                  <div className="font-bold text-purple-400 text-xs flex items-center gap-1.5">
                    <span>⚡</span> 3.2x Efficiency Uplift
                  </div>
                  <p className="text-xs text-slate-300">
                    Compares RecoverAI (~73% recovery) against standard industry blind retry algorithms (~22% fixed benchmark).
                  </p>
                </div>

                <div className="p-3.5 bg-slate-800/50 border border-slate-700/60 rounded-xl space-y-1">
                  <div className="font-bold text-amber-400 text-xs flex items-center gap-1.5">
                    <span>⚠️</span> Human-in-the-Loop Queue
                  </div>
                  <p className="text-xs text-slate-300">
                    High-ticket (≥ ₹10,000) or fraud-flagged transactions are automatically paused for human compliance sign-off.
                  </p>
                </div>
              </div>

              <div className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-xl space-y-2">
                <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider">The 4 Failure Categories</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div className="p-2 bg-slate-800/70 rounded-lg">
                    <strong className="text-slate-200">1. Bank Timeout:</strong> Temporary network drop. 100% safe to retry right away.
                  </div>
                  <div className="p-2 bg-slate-800/70 rounded-lg">
                    <strong className="text-slate-200">2. Insufficient Funds:</strong> Valid card, low balance. Delayed retry for salary days.
                  </div>
                  <div className="p-2 bg-slate-800/70 rounded-lg">
                    <strong className="text-slate-200">3. Expired Card:</strong> Card is dead. Notifies customer to update card info.
                  </div>
                  <div className="p-2 bg-slate-800/70 rounded-lg">
                    <strong className="text-slate-200">4. Fraud Flag:</strong> Suspicious activity. Blocks all retries immediately.
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: AGENT ARCHITECTURE */}
          {activeTab === "architecture" && (
            <div className="space-y-4">
              <p className="text-xs text-slate-400">
                How the underlying LangGraph state machine processes transactions under the hood:
              </p>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl font-mono text-xs text-slate-300 space-y-2">
                <div className="text-indigo-400 font-bold">[1] Entry: Raw Payment Failure</div>
                <div className="pl-4 text-slate-400">↓ Passes raw gateway error code to classify_reason_node</div>
                <div className="text-emerald-400 font-bold">[2] Classify Reason (LLM via Groq)</div>
                <div className="pl-4 text-slate-400">↓ Normalizes error to: insufficient_funds | expired_card | bank_timeout | fraud_flag</div>
                <div className="text-purple-400 font-bold">[3] Decide Recovery Policy (LLM Decision Engine)</div>
                <div className="pl-4 text-slate-400">↓ Evaluates attempt count (1, 2, 3) & business policy rules</div>
                <div className="text-amber-400 font-bold">[4] Execution & Safety Gate</div>
                <div className="pl-4 text-slate-400">↓ If fraud / high-ticket → pauses in pending_human_review</div>
                <div className="pl-4 text-slate-400">↓ If retry valid → executes attempt & updates PostgreSQL audit trail</div>
              </div>

              <div className="p-3.5 bg-slate-800/40 border border-slate-700/60 rounded-xl text-xs text-slate-300">
                <strong>💡 Resetting the System:</strong> Whenever you want to wipe the database clean and start a brand-new demo run, simply visit <a href="http://localhost:8000/reset" target="_blank" rel="noreferrer" className="text-indigo-400 underline font-mono">http://localhost:8000/reset</a> in your browser.
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-800/30 flex justify-end">
          <button
            onClick={onClose}
            className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition cursor-pointer shadow-sm"
          >
            Got It! Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
