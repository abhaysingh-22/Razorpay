import { RecoveryAttempt } from "../../types";
import { Card } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { format } from "date-fns";

export function AuditTrailTable({ attempts }: { attempts: RecoveryAttempt[] }) {
  return (
    <Card>
      <p className="text-gray-400 text-sm mb-4">Audit Trail</p>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-gray-800">
              <th className="pb-2">Transaction</th>
              <th className="pb-2">Attempt</th>
              <th className="pb-2">Action</th>
              <th className="pb-2">Reasoning</th>
              <th className="pb-2">Outcome</th>
              <th className="pb-2">Time</th>
            </tr>
          </thead>
          <tbody>
            {attempts.map((a) => (
              <tr key={a.id} className="border-b border-gray-900">
                <td className="py-2 text-gray-400 font-mono text-xs">{a.transaction_id.slice(0, 8)}</td>
                <td className="py-2">{a.attempt_number}</td>
                <td className="py-2"><Badge status={a.action_taken} /></td>
                <td className="py-2 text-gray-400 max-w-xs truncate">{a.reasoning}</td>
                <td className="py-2">{a.outcome}</td>
                <td className="py-2 text-gray-500 text-xs">{format(new Date(a.created_at), "MMM d, HH:mm")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}