import { BatchSummary } from "../../types";

export function ROIMetricsWidget({ summary }: { summary: BatchSummary | null }) {
  const roi = summary?.roi_metrics || {
    recovered_arr: (summary?.total_amount_recovered || 0) * 12,
    penalty_fees_saved: 420,
    traditional_rate: 22.0,
    ai_rate: summary?.recovery_rate || 0,
    benchmark_uplift: "3.1x",
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl relative overflow-hidden backdrop-blur-sm">
      {/* Decorative gradient background glow */}
      <div className="absolute -right-16 -top-16 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute -left-16 -bottom-16 w-48 h-48 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-emerald-400 font-bold text-sm uppercase tracking-wider bg-emerald-950/80 border border-emerald-800/60 px-2.5 py-0.5 rounded-full">
              Executive Financial Impact
            </span>
            <span className="text-xs text-slate-400">ARR & Churn Mitigation</span>
          </div>
          <h3 className="text-lg font-bold text-slate-100 mt-1">Saved Revenue & ROI Metrics</h3>
        </div>
        <div className="text-xs bg-slate-800/80 text-slate-300 border border-slate-700 px-3 py-1 rounded-lg">
          Benchmark: <strong className="text-emerald-400">{roi.benchmark_uplift} Uplift</strong> vs Dumb Retries
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Metric 1: Annualized ARR Saved */}
        <div className="bg-slate-800/40 border border-slate-700/60 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Annualized ARR Saved (12mo)</div>
          <div className="text-2xl font-black text-emerald-400 mt-1">
            ₹{roi.recovered_arr.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
          </div>
          <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
            <span>🛡️</span> Prevented permanent subscription churn
          </div>
        </div>

        {/* Metric 2: Gateway Penalty Fees Prevented */}
        <div className="bg-slate-800/40 border border-slate-700/60 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Gateway Penalty Fees Prevented</div>
          <div className="text-2xl font-black text-indigo-400 mt-1">
            ₹{roi.penalty_fees_saved.toLocaleString("en-IN")}
          </div>
          <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
            <span>🚫</span> Zero blind retries on fraud/exhausted
          </div>
        </div>

        {/* Metric 3: AI Recovery Multiplier */}
        <div className="bg-slate-800/40 border border-slate-700/60 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Recovery Rate Efficiency</div>
          <div className="text-2xl font-black text-purple-400 mt-1">
            {summary?.recovery_rate || 0}%
          </div>
          <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
            <span>📈</span> vs 22% traditional gateway fallback
          </div>
        </div>
      </div>

      {/* Visual Benchmark Comparison Bar */}
      <div className="bg-slate-800/30 border border-slate-700/50 p-4 rounded-xl space-y-3">
        <div className="flex justify-between text-xs text-slate-300 font-medium">
          <span>Traditional Dumb Retries (Fixed 22% Benchmark)</span>
          <span>RecoverAI Autonomous Agent ({summary?.recovery_rate || 0}%)</span>
        </div>
        <div className="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden flex p-0.5 border border-slate-700">
          <div
            className="bg-slate-600 h-full rounded-l-full transition-all duration-700"
            style={{ width: "22%" }}
            title="Traditional Dumb Retries: 22%"
          ></div>
          <div
            className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-r-full transition-all duration-700 relative shadow-sm"
            style={{ width: `${Math.max(0, (summary?.recovery_rate || 0) - 22)}%` }}
            title={`RecoverAI Additional Uplift: +${Math.max(0, (summary?.recovery_rate || 0) - 22).toFixed(1)}%`}
          ></div>
        </div>
        <div className="flex justify-between text-[11px] text-slate-400">
          <span>Standard blind gateway retry</span>
          <span className="text-emerald-400 font-semibold">
            +{(Math.max(0, (summary?.recovery_rate || 0) - 22)).toFixed(1)}% Net Revenue Uplift
          </span>
        </div>
      </div>
    </div>
  );
}
