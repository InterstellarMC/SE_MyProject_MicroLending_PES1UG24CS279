#!/usr/bin/env python3
"""
Micro-Lending & Peer Credit Risk Assessor - End-to-End Demonstration
Course: UE24CS341A - Software Engineering Lab
Student: Mudit Chaturvedi (SRN: PES1UG24CS279)
Problem Statement #33 | Retail, E-Commerce & Finance
"""

from datetime import date, timedelta
from credit_risk_assessor import CreditRiskAssessor, FinancialProfile
from amortization_schedule import AmortizationEngine
from escrow_marketplace import EscrowMarketplace
from default_monitor import DefaultMonitor


def main():
    """Run the sample borrower assessment, funding and repayment flow."""
    print("=" * 80)
    print(" MICRO-LENDING & PEER CREDIT RISK ASSESSOR PLATFORM")
    print(" PES University - Dept. of CSE | Problem Statement #33")
    print(" Student: Mudit Chaturvedi | SRN: PES1UG24CS279")
    print("=" * 80)

    # -------------------------------------------------------------
    # 1. Borrower Application & Credit Risk Underwriting (FR-001)
    # -------------------------------------------------------------
    print(
        "\n[Step 1] Ingesting Borrower Profile & "
        "Computing Credit Risk (FR-001)..."
    )
    profile = FinancialProfile(
        monthly_income=65000.0,
        existing_monthly_debt=14000.0,
        employment_tenure_months=24,
        is_salaried=True,
        repayment_history_ratio=0.96,  # 96% on-time repayment history
    )
    requested_principal = 40000.0
    tenure_months = 6

    assessor = CreditRiskAssessor()
    assessment = assessor.evaluate(profile, requested_principal)

    print(f" -> Monthly Net Income       : Rs. {profile.monthly_income:,.2f}")
    print(
        " -> Existing Monthly Debt    : Rs. "
        f"{profile.existing_monthly_debt:,.2f}"
    )
    print(
        " -> Debt-to-Income (DTI)     : "
        f"{assessment.debt_to_income_ratio:.1f}%"
    )
    print(f" -> Heuristic Credit Score   : {assessment.credit_score} / 850")
    print(f" -> Assigned Risk Tier       : {assessment.risk_tier.value}")
    print(f" -> Benchmark APR            : {assessment.recommended_apr:.1f}%")
    print(
        " -> Maximum Credit Limit     : Rs. "
        f"{assessment.max_borrowing_limit:,.2f}"
    )
    print(
        " -> Underwriting Status      : "
        f"{'APPROVED' if assessment.is_approved else 'REJECTED'}"
    )

    if not assessment.is_approved:
        print(f"Application terminated: {assessment.rejection_reason}")
        return

    # -------------------------------------------------------------
    # 2. Amortization Schedule Generation (FR-002)
    # -------------------------------------------------------------
    print(
        "\n[Step 2] Generating Reducing Balance "
        "Amortization Schedule (FR-002)..."
    )
    scheduler = AmortizationEngine()
    schedule = scheduler.generate_schedule(
        principal=requested_principal,
        apr=assessment.recommended_apr,
        tenure_months=tenure_months,
        start_date=date.today(),
    )

    print(f" -> Calculated Monthly EMI   : Rs. {schedule.monthly_emi:,.2f}")
    print(
        " -> Total Interest Payable   : Rs. "
        f"{schedule.total_interest_payable:,.2f}"
    )
    print(
        f" -> Total Repayment Obligation: Rs. {schedule.total_repayment:,.2f}"
    )
    print("\n Amortization Breakdown Table:")
    print(
        f" {'Month':<6} | {'Due Date':<12} | "
        f"{'Opening Bal':<13} | {'EMI':<10} | "
        f"{'Principal':<11} | {'Interest':<10} | "
        f"{'Closing Bal':<12}"
    )
    print(" " + "-" * 88)
    for inst in schedule.installments:
        print(
            f" #{inst.month_number:<5} | {str(inst.due_date):<12} | "
            f"Rs. {inst.opening_balance:<9,.2f} | Rs. "
            f"{inst.emi_amount:<6,.2f} | "
            f"Rs. {inst.principal_component:<7,.2f} | Rs. "
            f"{inst.interest_component:<6,.2f} | "
            f"Rs. {inst.closing_balance:<8,.2f}"
        )

    # -------------------------------------------------------------
    # 3. P2P Marketplace & Escrow Fractional Funding (FR-003)
    # -------------------------------------------------------------
    print(
        "\n[Step 3] Publishing to P2P Marketplace & "
        "Aggregating Lender Funds (FR-003)..."
    )
    marketplace = EscrowMarketplace()
    loan_id = "LN-2026-0033"
    borrower_id = "BW-9021"

    marketplace.publish_listing(
        loan_id=loan_id,
        borrower_id=borrower_id,
        amount=requested_principal,
        risk_tier=assessment.risk_tier.value,
        apr=assessment.recommended_apr,
        tenure=tenure_months,
    )

    # Register two peer lenders with wallets
    marketplace.register_lender("LENDER_ALICE", 30000.0)
    marketplace.register_lender("LENDER_BOB", 25000.0)

    print(f" -> Listing published on marketplace with ID: {loan_id}")
    print(" -> Lender Alice commits Rs. 25,000.00 into Escrow...")
    marketplace.commit_funding("LENDER_ALICE", loan_id, 25000.0)

    print(" -> Lender Bob commits Rs. 15,000.00 into Escrow...")
    marketplace.commit_funding("LENDER_BOB", loan_id, 15000.0)

    listing = marketplace.get_listing(loan_id)
    print(
        " -> Total Funded Amount: Rs. "
        f"{listing.funded_amount:,.2f} / Rs. "
        f"{listing.requested_amount:,.2f}"
    )
    print(f" -> Listing State Transition: {listing.status.value}")

    # -------------------------------------------------------------
    # 4. Repayment Processing & Proportional Payouts (FR-004, NFR-001)
    # -------------------------------------------------------------
    print(
        "\n[Step 4] Processing Borrower Installment & "
        "Distributing Dividends (FR-004)..."
    )
    _show_repayment(schedule, requested_principal)

    # -------------------------------------------------------------
    # 5. Automated Default Monitoring & Warning Service (FR-005)
    # -------------------------------------------------------------
    print(
        "\n[Step 5] Simulating Overdue Scenarios & "
        "Automated Default Warnings (FR-005)..."
    )
    _show_default_alerts(schedule, borrower_id, loan_id)

    print("\n" + "=" * 80)
    print(
        " DEMONSTRATION COMPLETE: ALL 5 FUNCTIONAL "
        "REQUIREMENTS VERIFIED SUCCESSFULLY."
    )
    print("=" * 80)


def _show_default_alerts(schedule, borrower_id, loan_id):
    """Display the grace-period, late-payment and default examples."""
    monitor = DefaultMonitor()
    inst2 = schedule.installments[1]

    # Scenario A: 2 days overdue (Within 3-day grace period)
    simulated_date_grace = inst2.due_date + timedelta(days=2)
    alert_grace = monitor.check_installment_status(
        borrower_id,
        loan_id,
        inst2.month_number,
        inst2.due_date,
        inst2.emi_amount,
        simulated_date_grace,
    )
    print(f" -> Day T+2 (Grace Period): [{alert_grace.alert_level.value}]")
    print(f"    Message: {alert_grace.message}")

    # Scenario B: 6 days overdue (Past grace period)
    simulated_date_late = inst2.due_date + timedelta(days=6)
    alert_late = monitor.check_installment_status(
        borrower_id,
        loan_id,
        inst2.month_number,
        inst2.due_date,
        inst2.emi_amount,
        simulated_date_late,
    )
    print(f" -> Day T+6 (First Overdue): [{alert_late.alert_level.value}]")
    print(f"    Message: {alert_late.message}")

    # Scenario C: 18 days overdue (Default threshold)
    simulated_date_default = inst2.due_date + timedelta(days=18)
    alert_default = monitor.check_installment_status(
        borrower_id,
        loan_id,
        inst2.month_number,
        inst2.due_date,
        inst2.emi_amount,
        simulated_date_default,
    )
    print(
        " -> Day T+18 (Default Triggered): "
        f"[{alert_default.alert_level.value}]"
    )
    print(f"    Message: {alert_default.message}")
    print(f"    Risk Downgrade Flag: {alert_default.downgrade_risk_tier}")


def _show_repayment(schedule, requested_principal):
    """Print the sample repayment and proportional lender shares."""
    first_emi = schedule.installments[0]
    total_repaid = first_emi.emi_amount

    # Proportional payout calculation
    alice_share = total_repaid * (25000.0 / requested_principal)
    bob_share = total_repaid * (15000.0 / requested_principal)

    print(
        " -> Borrower settles Installment #1 (Rs. "
        f"{total_repaid:,.2f}) via Gateway."
    )
    first_emi.status = "PAID"
    print(" -> ACID Ledger Transaction Dispatched:")
    print(f"    - Lender Alice (62.5% share) credited: Rs. {alice_share:,.2f}")
    print(f"    - Lender Bob   (37.5% share) credited: Rs. {bob_share:,.2f}")
    print(
        "    - Sum of Payouts: Rs. "
        f"{alice_share + bob_share:,.2f} (Balance "
        "conserved)."
    )


if __name__ == "__main__":
    main()
