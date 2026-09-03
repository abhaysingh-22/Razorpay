import { useEffect, useState } from "react";
import { getLatestSummary, getRecoveryAttempts, runRecoveryBatch, injectPayments, getReviewQueue, resolveReview, downloadReportPDF } from "../api/endpoints";
import { BatchSummary, RecoveryAttempt, Transaction } from "../types";
import { RecoveryMetricsCard } from "../components/dashboard/RecoveryMetricsCard";
import { RecoveryRateByReason } from "../components/dashboard/RecoveryRateByReason";
import { KeyHighlights } from "../components/dashboard/KeyHighlights";
import { AuditTrailTable } from "../components/dashboard/AuditTrailTable";
import { ROIMetricsWidget } from "../components/dashboard/ROIMetricsWidget";
import { PendingReviewsBanner } from "../components/dashboard/PendingReviewsBanner";
import { HITLReviewModal } from "../components/dashboard/HITLReviewModal";
import { UserGuideModal } from "../components/dashboard/UserGuideModal";
import { Button } from "../components/ui/Button";

export function Dashboard() {
  const [summary, setSummary] = useState<BatchSummary | null>(null);
  const [attempts, setAttempts] = useState<RecoveryAttempt[]>([]);
  const [pendingReviews, setPendingReviews] = useState<Transaction[]>([]);
  const [activeReviewTx, setActiveReviewTx] = useState<Transaction | null>(null);
  const [showGuide, setShowGuide] = useState(false);
  const [loading, setLoading] = useState(false);
  const [injecting, setInjecting] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [banner, setBanner] = useState<{ message: string; type: "success" | "info" } | null>(null);

  const loadData = async () => {
    try {
      const [s, a, q] = await Promise.all([getLatestSummary(), getRecoveryAttempts(), getReviewQueue()]);
      setSummary(s);
      setAttempts(a);
      setPendingReviews(q || []);
    } catch (err) {
      console.error("Failed to load dashboard data", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleInjectPayments = async () => {
    setInjecting(true);
    try {
      const res = await injectPayments(10);
      setBanner({
        type: "success",
        message: `⚡ Injected ${res.inserted || 10} synthetic failed payments into database. Ready to run recovery batch!`,
      });
      await loadData();
    } catch (err) {
      console.error("Failed to inject payments", err);
      setBanner({
        type: "info",
        message: "Failed to inject synthetic transactions. Check backend logs.",
      });
    } finally {
      setInjecting(false);
      setTimeout(() => setBanner(null), 6000);
    }
  };

  const handleRunBatch = async () => {
    setLoading(true);
    try {
      const res = await runRecoveryBatch();
      setBanner({
        type: "success",
        message: `🚀 Batch completed! Processed ${res.processed || 0} transactions through the LangGraph AI Recovery Engine.`,
      });
      await loadData();
    } catch (err) {
      console.error("Failed to run batch", err);
      setBanner({
        type: "info",
        message: "Error executing recovery batch.",
      });
    } finally {
      setLoading(false);
      setTimeout(() => setBanner(null), 6000);
    }
  };

  const handleResolveReview = async (transactionId: string, decision: "approve" | "reject", notes?: string) => {
    try {
      await resolveReview(transactionId, decision, notes);
      setBanner({
        type: "success",
        message: decision === "approve"
          ? "✅ Risk Officer approved payment recovery. Transaction recovered successfully!"
          : "🚫 Risk Officer confirmed fraud block. Transaction permanently escalated.",
      });
      await loadData();
    } catch (err) {
      console.error("Failed to resolve review", err);
      setBanner({
        type: "info",
        message: "Failed to submit review resolution.",
      });
    }
  };

  const handleExportPDF = async () => {
    setExporting(true);
    try {
      await downloadReportPDF();
      setBanner({
        type: "success",
        message: "📄 Executive PDF Report generated & downloaded successfully!",
      });
    } catch (err) {
      console.error("Failed to export PDF", err);
      setBanner({
        type: "info",
        message: "Failed to generate PDF report.",
      });
    } finally {
      setExporting(false);
      setTimeout(() => setBanner(null), 6000);
    }
  };

  const showEmptyState = summary === null;

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            RecoupAI
            <span className="text-xs bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 px-2 py-0.5 rounded-full font-medium">
              Payment Recovery Engine
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Autonomous multi-attempt payment recovery & real-time loss mitigation
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={handleExportPDF}
            loading={exporting}
            className="hover:border-slate-600 text-slate-300 hover:text-white"
          >
            📥 Export Report
          </Button>

          <Button
            variant="outline"
            onClick={() => setShowGuide(true)}
            className="hover:border-indigo-500 text-indigo-300 hover:text-indigo-200"
          >
            📖 Guide
          </Button>

          <Button
            variant="secondary"
            onClick={handleInjectPayments}
            loading={injecting}
            className="hover:border-emerald-500/50 text-emerald-400 hover:text-emerald-300"
          >
            ⚡ Inject 10 Payments
          </Button>

          <Button
            variant="primary"
            onClick={handleRunBatch}
            loading={loading}
          >
            ▶ Run Recovery Batch
          </Button>
        </div>
      </div>

      {/* Pending HITL Alert Banner */}
      <PendingReviewsBanner
        pendingList={pendingReviews}
        onOpenReview={(tx) => setActiveReviewTx(tx)}
      />

      {/* Flash Status Banner */}
      {banner && (
        <div
          className={`p-3 rounded-lg border text-sm flex items-center justify-between transition ${banner.type === "success"
            ? "bg-emerald-950/40 border-emerald-800/60 text-emerald-300"
            : "bg-slate-800 border-slate-700 text-slate-300"
            }`}
        >
          <span>{banner.message}</span>
          <button
            onClick={() => setBanner(null)}
            className="text-xs text-slate-400 hover:text-white ml-4 font-bold"
          >
            ✕
          </button>
        </div>
      )}

      {showEmptyState ? (
        <div className="p-12 text-center text-slate-400 border border-dashed border-slate-700 rounded-xl bg-slate-900/30 space-y-4">
          <div className="text-3xl">💳</div>
          <div className="font-semibold text-slate-200">No recovery data recorded yet</div>
          <p className="text-sm text-slate-400 max-w-md mx-auto">
            Click <strong>"Inject 10 Payments"</strong> to create simulated payment failures, then click <strong>"Run Recovery Batch"</strong> to watch the AI recovery lifecycle in action.
          </p>
          <div className="flex justify-center gap-3 pt-2">
            <Button variant="outline" onClick={() => setShowGuide(true)}>
              📖 Read User Guide
            </Button>
            <Button variant="secondary" onClick={handleInjectPayments} loading={injecting}>
              ⚡ Inject 10 Payments
            </Button>
            <Button variant="primary" onClick={handleRunBatch} loading={loading}>
              ▶ Run Recovery Batch
            </Button>
          </div>
        </div>
      ) : (
        <>
          {/* Executive ARR & ROI Widget */}
          <ROIMetricsWidget summary={summary} />

          {/* Core Metrics & Key Highlights */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <RecoveryMetricsCard summary={summary} />
            <KeyHighlights summary={summary} />
          </div>

          {/* Breakdown & Audit Trail */}
          <RecoveryRateByReason summary={summary} />
          <AuditTrailTable attempts={attempts} />
        </>
      )}

      {/* Human-in-the-Loop Review Modal */}
      {activeReviewTx && (
        <HITLReviewModal
          transaction={activeReviewTx}
          onClose={() => setActiveReviewTx(null)}
          onResolve={handleResolveReview}
        />
      )}

      {/* Interactive User Guide Modal */}
      {showGuide && (
        <UserGuideModal onClose={() => setShowGuide(false)} />
      )}
    </div>
  );
}