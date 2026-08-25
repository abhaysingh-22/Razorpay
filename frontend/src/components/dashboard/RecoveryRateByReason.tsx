import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { BatchSummary } from "../../types";
import { Card } from "../ui/Card";

export function RecoveryRateByReason({ summary }: { summary: BatchSummary }) {
  const data = Object.entries(summary.breakdown_by_reason).map(([reason, stats]) => ({
    reason: reason.replace(/_/g, " "),
    count: stats.count,
    recovered: stats.recovered,
  }));

  return (
    <Card>
      <p className="text-gray-400 text-sm mb-4">Recovery by Failure Reason</p>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <XAxis dataKey="reason" stroke="#9ca3af" fontSize={12} />
          <YAxis stroke="#9ca3af" fontSize={12} />
          <Tooltip contentStyle={{ background: "#111827", border: "1px solid #374151" }} />
          <Bar dataKey="count" fill="#4b5563" name="Total" />
          <Bar dataKey="recovered" fill="#16a34a" name="Recovered ₹" />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}