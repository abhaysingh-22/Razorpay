import { useEffect, useState } from "react";
import { getLatestSummary, getRecoveryAttempts, runRecoveryBatch } from "../api/endpoints";
import { BatchSummary, RecoveryAttempt } from "../types";
import { RecoveryMetricsCard } from "../components/dashboard/RecoveryMetricsCard";
import { RecoveryRateByReason } from "../components/dashboard/RecoveryRateByReason";
import { KeyHighlights } from "../components/dashboard/KeyHighlights";
import { AuditTrailTable } from "../components/dashboard/AuditTrailTable";
import { Button } from "../components/ui/Button";

export function Dashboard() {
  const [summary, setSummary] = useState<BatchSummary | null>(null);
  const [attempts, setAttempts] = useState<RecoveryAttempt[]>([]);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    const [s, a] = await Promise.all([getLatestSummary(), getRecoveryAttempts()]);
    setSummary(s);
    setAttempts(a);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunBatch = async () => {
    setLoading(true);
    await runRecoveryBatch();
    await loadData();
    setLoading(false);
  };

  const showEmptyState = summary === null;

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">AI Revenue Recovery</h1>
        <Button onClick={handleRunBatch} loading={loading}>Run Recovery Batch</Button>
      </div>

      {showEmptyState ? (
        <div className="p-8 text-center text-gray-400 border border-dashed border-gray-700 rounded-xl">
          No recovery batches run yet. Click "Run Recovery Batch" to start.
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <RecoveryMetricsCard summary={summary} />
            <KeyHighlights summary={summary} />
          </div>

          <RecoveryRateByReason summary={summary} />
          <AuditTrailTable attempts={attempts} />
        </>
      )}
    </div>
  );
}