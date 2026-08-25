import { BatchSummary } from "../../types";
import { Card } from "../ui/Card";

export function RecoveryMetricsCard({ summary }: { summary: BatchSummary }) {
  return (
    <Card>
      <p className="text-gray-400 text-sm mb-2">Revenue Recovered</p>
      <p className="text-4xl font-bold text-success">
        ₹{summary.total_amount_recovered.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
      </p>
      <p className="text-gray-400 mt-2">
        out of ₹{summary.total_amount_at_risk.toLocaleString("en-IN", { maximumFractionDigits: 0 })} at risk
        <span className="text-gray-200 font-semibold"> · {summary.recovery_rate}%</span>
      </p>
    </Card>
  );
}