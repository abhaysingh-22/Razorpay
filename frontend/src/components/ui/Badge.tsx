const statusColors: Record<string, string> = {
  recovered: "bg-success/20 text-success",
  awaiting_customer_action: "bg-warning/20 text-warning",
  escalated: "bg-danger/20 text-danger",
  exhausted: "bg-gray-700 text-gray-300",
  failed: "bg-gray-700 text-gray-300",
};

export function Badge({ status }: { status: string }) {
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[status] || "bg-gray-700 text-gray-300"}`}>
      {status.replace(/_/g, " ")}
    </span>
  );
}