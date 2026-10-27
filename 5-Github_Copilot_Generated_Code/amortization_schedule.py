"""
Micro-Lending & Peer Credit Risk Assessor
Component 3: Amortization & Repayment Engine (FR-002)

Author: Mudit Chaturvedi (SRN: PES1UG24CS279)
Course: UE24CS341A - Software Engineering
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List


@dataclass
class Installment:
    """One scheduled payment and its remaining balance."""

    month_number: int
    due_date: date
    opening_balance: float
    emi_amount: float
    principal_component: float
    interest_component: float
    closing_balance: float
    status: str = "PENDING"  # PENDING, PAID, OVERDUE, DEFAULTED


@dataclass
class RepaymentSchedule:
    """Loan totals and the list of scheduled payments."""

    principal: float
    annual_interest_rate: float
    tenure_months: int
    monthly_emi: float
    total_interest_payable: float
    total_repayment: float
    installments: List[Installment]


class AmortizationEngine:
    """
    Computes reducing balance Equated Monthly Installment (EMI) schedules.
    Satisfies FR-002.
    """

    @staticmethod
    def calculate_emi(
        principal: float, apr: float, tenure_months: int
    ) -> float:
        """Return the rounded monthly payment for a positive-rate loan."""
        if principal <= 0 or apr <= 0 or tenure_months <= 0:
            raise ValueError(
                "Principal, APR, and tenure must all be strictly positive."
            )

        monthly_rate = (apr / 100.0) / 12.0
        # Formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        factor = (1.0 + monthly_rate) ** tenure_months
        emi = principal * (monthly_rate * factor) / (factor - 1.0)
        return round(emi, 2)

    def generate_schedule(
        self,
        principal: float,
        apr: float,
        tenure_months: int,
        start_date: date = None,
    ) -> RepaymentSchedule:
        """Build the payment schedule and reconcile the final balance."""
        if start_date is None:
            start_date = date.today()

        monthly_rate = (apr / 100.0) / 12.0
        emi = self.calculate_emi(principal, apr, tenure_months)

        installments: List[Installment] = []
        current_balance = principal
        total_interest = 0.0

        for month in range(1, tenure_months + 1):
            # Advance due date by 30 days per installment
            due_date = start_date + timedelta(days=30 * month)

            interest_comp = round(current_balance * monthly_rate, 2)

            # In the final month, reconcile any rounding cents to ensure zero
            # closing balance
            if month == tenure_months:
                principal_comp = round(current_balance, 2)
                month_emi = round(principal_comp + interest_comp, 2)
                closing_balance = 0.0
            else:
                principal_comp = round(emi - interest_comp, 2)
                closing_balance = round(current_balance - principal_comp, 2)
                month_emi = emi

            total_interest += interest_comp

            installments.append(
                Installment(
                    month_number=month,
                    due_date=due_date,
                    opening_balance=round(current_balance, 2),
                    emi_amount=month_emi,
                    principal_component=principal_comp,
                    interest_component=interest_comp,
                    closing_balance=closing_balance,
                    status="PENDING",
                )
            )

            current_balance = closing_balance

        total_repayment = round(principal + total_interest, 2)

        return RepaymentSchedule(
            principal=principal,
            annual_interest_rate=apr,
            tenure_months=tenure_months,
            monthly_emi=emi,
            total_interest_payable=round(total_interest, 2),
            total_repayment=total_repayment,
            installments=installments,
        )
