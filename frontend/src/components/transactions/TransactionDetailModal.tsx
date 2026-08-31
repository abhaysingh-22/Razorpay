import { useEffect, useState } from "react";
import { getTransactionDetail } from "../../api/endpoints";
import { Transaction, RecoveryAttempt } from "../../types";
import { Badge } from "../ui/Badge";

export function TransactionDetailModal({ id, onClose }: { id: string; onClose: () => void }) {
  const [data, setData] = useState<{ transaction: Transaction; recovery_attempts: RecoveryAttempt[] } | null>(null);

  useEffect(() => {
    getTransactionDetail(id).then(setData);
  }, [id]);

  if (!data) return null;

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 max-w-lg w-full" onClick={(e) => e.stopPropagation()}>
        <div className="flex justify-between items-start mb-4">
          <div>
            <p className="text-gray-400 text-sm">Transaction</p>
            <p className="font-mono text-sm">{data.transaction.id}</p>
          </div>
          <Badge status={data.transaction.status} />
        </div>
        <p className="text-2xl font-bold mb-4">₹{data.transaction.amount.toLocaleString("en-IN")}</p>
        <p className="text-gray-400 text-sm mb-2">Attempt history</p>
        <div className="space-y-3">
          {data.recovery_attempts.map((a) => (
            <div key={a.id} className="border-l-2 border-indigo-600 pl-3">
              <p className="text-sm">Attempt {a.attempt_number}: <Badge status={a.action_taken} /></p>
              <p className="text-xs text-gray-400 mt-1">{a.reasoning}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}