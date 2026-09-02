import { useState } from "react";
import { Transaction } from "../../types";
import { Button } from "../ui/Button";

interface HITLReviewModalProps {
  transaction: Transaction | null;
  onClose: () => void;
  onResolve: (transactionId: string, decision: "approve" | "reject", notes?: string) => Promise<void>;
}

export function HITLReviewModal({ transaction, onClose, onResolve }: HITLReviewModalProps) {
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (!transaction) return null;

  const handleAction = async (decision: "approve" | "reject") => {
    setSubmitting(true);
    try {
      await onResolve(transaction.id, decision, notes);
      onClose();
    } catch (err) {
      console.error("Failed to resolve review", err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-lg rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex justify-between items-center bg-slate-800/40">
          <div className="flex items-center gap-2.5">
            <span className="p-2 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-xl text-lg">
              🛡️
            </span>
            <div>
              <h3 className="font-bold text-slate-100 text-base">Human-in-the-Loop Risk Review</h3>
              <p className="text-xs text-slate-400">Agent paused for manual compliance sign-off</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-lg font-bold p-1 rounded-lg hover:bg-slate-800 transition"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5">
          {/* Transaction Metadata Card */}
          <div className="grid grid-cols-2 gap-3 bg-slate-800/50 p-4 rounded-xl border border-slate-700/50 text-xs">
            <div>
              <span className="text-slate-400">Transaction ID:</span>
              <div className="font-mono text-slate-200 mt-0.5">{transaction.id.slice(0, 12)}...</div>
            </div>
            <div>
              <span className="text-slate-400">Amount at Risk:</span>
              <div className="font-bold text-emerald-400 text-sm mt-0.5">₹{transaction.amount.toLocaleString()}</div>
            </div>
            <div>
              <span className="text-slate-400">Customer ID:</span>
              <div className="font-mono text-slate-200 mt-0.5">{transaction.customer_id}</div>
            </div>
            <div>
              <span className="text-slate-400">Flagged Reason:</span>
              <div className="font-semibold text-amber-400 mt-0.5">{transaction.failure_reason}</div>
            </div>
          </div>

          {/* AI Risk Assessment */}
          <div className="bg-amber-950/20 border border-amber-800/40 p-4 rounded-xl space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider">
              <span>🤖</span> AI Diagnostic Assessment
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {transaction.failure_reason === "fraud_flag"
                ? "Transaction matches velocity fraud anomalies or gateway risk triggers. Automated retries were prevented to avoid chargeback penalties."
                : `High-value subscription charge (₹${transaction.amount.toLocaleString()}) paused for human verification before proceeding with automated retry rails.`}
            </p>
          </div>

          {/* Reviewer Notes Input */}
          <div className="space-y-1.5">
            <label className="text-xs font-medium text-slate-300">Reviewer Audit Notes (Optional)</label>
            <input
              type="text"
              placeholder="e.g. Verified customer KYC / IP matches address..."
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-5 border-t border-slate-800 bg-slate-800/30 flex justify-end gap-3">
          <Button
            variant="outline"
            onClick={() => handleAction("reject")}
            loading={submitting}
            className="hover:border-rose-500 hover:text-rose-400 text-rose-300"
          >
            🚫 Confirm Fraud Block
          </Button>
          <Button
            variant="success"
            onClick={() => handleAction("approve")}
            loading={submitting}
          >
            ✅ Approve Recovery Retry
          </Button>
        </div>
      </div>
    </div>
  );
}
