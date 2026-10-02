#!/usr/bin/env python3
"""
Academic PDF Generator for PES University SE Lab Submissions
Student: Mudit Chaturvedi (SRN: PES1UG24CS279)
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image
)

ROOT = Path("/Users/manojkumarchaturvedi/MyProject_MicroLending")

NAVY = HexColor("#0B3D91")
GREY = HexColor("#333333")
LIGHT_BG = HexColor("#F4F8FD")
BORDER_COLOR = HexColor("#B0C4DE")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle", parent=styles["Title"], fontSize=18, leading=23, textColor=NAVY, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name="DocSub", parent=styles["Normal"], fontSize=10, leading=14, alignment=TA_CENTER, textColor=GREY, spaceAfter=3))
styles.add(ParagraphStyle(name="SecH1", parent=styles["Heading2"], fontSize=13, leading=17, textColor=NAVY, spaceBefore=12, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name="SecH2", parent=styles["Heading3"], fontSize=11, leading=15, textColor=HexColor("#1F4E79"), spaceBefore=8, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyTextJ", parent=styles["Normal"], fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY, textColor=GREY, spaceAfter=5))
styles.add(ParagraphStyle(name="TableHead", parent=styles["Normal"], fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=HexColor("#FFFFFF"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TableCell", parent=styles["Normal"], fontSize=8, leading=10.5, textColor=GREY))
styles.add(ParagraphStyle(name="TableCellBold", parent=styles["Normal"], fontSize=8, leading=10.5, fontName="Helvetica-Bold", textColor=NAVY))
styles.add(ParagraphStyle(name="QuoteBox", parent=styles["Normal"], fontSize=10, leading=14, fontName="Helvetica-BoldOblique", textColor=NAVY, alignment=TA_CENTER))


def header_footer(canvas, doc):
    canvas.saveState()
    # Top header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 10 * mm, A4[0], 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#FFFFFF"))
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(14 * mm, A4[1] - 7 * mm, "PES University | Department of Computer Science & Engineering")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(A4[0] - 14 * mm, A4[1] - 7 * mm, "Mudit Chaturvedi (PES1UG24CS279)")

    # Bottom footer bar
    canvas.setFillColor(HexColor("#EBF3FB"))
    canvas.rect(0, 0, A4[0], 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(14 * mm, 3.5 * mm, "Problem Statement #33 — Micro-Lending & Peer Credit Risk Assessor")
    canvas.drawRightString(A4[0] - 14 * mm, 3.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


# =========================================================================
# PDF 1: Lab 1 - Requirements Engineering & RTM
# =========================================================================
def build_re_pdf():
    pdf_path = ROOT / "1-Requirements_Engineering" / "Requirements_Engineering_Report.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        title="Lab 1: Requirements Engineering Report",
        author="Mudit Chaturvedi",
    )
    story = [
        Paragraph("Lab 1: Requirements Engineering & Traceability", styles["DocTitle"]),
        Paragraph("<b>Problem Statement #33: Micro-Lending &amp; Peer Credit Risk Assessor</b>", styles["DocSub"]),
        Paragraph("Student: Mudit Chaturvedi | SRN: PES1UG24CS279 | Section 5E | Course: UE24CS341A", styles["DocSub"]),
        Spacer(1, 4 * mm),
        Paragraph("1. Problem Context & Overview", styles["SecH1"]),
        Paragraph(
            "The <b>Micro-Lending &amp; Peer Credit Risk Assessor</b> platform is a decentralized peer-to-peer micro-finance ecosystem "
            "engineered to expand responsible credit access to underserved borrowers. It calculates deterministic borrower credit risk scores "
            "from debt-to-income (DTI) metrics, produces exact reducing-balance repayment schedules, orchestrates fractional peer investments, "
            "and triggers automated default warnings upon missed deadlines.",
            styles["BodyTextJ"],
        ),
        Spacer(1, 2 * mm),
        Paragraph("2. Functional Requirements Table (FR-001 to FR-005)", styles["SecH1"]),
    ]

    # FR Table
    fr_data = [
        [
            Paragraph("ID", styles["TableHead"]),
            Paragraph("Priority", styles["TableHead"]),
            Paragraph("Description", styles["TableHead"]),
            Paragraph("Acceptance Criteria", styles["TableHead"]),
            Paragraph("Rationale", styles["TableHead"]),
        ],
        [
            Paragraph("FR-001", styles["TableCellBold"]),
            Paragraph("High", styles["TableCell"]),
            Paragraph("Compute borrower credit risk ratings and numerical scores (300–850) based on DTI, repayment history, and employment stability.", styles["TableCell"]),
            Paragraph("<b>Pass:</b> Risk tier (Low/Med/High) accurately assigned.<br/><b>Fail:</b> Incomplete profile generates approval.", styles["TableCell"]),
            Paragraph("Automates underwriting without bias while safeguarding peer lender capital.", styles["TableCell"]),
        ],
        [
            Paragraph("FR-002", styles["TableCellBold"]),
            Paragraph("High", styles["TableCell"]),
            Paragraph("Generate structured reducing-balance EMI schedules with detailed principal/interest splits upon loan approval.", styles["TableCell"]),
            Paragraph("<b>Pass:</b> Sum of principal matches sanctioned amount (diff &le; Rs.0.50).<br/><b>Fail:</b> Negative amortization or rounding drift.", styles["TableCell"]),
            Paragraph("Provides transparent repayment obligations for borrowers and cash flow projections for lenders.", styles["TableCell"]),
        ],
        [
            Paragraph("FR-003", styles["TableCellBold"]),
            Paragraph("High", styles["TableCell"]),
            Paragraph("Enable Peer Lenders to browse active loans, filter by risk tiers, and commit fractional funds into escrow.", styles["TableCell"]),
            Paragraph("<b>Pass:</b> Escrow locked atomically, listing marked Fully Funded at 100%.<br/><b>Fail:</b> Overfunding permitted or wallet deducted without lock.", styles["TableCell"]),
            Paragraph("Enables fractional risk diversification across multiple micro-borrowers.", styles["TableCell"]),
        ],
        [
            Paragraph("FR-004", styles["TableCellBold"]),
            Paragraph("Medium", styles["TableCell"]),
            Paragraph("Process borrower installment payments via gateway and distribute proportional dividends to participating lenders.", styles["TableCell"]),
            Paragraph("<b>Pass:</b> Proportional shares credited inside an ACID transaction.<br/><b>Fail:</b> Borrower debited but lender wallets unchanged.", styles["TableCell"]),
            Paragraph("Preserves financial ledger integrity and guarantees fair dividend returns.", styles["TableCell"]),
        ],
        [
            Paragraph("FR-005", styles["TableCellBold"]),
            Paragraph("High", styles["TableCell"]),
            Paragraph("Monitor repayment due dates and automatically trigger tiered default warnings when grace periods expire.", styles["TableCell"]),
            Paragraph("<b>Pass:</b> T+3 days triggers reminder; T+15 days triggers formal default.<br/><b>Fail:</b> Warning fires on on-time accounts or fails to fire.", styles["TableCell"]),
            Paragraph("Enforces disciplined repayment and minimizes platform Non-Performing Assets.", styles["TableCell"]),
        ],
    ]

    t_fr = Table(fr_data, colWidths=[18 * mm, 16 * mm, 50 * mm, 54 * mm, 44 * mm])
    t_fr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_fr)

    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("3. Non-Functional Requirements (NFR-001 & NFR-002)", styles["SecH1"]))

    nfr_data = [
        [
            Paragraph("ID & Type", styles["TableHead"]),
            Paragraph("Priority", styles["TableHead"]),
            Paragraph("Description", styles["TableHead"]),
            Paragraph("Acceptance Criteria", styles["TableHead"]),
            Paragraph("Rationale", styles["TableHead"]),
        ],
        [
            Paragraph("NFR-001<br/>Performance &amp; Security", styles["TableCellBold"]),
            Paragraph("High", styles["TableCell"]),
            Paragraph("Repayment transactions, escrow locks, and lender dividend payouts must execute inside ACID transactions with strict serializability.", styles["TableCell"]),
            Paragraph("<b>Pass:</b> 200 concurrent requests verify zero ledger discrepancies, 100% atomic rollbacks, latency &lt; 350 ms.<br/><b>Fail:</b> Race conditions or double debits.", styles["TableCell"]),
            Paragraph("Ledger consistency is mission-critical; financial inconsistencies create legal liability and violate RBI P2P mandates.", styles["TableCell"]),
        ],
        [
            Paragraph("NFR-002<br/>Reliability &amp; Privacy", styles["TableCellBold"]),
            Paragraph("High", styles["TableCell"]),
            Paragraph("Borrower PII, tax IDs, and credit data must be encrypted at rest (AES-256) and in transit (TLS 1.3), with backups ensuring RPO &le; 15m, RTO &le; 1h.", styles["TableCell"]),
            Paragraph("<b>Pass:</b> Zero plaintext PII in database, TLS 1.3 enforced, disaster recovery restores operational state &lt; 45 mins.<br/><b>Fail:</b> Plaintext PII leak or RTO &gt; 1h.", styles["TableCell"]),
            Paragraph("Ensures regulatory compliance, user data confidentiality, and guarantees platform operational recovery.", styles["TableCell"]),
        ],
    ]

    t_nfr = Table(nfr_data, colWidths=[24 * mm, 14 * mm, 50 * mm, 50 * mm, 44 * mm])
    t_nfr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_nfr)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("RE PDF generated successfully.")


# =========================================================================
# PDF 2: Use-Case Flow Specification (1 Page Core Spec)
# =========================================================================
def build_uc_spec_pdf():
    pdf_path = ROOT / "1-Requirements_Engineering" / "Use_Case_Flow_Specification.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=15 * mm,
        bottomMargin=14 * mm,
        title="Use-Case Flow Specification: UC-01",
        author="Mudit Chaturvedi",
    )
    story = [
        Paragraph("Use-Case Flow Specification", styles["DocTitle"]),
        Paragraph("<b>UC-01: Apply for Micro-Loan &amp; Assess Credit Risk</b>", styles["DocSub"]),
        Paragraph("Student: Mudit Chaturvedi (PES1UG24CS279) | Problem Statement #33", styles["DocSub"]),
        Spacer(1, 2 * mm),
        Paragraph("<b>Use Case ID:</b> UC-01 (includes UC-02, UC-03, UC-04) &nbsp;|&nbsp; <b>Primary Actor:</b> Borrower &nbsp;|&nbsp; <b>Secondary Actors:</b> Credit Engine, Gateway", styles["BodyTextJ"]),
        Paragraph("<b>Goal in Context:</b> Borrower submits loan request and financial metrics; system performs algorithmic risk scoring, generates an amortization schedule, and publishes to the peer marketplace.", styles["BodyTextJ"]),
        Spacer(1, 1 * mm),
        Paragraph("Preconditions &amp; Postconditions", styles["SecH1"]),
        Paragraph("• <b>Preconditions:</b> (1) Borrower is registered with verified phone/email. (2) No delinquent active default notices. (3) Credit Engine service is operational.", styles["BodyTextJ"]),
        Paragraph("• <b>Success Postconditions:</b> (1) Credit score (300-850) and risk tier (Low/Med/High) recorded. (2) Amortization schedule generated. (3) Loan published to marketplace as OPEN_FOR_FUNDING.", styles["BodyTextJ"]),
        Paragraph("• <b>Failure Postconditions:</b> (1) No listing published. (2) Application tagged REJECTED with actionable feedback.", styles["BodyTextJ"]),
        Spacer(1, 1 * mm),
        Paragraph("Main Success Scenario (MSS)", styles["SecH1"]),
        Paragraph("1. <b>Application Initiation:</b> Borrower specifies requested principal (Rs. 40,000) and tenure (6 months).", styles["BodyTextJ"]),
        Paragraph("2. <b>Financial Ingestion («include» UC-02):</b> Borrower submits monthly net income, existing debt obligations, and employment tenure.", styles["BodyTextJ"]),
        Paragraph("3. <b>Heuristic Scoring («include» UC-03):</b> System computes Debt-to-Income (DTI = 21.5%), evaluates repayment history ratio (0.96), and calculates composite credit score (717/850).", styles["BodyTextJ"]),
        Paragraph("4. <b>Risk Tiering:</b> System maps score to <b>Medium Risk</b> (benchmark APR: 15.0%, borrowing ceiling: Rs. 50,000).", styles["BodyTextJ"]),
        Paragraph("5. <b>Amortization Generation («include» UC-04):</b> System produces reducing-balance schedule (Monthly EMI: Rs. 6,961.35).", styles["BodyTextJ"]),
        Paragraph("6. <b>Borrower Acceptance:</b> Borrower reviews loan terms and accepts the offer digitally.", styles["BodyTextJ"]),
        Paragraph("7. <b>Marketplace Activation:</b> Listing state set to OPEN_FOR_FUNDING; notification dispatched to peer lenders.", styles["BodyTextJ"]),
        Spacer(1, 1 * mm),
        Paragraph("Alternate Flows", styles["SecH1"]),
        Paragraph("• <b>A1: High-Risk Classification:</b> If credit score is 450–600 or DTI 45%–60%, system categorizes loan as High Risk (APR: 22.0%, cap: Rs. 15,000). If requested principal exceeds Rs. 15,000, borrower is prompted to reduce principal.", styles["BodyTextJ"]),
        Paragraph("• <b>A2: Immediate Rejection (Excessive DTI &gt; 60%):</b> If DTI &gt; 60% or score &lt; 450, application is set to REJECTED_HIGH_RISK with a 90-day cooling advisory. Use case terminates.", styles["BodyTextJ"]),
        Paragraph("• <b>E1: Database Persistence Timeout:</b> If transaction fails during marketplace save, database rolls back immediately and borrower is advised to retry.", styles["BodyTextJ"]),
    ]

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("Use-Case Flow Spec PDF generated successfully.")


# =========================================================================
# PDF 3: Lab 3 - Architectural Justification (1 Page Strict Spec)
# =========================================================================
def build_arch_pdf():
    pdf_path = ROOT / "2-Architectural_Diagram" / "Architectural_Justification_Report.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=15 * mm,
        bottomMargin=14 * mm,
        title="Lab 3: Architectural Justification",
        author="Mudit Chaturvedi",
    )
    story = [
        Paragraph("Lab 3: Component Modelling &amp; Architectural Justification", styles["DocTitle"]),
        Paragraph("<b>Problem Statement #33: Micro-Lending &amp; Peer Credit Risk Assessor</b>", styles["DocSub"]),
        Paragraph("Student: Mudit Chaturvedi | SRN: PES1UG24CS279 | Section 5E", styles["DocSub"]),
        Spacer(1, 3 * mm),
        Paragraph('Architecture Selection: <i>"We chose a 3-Tier Layered Architecture with Service-Oriented Component Decoupling for the Micro-Lending &amp; Peer Credit Risk Assessor System."</i>', styles["QuoteBox"]),
        Spacer(1, 2 * mm),
        Paragraph("1. Architectural Choice", styles["SecH1"]),
        Paragraph(
            "For the Micro-Lending platform, we selected a <b>3-Tier Layered Architecture</b> structured into: "
            "(1) Presentation &amp; Client Layer, (2) Core Domain &amp; Business Services Layer, and (3) Data Persistence &amp; External Integration Layer. "
            "Internal communication between domain components (Loan Management, Credit Risk Engine, Amortization Engine, P2P Marketplace, "
            "Payment Settlement, and Default Monitor) is strictly governed by explicit provided and required interfaces using UML ball-and-socket notation "
            "(<code>ICreditAssessment</code>, <code>IScheduleGenerator</code>, <code>IEscrowFunding</code>, and <code>IPaymentSettlement</code>).",
            styles["BodyTextJ"],
        ),
        Paragraph("2. Two Specific Scenario-Related Reasons", styles["SecH1"]),
        Paragraph(
            "• <b>Reason 1: Decoupling Volatile Heuristic Risk Logic from Core Settlement Ledgers (FR-001):</b><br/>"
            "Underwriting heuristic formulas (DTI weights, stability coefficients, credit tier thresholds) evolve continuously as risk policies "
            "are calibrated. Encapsulating the <code>CreditRiskEngine</code> behind the <code>ICreditAssessment</code> interface ensures algorithm tuning "
            "can occur without modifying database schemas, payment gateways, or double-entry accounting services.",
            styles["BodyTextJ"],
        ),
        Paragraph(
            "• <b>Reason 2: Guaranteed Transactional Consistency in Fractional Escrow Payouts (FR-003, FR-004):</b><br/>"
            "In peer-to-peer lending, fractional lender allocations and installment dividend distributions must satisfy strict ledger conservation "
            "(&sum; Debits = &sum; Credits). A layered architecture enforces strict transactional boundaries, ensuring all balance mutations occur "
            "strictly within the <code>Payment Settlement Service</code> and the underlying ACID relational database.",
            styles["BodyTextJ"],
        ),
        Paragraph("3. Security Advantage: Sensitive Financial PII &amp; Escrow Isolation", styles["SecH1"]),
        Paragraph(
            "Borrower PAN, bank credentials, and credit reports represent high-risk data subject to RBI NBFC-P2P regulatory mandates. "
            "Layering ensures client-facing presentation apps have zero direct database access. All data queries must pass through authenticated "
            "business services where role-based access control (RBAC) and AES-256 column-level encryption are strictly enforced.",
            styles["BodyTextJ"],
        ),
        Paragraph("4. Performance Benefit: Caching Read-Heavy Marketplace Traffic Without Write Contention", styles["SecH1"]),
        Paragraph(
            "Read-heavy operations (hundreds of peer lenders browsing loan listings) are separated from write-intensive ACID transaction ledgers. "
            "Marketplace listings are served from an in-memory Redis cache at the application layer, ensuring 99th-percentile repayment transaction latency "
            "remains strictly below 250 ms without lock contention on the primary relational database.",
            styles["BodyTextJ"],
        ),
    ]

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("Architectural Justification PDF generated successfully.")


if __name__ == "__main__":
    build_re_pdf()
    build_uc_spec_pdf()
    build_arch_pdf()
    print("All PDFs compiled successfully.")
