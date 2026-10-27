"""
Micro-Lending & Peer Credit Risk Assessor
Component 4: P2P Marketplace & Escrow Service (FR-003, NFR-001)

Author: Mudit Chaturvedi (SRN: PES1UG24CS279)
Course: UE24CS341A - Software Engineering
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class LoanListingStatus(str, Enum):
    """Funding states supported by a loan listing."""
    PENDING_APPROVAL = "PENDING_APPROVAL"
    OPEN_FOR_FUNDING = "OPEN_FOR_FUNDING"
    FULLY_FUNDED = "FULLY_FUNDED"
    DISBURSED = "DISBURSED"
    CLOSED = "CLOSED"


@dataclass
class LenderCommitment:
    """A lender contribution with its creation time."""
    lender_id: str
    amount: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LoanListing:
    """Loan details, funding status and lender contributions."""
    loan_id: str
    borrower_id: str
    requested_amount: float
    risk_tier: str
    interest_rate: float
    tenure_months: int
    funded_amount: float = 0.0
    status: LoanListingStatus = LoanListingStatus.OPEN_FOR_FUNDING
    commitments: List[LenderCommitment] = field(default_factory=list)


class EscrowMarketplace:
    """
    Manages peer-to-peer loan listings, fractional lender commitments,
    and escrow allocations. Satisfies FR-003.
    """

    def __init__(self):
        self._listings: Dict[str, LoanListing] = {}
        self._lender_wallets: Dict[str, float] = {}
        self._escrow_locked_balances: Dict[str, float] = {}

    def register_lender(self, lender_id: str, initial_deposit: float):
        """Add a non-negative deposit to a lender wallet."""
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        self._lender_wallets[lender_id] = self._lender_wallets.get(lender_id, 0.0) + initial_deposit
        self._escrow_locked_balances[lender_id] = self._escrow_locked_balances.get(lender_id, 0.0)

    def get_lender_wallet_balance(self, lender_id: str) -> float:
        """Return a lender balance, or zero for an unknown lender."""
        return self._lender_wallets.get(lender_id, 0.0)

    def publish_listing(
        self, loan_id: str, borrower_id: str, amount: float, risk_tier: str, apr: float, tenure: int
    ) -> LoanListing:
        """Create and store a loan listing for peer funding."""
        if amount <= 0:
            raise ValueError("Loan amount must be positive.")
        listing = LoanListing(
            loan_id=loan_id,
            borrower_id=borrower_id,
            requested_amount=amount,
            risk_tier=risk_tier,
            interest_rate=apr,
            tenure_months=tenure,
            status=LoanListingStatus.OPEN_FOR_FUNDING,
        )
        self._listings[loan_id] = listing
        return listing

    def commit_funding(self, lender_id: str, loan_id: str, commitment_amount: float) -> bool:
        """
        Executes atomic escrow reservation for peer lender funding.
        Guarantees:
        1. Lender has sufficient available wallet balance.
        2. No overfunding beyond loan requested principal.
        3. Automatic state transition to FULLY_FUNDED upon 100% aggregation.
        """
        if loan_id not in self._listings:
            raise KeyError(f"Loan listing {loan_id} not found.")

        listing = self._listings[loan_id]
        if listing.status != LoanListingStatus.OPEN_FOR_FUNDING:
            raise ValueError(f"Loan {loan_id} is not open for funding (Current status: {listing.status.value}).")

        if commitment_amount <= 0:
            raise ValueError("Commitment amount must be strictly greater than zero.")

        # Check lender wallet balance
        available_balance = self._lender_wallets.get(lender_id, 0.0)
        if available_balance < commitment_amount:
            raise ValueError(
                f"Lender {lender_id} has insufficient funds (Available: Rs. {available_balance:,.2f}, "
                f"Requested: Rs. {commitment_amount:,.2f})."
            )

        # Check overfunding guardrail
        remaining_needed = listing.requested_amount - listing.funded_amount
        if commitment_amount > remaining_needed:
            raise ValueError(
                f"Commitment of Rs. {commitment_amount:,.2f} exceeds remaining required funding of Rs. {remaining_needed:,.2f}."
            )

        # Atomic Escrow Lock (ACID Guarantee)
        self._lender_wallets[lender_id] -= commitment_amount
        self._escrow_locked_balances[lender_id] += commitment_amount

        listing.funded_amount += commitment_amount
        listing.commitments.append(LenderCommitment(lender_id=lender_id, amount=commitment_amount))

        # Check if 100% funded
        if round(listing.funded_amount, 2) >= round(listing.requested_amount, 2):
            listing.status = LoanListingStatus.FULLY_FUNDED

        return True

    def get_listing(self, loan_id: str) -> Optional[LoanListing]:
        """Return the listing if the loan ID is known."""
        return self._listings.get(loan_id)
