"""
Micro-Lending & Peer Credit Risk Assessor
Component 2: Credit Risk Evaluation Engine (FR-001)

Author: Mudit Chaturvedi (SRN: PES1UG24CS279)
Course: UE24CS341A - Software Engineering
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskTier(str, Enum):
    """Risk categories used by the assessment result."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    REJECTED = "Rejected"


@dataclass
class FinancialProfile:
    """Income, debt and repayment details supplied for assessment."""
    monthly_income: float
    existing_monthly_debt: float
    employment_tenure_months: int
    is_salaried: bool
    repayment_history_ratio: float  # Value between 0.0 and 1.0 (on-time payments / total installments)


@dataclass
class AssessmentResult:
    """Score, lending limit and decision returned for an application."""
    credit_score: int
    risk_tier: RiskTier
    debt_to_income_ratio: float
    recommended_apr: float
    max_borrowing_limit: float
    is_approved: bool
    rejection_reason: Optional[str] = None


class CreditRiskAssessor:
    """
    Evaluates borrower credit risk using deterministic heuristic rules.
    Satisfies FR-001.
    """

    MAX_PERMITTED_DTI = 60.0  # DTI > 60% results in automatic rejection
    MIN_CREDIT_SCORE = 300
    MAX_CREDIT_SCORE = 850

    def evaluate(self, profile: FinancialProfile, requested_amount: float) -> AssessmentResult:
        # Step 1: Input Validation
        """Validate a borrower profile and apply the credit scoring rules."""
        if profile.monthly_income <= 0:
            raise ValueError("Monthly income must be strictly greater than zero.")
        if profile.existing_monthly_debt < 0:
            raise ValueError("Existing monthly debt cannot be negative.")
        if profile.employment_tenure_months < 0:
            raise ValueError("Employment tenure cannot be negative.")
        if not 0.0 <= profile.repayment_history_ratio <= 1.0:
            raise ValueError("Repayment history ratio must be between 0.0 and 1.0.")
        if requested_amount <= 0:
            raise ValueError("Requested loan amount must be positive.")

        # Step 2: Calculate Debt-to-Income (DTI) Ratio
        dti = (profile.existing_monthly_debt / profile.monthly_income) * 100.0

        # Boundary Check: Excessive DTI leads to immediate rejection
        if dti > self.MAX_PERMITTED_DTI:
            return AssessmentResult(
                credit_score=420,
                risk_tier=RiskTier.REJECTED,
                debt_to_income_ratio=round(dti, 2),
                recommended_apr=0.0,
                max_borrowing_limit=0.0,
                is_approved=False,
                rejection_reason=f"Debt-to-Income ratio ({dti:.1f}%) exceeds maximum statutory threshold of 60.0%."
            )

        # Step 3: Heuristic Sub-Scores (each scaled to 0-100)
        # a) DTI Score: Lower DTI yields higher score
        dti_score = max(0.0, 100.0 - (dti * 1.5))

        # b) Employment Stability Score
        emp_multiplier = 1.10 if profile.is_salaried else 1.00
        tenure_base = min(100.0, profile.employment_tenure_months * 2.5)
        employment_score = min(100.0, tenure_base * emp_multiplier)

        # c) Repayment History Score
        repayment_score = profile.repayment_history_ratio * 100.0

        # Step 4: Weighted Composite Score (Weights: 45% DTI, 30% Repayment, 25% Stability)
        composite_metric = (
            (0.45 * dti_score) +
            (0.30 * repayment_score) +
            (0.25 * employment_score)
        )

        # Scale linearly to financial score range [300, 850]
        credit_score = int(round(300 + (5.5 * composite_metric)))
        credit_score = max(self.MIN_CREDIT_SCORE, min(self.MAX_CREDIT_SCORE, credit_score))

        # Step 5: Risk Tiering & Benchmark Pricing
        if credit_score >= 720:
            risk_tier = RiskTier.LOW
            recommended_apr = 10.5
            max_limit = 100000.0
        elif credit_score >= 600:
            risk_tier = RiskTier.MEDIUM
            recommended_apr = 15.0
            max_limit = 50000.0
        elif credit_score >= 450:
            risk_tier = RiskTier.HIGH
            recommended_apr = 22.0
            max_limit = 15000.0
        else:
            return AssessmentResult(
                credit_score=credit_score,
                risk_tier=RiskTier.REJECTED,
                debt_to_income_ratio=round(dti, 2),
                recommended_apr=0.0,
                max_borrowing_limit=0.0,
                is_approved=False,
                rejection_reason=f"Credit score ({credit_score}) is below minimum underwriting threshold (450)."
            )

        # Check if requested principal is within allowed risk limits
        is_approved = requested_amount <= max_limit
        rejection_reason = None
        if not is_approved:
            rejection_reason = (
                f"Requested amount (Rs. {requested_amount:,.2f}) exceeds maximum allowed borrowing limit "
                f"(Rs. {max_limit:,.2f}) for assigned {risk_tier.value} Risk tier."
            )

        return AssessmentResult(
            credit_score=credit_score,
            risk_tier=risk_tier,
            debt_to_income_ratio=round(dti, 2),
            recommended_apr=recommended_apr,
            max_borrowing_limit=max_limit,
            is_approved=is_approved,
            rejection_reason=rejection_reason
        )
