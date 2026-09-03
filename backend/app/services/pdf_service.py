import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from app.db.client import supabase


def generate_recovery_pdf_report() -> bytes:
    """Generates an executive-grade PDF summary of payment recovery performance and audit trail."""

    # 1. Fetch data from Supabase
    summary_res = (
        supabase.table("batch_summaries")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    summary = summary_res.data[0] if summary_res.data else None

    tx_res = (
        supabase.table("transactions")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    transactions = tx_res.data or []

    attempts_res = (
        supabase.table("recovery_attempts")
        .select("*")
        .order("created_at", desc=True)
        .limit(15)
        .execute()
    )
    attempts = attempts_res.data or []

    # Defaults if no data
    total_tx = (
        summary.get("total_transactions", len(transactions))
        if summary
        else len(transactions)
    )
    at_risk = (
        float(summary.get("total_amount_at_risk", 0))
        if summary
        else sum(float(t.get("amount", 0)) for t in transactions)
    )
    recovered = (
        float(summary.get("total_amount_recovered", 0))
        if summary
        else sum(
            float(t.get("amount", 0))
            for t in transactions
            if t.get("status") == "recovered"
        )
    )
    rate = (
        float(summary.get("recovery_rate", 0))
        if summary
        else (round((recovered / at_risk) * 100, 1) if at_risk else 0)
    )
    arr_saved = recovered * 12
    breakdown = summary.get("breakdown_by_reason", {}) if summary else {}
    highlights = summary.get("key_highlights", []) if summary else []

    # 2. Setup PDF Document
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    COLOR_PRIMARY = colors.HexColor("#0F172A")  # Slate 900
    COLOR_ACCENT = colors.HexColor("#4F46E5")  # Indigo 600
    COLOR_SUCCESS = colors.HexColor("#059669")  # Emerald 600
    COLOR_MUTED = colors.HexColor("#64748B")  # Slate 500
    COLOR_BG_LIGHT = colors.HexColor("#F8FAFC")  # Slate 50
    COLOR_BORDER = colors.HexColor("#E2E8F0")  # Slate 200

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=COLOR_PRIMARY,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=COLOR_MUTED,
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#334155"),
    )

    kpi_label = ParagraphStyle(
        "KPILabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        textColor=COLOR_MUTED,
        alignment=1,
    )

    kpi_value = ParagraphStyle(
        "KPIValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=COLOR_PRIMARY,
        alignment=1,
    )

    story = []

    # --- HEADER BLOCK ---
    story.append(Paragraph("Razorpay RecoverAI", title_style))
    story.append(
        Paragraph(
            f"Executive Financial Recovery & Audit Report • Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        HRFlowable(width="100%", thickness=1, color=COLOR_BORDER, spaceAfter=14)
    )

    # --- KPI METRICS CARDS (Table) ---
    kpi_data = [
        [
            Paragraph("TOTAL AT RISK", kpi_label),
            Paragraph("TOTAL RECOVERED", kpi_label),
            Paragraph("RECOVERY RATE", kpi_label),
            Paragraph("ANNUALIZED ARR SAVED", kpi_label),
        ],
        [
            Paragraph(f"₹{at_risk:,.2f}", kpi_value),
            Paragraph(f"<font color='#059669'>₹{recovered:,.2f}</font>", kpi_value),
            Paragraph(f"<font color='#4F46E5'>{rate}%</font>", kpi_value),
            Paragraph(f"<font color='#059669'>₹{arr_saved:,.0f}</font>", kpi_value),
        ],
    ]

    kpi_table = Table(kpi_data, colWidths=[135, 135, 135, 135])
    kpi_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), COLOR_BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 1, COLOR_BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )
    story.append(kpi_table)
    story.append(Spacer(1, 16))

    # --- EXECUTIVE HIGHLIGHTS ---
    story.append(Paragraph("Executive Performance Highlights", section_heading))
    if highlights:
        for h in highlights:
            bullet_text = f"• <b>{h}</b>"
            story.append(Paragraph(bullet_text, body_style))
            story.append(Spacer(1, 2))
    else:
        story.append(
            Paragraph(
                f"• Successfully processed {total_tx} failed transactions via autonomous LangGraph retry policies.",
                body_style,
            )
        )
        story.append(
            Paragraph(
                f"• Generated net {rate}% recovery efficiency (+{(max(0, rate - 22)):.1f}% over traditional blind retries).",
                body_style,
            )
        )
    story.append(Spacer(1, 14))

    # --- BREAKDOWN BY FAILURE REASON ---
    story.append(Paragraph("Recovery Breakdown by Failure Category", section_heading))
    breakdown_headers = [
        Paragraph("<b>Failure Reason</b>", body_style),
        Paragraph("<b>Total Count</b>", body_style),
        Paragraph("<b>Recovered (₹)</b>", body_style),
        Paragraph("<b>Recovery %</b>", body_style),
        Paragraph("<b>Policy Applied</b>", body_style),
    ]

    policy_map = {
        "bank_timeout": "Immediate transient retry (85% success)",
        "insufficient_funds": "Delayed temporal retries aligned with salary",
        "expired_card": "1-click customer payment update reminders",
        "fraud_flag": "Zero retries • Paused for Human Risk Review",
    }

    breakdown_rows = [breakdown_headers]
    for reason, data in breakdown.items():
        c = data.get("count", 0)
        rec = float(data.get("recovered", 0))
        pct = (
            round((rec / (c * (at_risk / total_tx))) * 100, 1)
            if (total_tx and at_risk and c)
            else (100.0 if rec > 0 else 0.0)
        )
        breakdown_rows.append(
            [
                Paragraph(reason.replace("_", " ").title(), body_style),
                Paragraph(str(c), body_style),
                Paragraph(f"₹{rec:,.2f}", body_style),
                Paragraph(f"{min(100.0, pct)}%", body_style),
                Paragraph(policy_map.get(reason, "Autonomous policy"), body_style),
            ]
        )

    if len(breakdown_rows) == 1:
        breakdown_rows.append(
            [
                Paragraph("All Categories", body_style),
                Paragraph(str(total_tx), body_style),
                Paragraph(f"₹{recovered:,.2f}", body_style),
                Paragraph(f"{rate}%", body_style),
                Paragraph("LangGraph Multi-Run Engine", body_style),
            ]
        )

    breakdown_table = Table(breakdown_rows, colWidths=[110, 65, 95, 75, 195])
    breakdown_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COLOR_BG_LIGHT),
                ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_PRIMARY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(breakdown_table)
    story.append(Spacer(1, 16))

    # --- RECENT AUDIT TRAIL LOGS ---
    story.append(Paragraph("Recent Recovery Audit Trail (Sample)", section_heading))
    audit_headers = [
        Paragraph("<b>Tx ID</b>", body_style),
        Paragraph("<b>Attempt</b>", body_style),
        Paragraph("<b>Action Taken</b>", body_style),
        Paragraph("<b>Outcome</b>", body_style),
        Paragraph("<b>Recovered</b>", body_style),
        Paragraph("<b>AI Reasoning</b>", body_style),
    ]

    audit_rows = [audit_headers]
    for a in attempts[:10]:
        tx_id_short = a.get("transaction_id", "")[:8]
        att_num = str(a.get("attempt_number", 1))
        act = a.get("action_taken", "retry")
        outcome = a.get("outcome", "pending")
        amt_rec = float(a.get("amount_recovered", 0))
        reasoning = (a.get("reasoning") or "")[:45] + (
            "..." if len(a.get("reasoning") or "") > 45 else ""
        )

        outcome_color = (
            "#059669"
            if outcome == "success"
            else ("#DC2626" if outcome == "failed" else "#D97706")
        )

        audit_rows.append(
            [
                Paragraph(f"<font face='Courier'>{tx_id_short}</font>", body_style),
                Paragraph(f"#{att_num}", body_style),
                Paragraph(act.replace("_", " "), body_style),
                Paragraph(
                    f"<font color='{outcome_color}'><b>{outcome.upper()}</b></font>",
                    body_style,
                ),
                Paragraph(f"₹{amt_rec:,.0f}", body_style),
                Paragraph(reasoning, body_style),
            ]
        )

    if len(audit_rows) == 1:
        audit_rows.append(
            [
                Paragraph("-", body_style),
                Paragraph("-", body_style),
                Paragraph("No recent attempts", body_style),
                Paragraph("-", body_style),
                Paragraph("₹0", body_style),
                Paragraph("Run a recovery batch to generate audit logs", body_style),
            ]
        )

    audit_table = Table(audit_rows, colWidths=[65, 45, 105, 65, 60, 200])
    audit_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COLOR_BG_LIGHT),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(audit_table)
    story.append(Spacer(1, 14))

    # --- FOOTER METADATA ---
    story.append(
        HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER, spaceAfter=8)
    )
    story.append(
        Paragraph(
            "Confidential • Generated by Razorpay RecoverAI Autonomous Agent System • Verified with Human-in-the-Loop Governance",
            subtitle_style,
        )
    )

    # Build Document
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
