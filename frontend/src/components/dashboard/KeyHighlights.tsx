import { BatchSummary } from "../../types";
import { Card } from "../ui/Card";

export function KeyHighlights({ summary }: { summary: BatchSummary }) {
  return (
    <Card>
      <p className="text-gray-400 text-sm mb-3">Key Highlights</p>
      <ul className="space-y-2">
        {summary.key_highlights.map((h, i) => (
          <li key={i} className="text-sm text-gray-200 flex gap-2">
            <span className="text-indigo-400">•</span> {h}
          </li>
        ))}
      </ul>
      {summary.exceptions.length > 0 && (
        <>
          <p className="text-gray-400 text-sm mt-4 mb-2">Exceptions</p>
          <ul className="space-y-1">
            {summary.exceptions.map((e, i) => (
              <li key={i} className="text-xs text-gray-500">{e}</li>
            ))}
          </ul>
        </>
      )}
    </Card>
  );
}