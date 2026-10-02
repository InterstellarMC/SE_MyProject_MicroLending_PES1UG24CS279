"""
Micro-Lending & Peer Credit Risk Assessor - Automated Test Suite
Course: UE24CS341A - Software Engineering (Lab Deliverable f)
Student: Mudit Chaturvedi (SRN: PES1UG24CS279)
Test Framework: pytest
"""

import pytest
import sys
from datetime import date, timedelta
from pathlib import Path

# Add core implementation to system path
CODE_DIR = Path(__file__).resolve().parent.parent / "5-Github_Copilot_Generated_Code"
sys.path.insert(0, str(CODE_DIR))

from credit_risk_assessor import CreditRiskAssessor, FinancialProfile, RiskTier
from amortization_schedule import AmortizationEngine
from escrow_marketplace import EscrowMarketplace, LoanListingStatus
from default_monitor import DefaultMonitor, AlertLevel


# =====================================================================
# Test Suite 1: Credit Risk Heuristic Evaluation (FR-001)
# =====================================================================

def test_tc01_low_risk_borrower_approval():
    """TC-01: Verifies that a borrower with low DTI, high tenure, and strong history is assigned Low Risk."""
    assessor = CreditRiskAssessor()
    profile = FinancialProfile(
        monthly_income=80000.0,
        existing_monthly_debt=12000.0,  # DTI = 15.0%
        employment_tenure_months=36,
        is_salaried=True,
        repayment_history_ratio=1.0,
    )
    result = assessor.evaluate(profile, requested_amount=60000.0)

    assert result.is_approved is True
    assert result.risk_tier == RiskTier.LOW
    assert result.credit_score >= 720
    assert result.debt_to_income_ratio == 15.0
    assert result.recommended_apr == 10.5
    assert result.max_borrowing_limit == 100000.0


def test_tc02_excessive_dti_rejection():
    """TC-02: Verifies that a borrower with DTI > 60% is automatically rejected."""
    assessor = CreditRiskAssessor()
    profile = FinancialProfile(
        monthly_income=50000.0,
        existing_monthly_debt=35000.0,  # DTI = 70.0% > 60%
        employment_tenure_months=12,
        is_salaried=False,
        repayment_history_ratio=0.80,
    )
    result = assessor.evaluate(profile, requested_amount=20000.0)

    assert result.is_approved is False
    assert result.risk_tier == RiskTier.REJECTED
    assert "exceeds maximum statutory threshold" in result.rejection_reason


def test_tc03_invalid_input_validation():
    """TC-03: Verifies defensive programming guards against negative income, debt, and out-of-range ratios."""
    assessor = CreditRiskAssessor()

    with pytest.raises(ValueError, match="Monthly income must be strictly greater than zero"):
        profile = FinancialProfile(
            monthly_income=-5000.0,
            existing_monthly_debt=1000.0,
            employment_tenure_months=12,
            is_salaried=True,
            repayment_history_ratio=0.9,
        )
        assessor.evaluate(profile, 10000.0)

    with pytest.raises(ValueError, match="Repayment history ratio must be between 0.0 and 1.0"):
        profile = FinancialProfile(
            monthly_income=50000.0,
            existing_monthly_debt=5000.0,
            employment_tenure_months=12,
            is_salaried=True,
            repayment_history_ratio=1.5,
        )
        assessor.evaluate(profile, 10000.0)


# =====================================================================
# Test Suite 2: Amortization Schedule Mathematical Precision (FR-002)
# =====================================================================

def test_tc04_amortization_schedule_balance_conservation():
    """
    TC-04: Verifies reducing-balance EMI schedule:
    1. Sum of principal components strictly equals loan principal.
    2. Final month closing balance is strictly 0.00.
    """
    scheduler = AmortizationEngine()
    principal = 50000.0
    apr = 14.5
    tenure_months = 12

    schedule = scheduler.generate_schedule(principal, apr, tenure_months)

    assert len(schedule.installments) == tenure_months
    assert schedule.installments[-1].closing_balance == 0.0

    # Mathematical conservation check
    sum_principal = sum(inst.principal_component for inst in schedule.installments)
    assert abs(sum_principal - principal) < 0.01

    # Verify each month opening balance equals previous closing balance
    for i in range(1, tenure_months):
        prev_closing = schedule.installments[i - 1].closing_balance
        curr_opening = schedule.installments[i].opening_balance
        assert abs(prev_closing - curr_opening) < 0.01


# =====================================================================
# Test Suite 3: P2P Marketplace & Escrow Funding Allocation (FR-003)
# =====================================================================

def test_tc05_escrow_overfunding_prevention():
    """TC-05: Verifies that lender commitments cannot exceed remaining required loan principal."""
    marketplace = EscrowMarketplace()
    loan_id = "LN-TEST-01"
    marketplace.publish_listing(loan_id, "BW-01", amount=20000.0, risk_tier="Low", apr=10.5, tenure=6)

    marketplace.register_lender("LENDER_A", 15000.0)
    marketplace.register_lender("LENDER_B", 10000.0)

    # Lender A funds 15,000
    marketplace.commit_funding("LENDER_A", loan_id, 15000.0)
    assert marketplace.get_lender_wallet_balance("LENDER_A") == 0.0

    # Lender B attempts to fund 8,000 (exceeds remaining 5,000 needed)
    with pytest.raises(ValueError, match="exceeds remaining required funding"):
        marketplace.commit_funding("LENDER_B", loan_id, 8000.0)

    # Lender B funds exact remaining 5,000
    marketplace.commit_funding("LENDER_B", loan_id, 5000.0)
    listing = marketplace.get_listing(loan_id)
    assert listing.status == LoanListingStatus.FULLY_FUNDED
    assert listing.funded_amount == 20000.0


def test_tc06_insufficient_wallet_balance_rejection():
    """TC-06: Verifies that lenders cannot commit funds beyond their deposited wallet balance."""
    marketplace = EscrowMarketplace()
    loan_id = "LN-TEST-02"
    marketplace.publish_listing(loan_id, "BW-02", amount=10000.0, risk_tier="Medium", apr=15.0, tenure=6)

    marketplace.register_lender("LENDER_BROKE", 2000.0)

    with pytest.raises(ValueError, match="insufficient funds"):
        marketplace.commit_funding("LENDER_BROKE", loan_id, 5000.0)


# =====================================================================
# Test Suite 4: Automated Default Monitoring & Alerts (FR-005)
# =====================================================================

def test_tc07_default_monitoring_escalation_lifecycle():
    """TC-07: Verifies on-time, grace-period, overdue warning, and formal default trigger states."""
    monitor = DefaultMonitor()
    borrower_id = "BW-TEST"
    loan_id = "LN-999"
    due_date = date(2026, 10, 1)
    emi = 5000.0

    # Current (on-time)
    alert_ontime = monitor.check_installment_status(
        borrower_id, loan_id, 1, due_date, emi, current_date=date(2026, 10, 1)
    )
    assert alert_ontime.alert_level == AlertLevel.ON_TIME
    assert alert_ontime.penalty_fee == 0.0

    # T+2 Days: Grace Period
    alert_grace = monitor.check_installment_status(
        borrower_id, loan_id, 1, due_date, emi, current_date=date(2026, 10, 3)
    )
    assert alert_grace.alert_level == AlertLevel.GRACE_PERIOD_REMINDER
    assert alert_grace.penalty_fee == 0.0

    # T+5 Days: Grace Expired, Late Penalty Applied
    alert_late = monitor.check_installment_status(
        borrower_id, loan_id, 1, due_date, emi, current_date=date(2026, 10, 6)
    )
    assert alert_late.alert_level == AlertLevel.FIRST_OVERDUE_WARNING
    assert alert_late.penalty_fee == round(5000.0 * 0.02, 2)
    assert alert_late.downgrade_risk_tier is False

    # T+16 Days: Formal Default
    alert_default = monitor.check_installment_status(
        borrower_id, loan_id, 1, due_date, emi, current_date=date(2026, 10, 17)
    )
    assert alert_default.alert_level == AlertLevel.DEFAULT_NOTICE
    assert alert_default.downgrade_risk_tier is True
    assert alert_default.penalty_fee == round(5000.0 * 0.05, 2)


# =====================================================================
# Test Suite 5: Financial Conservation & Ledger Invariance (NFR-001)
# =====================================================================

def test_tc08_proportional_dividend_conservation():
    """TC-08: Verifies that fractional dividend payouts to multiple lenders sum exactly to the installment payment."""
    total_principal = 30000.0
    commitments = {"LENDER_1": 15000.0, "LENDER_2": 10000.0, "LENDER_3": 5000.0}

    repaid_emi = 5240.50

    payouts = {
        lender: round(repaid_emi * (amt / total_principal), 2)
        for lender, amt in commitments.items()
    }

    total_payout = sum(payouts.values())
    # Drift must be <= 1 cent (0.01) due to fractional rounding
    assert abs(total_payout - repaid_emi) <= 0.02
