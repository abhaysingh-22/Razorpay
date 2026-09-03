# pyrefly: ignore [missing-import]
from fastapi import APIRouter

# pyrefly: ignore [missing-import]
from fastapi.responses import Response
from app.db.client import supabase
from app.services.pdf_service import generate_recovery_pdf_report

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary")
def get_latest_summary():
    """Returns the most recent batch summary — the dashboard headline numbers."""
    result = (
        supabase.table("batch_summaries")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if not result.data:
        return None
    summary = result.data[0]
    total_recovered = float(summary.get("total_amount_recovered") or 0)
    recovery_rate = float(summary.get("recovery_rate") or 0)
    summary["roi_metrics"] = {
        "recovered_arr": round(total_recovered * 12, 2),
        "penalty_fees_saved": 420,
        "traditional_rate": 22.0,
        "ai_rate": recovery_rate,
        "benchmark_uplift": f"{round(recovery_rate / 22.0, 1) if recovery_rate > 0 else 1.0}x",
    }
    return summary


@router.get("/history")
def get_summary_history(limit: int = 20):
    """All batch summaries over time — this powers your 'recovery maturing over runs' chart."""
    result = (
        supabase.table("batch_summaries")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data


@router.get("/export-pdf")
def export_recovery_pdf():
    """Generates and downloads the executive recovery PDF report."""
    pdf_bytes = generate_recovery_pdf_report()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=RecoverAI_Executive_Report.pdf"
        },
    )
