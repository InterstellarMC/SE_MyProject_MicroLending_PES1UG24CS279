"""
Micro-Lending & Peer Credit Risk Assessor
Component 6: Default Monitoring & Warning Service (FR-005)

Author: Mudit Chaturvedi (SRN: PES1UG24CS279)
Course: UE24CS341A - Software Engineering
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List


class AlertLevel(str, Enum):
    ON_TIME = "ON_TIME"
    GRACE_PERIOD_REMINDER = "GRACE_PERIOD_REMINDER"  # 1 to 3 days overdue
    FIRST_OVERDUE_WARNING = "FIRST_OVERDUE_WARNING"  # 4 to 14 days overdue
    DEFAULT_NOTICE = "DEFAULT_NOTICE"  # >= 15 days overdue


@dataclass
class AlertNotification:
    borrower_id: str
    loan_id: str
    installment_month: int
    overdue_days: int
    alert_level: AlertLevel
    message: str
    penalty_fee: float
    downgrade_risk_tier: bool


class DefaultMonitor:
    """
    Monitors repayment due dates and automatically triggers tiered default warnings.
    Satisfies FR-005.
    """

    GRACE_PERIOD_DAYS = 3
    DEFAULT_THRESHOLD_DAYS = 15
    LATE_PENALTY_RATE = 0.02  # 2% late fee on overdue installment

    def check_installment_status(
        self, borrower_id: str, loan_id: str, installment_month: int, due_date: date, emi_amount: float, current_date: date
    ) -> AlertNotification:
        overdue_days = (current_date - due_date).days

        if overdue_days <= 0:
            return AlertNotification(
                borrower_id=borrower_id,
                loan_id=loan_id,
                installment_month=installment_month,
                overdue_days=0,
                alert_level=AlertLevel.ON_TIME,
                message="Installment is current. No action required.",
                penalty_fee=0.0,
                downgrade_risk_tier=False,
            )

        if overdue_days <= self.GRACE_PERIOD_DAYS:
            return AlertNotification(
                borrower_id=borrower_id,
                loan_id=loan_id,
                installment_month=installment_month,
                overdue_days=overdue_days,
                alert_level=AlertLevel.GRACE_PERIOD_REMINDER,
                message=(
                    f"Reminder: Installment #{installment_month} is {overdue_days} day(s) past due. "
                    f"Please settle within the 3-day grace period to avoid penalties."
                ),
                penalty_fee=0.0,
                downgrade_risk_tier=False,
            )

        if overdue_days < self.DEFAULT_THRESHOLD_DAYS:
            penalty = round(emi_amount * self.LATE_PENALTY_RATE, 2)
            return AlertNotification(
                borrower_id=borrower_id,
                loan_id=loan_id,
                installment_month=installment_month,
                overdue_days=overdue_days,
                alert_level=AlertLevel.FIRST_OVERDUE_WARNING,
                message=(
                    f"Urgent Overdue Warning: Grace period expired. Installment #{installment_month} is {overdue_days} "
                    f"days overdue. A late fee of Rs. {penalty:,.2f} has been levied."
                ),
                penalty_fee=penalty,
                downgrade_risk_tier=False,
            )

        # 15+ Days: Formal Default
        penalty = round(emi_amount * 0.05, 2)  # 5% default surcharge
        return AlertNotification(
            borrower_id=borrower_id,
            loan_id=loan_id,
            installment_month=installment_month,
            overdue_days=overdue_days,
            alert_level=AlertLevel.DEFAULT_NOTICE,
            message=(
                f"FORMAL DEFAULT NOTICE: Loan {loan_id} installment #{installment_month} is {overdue_days} days delinquent. "
                f"Credit rating downgraded to High Risk. Collection proceedings initiated."
            ),
            penalty_fee=penalty,
            downgrade_risk_tier=True,
        )
