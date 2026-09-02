import { Transaction } from "../../types";
import { Button } from "../ui/Button";

interface PendingReviewsBannerProps {
  pendingList: Transaction[];
  onOpenReview: (tx: Transaction) => void;
}

export function PendingReviewsBanner({ pendingList, onOpenReview }: PendingReviewsBannerProps) {
  if (!pendingList || pendingList.length === 0) return null;

  return (
    <div className="bg-gradient-to-r from-amber-950/40 via-amber-900/20 to-slate-900 border border-amber-500/40 p-4 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-lg shadow-amber-950/20">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-lg text-amber-400">
          ⚠️
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-100 text-sm">
              {pendingList.length} Payment{pendingList.length > 1 ? "s" : ""} Awaiting Risk Sign-Off
            </span>
            <span className="text-[10px] bg-amber-500/20 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded-full font-bold uppercase tracking-wider animate-pulse">
              Action Required
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Agent paused execution on high-risk/high-value transactions pending Human-in-the-Loop review.
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2 w-full sm:w-auto">
        <Button
          variant="secondary"
          onClick={() => onOpenReview(pendingList[0])}
          className="w-full sm:w-auto bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border-amber-500/40"
        >
          🛡️ Review Next ({pendingList.length} pending)
        </Button>
      </div>
    </div>
  );
}
