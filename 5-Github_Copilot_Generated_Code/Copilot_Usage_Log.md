# GitHub Copilot Usage & Prompt Engineering Log
## Micro-Lending & Peer Credit Risk Assessor (Problem Statement #33)

**Course:** Software Engineering (UE24CS341A) — Lab Deliverable (e)  
**Student Name:** Mudit Chaturvedi  
**SRN:** PES1UG24CS279  
**Tool Used:** GitHub Copilot (VS Code / JetBrains IDE Extension)  

---

### 1. Overview & Objective
This log documents the interactive prompt workflows, code generation steps, and iterative refactoring sessions conducted with **GitHub Copilot** to implement the core business logic components for the **Micro-Lending & Peer Credit Risk Assessor** platform. Copilot was utilized to assist with algorithmic boilerplate, financial rounding constraints, and edge-case validation.

---

### 2. Prompting Sessions & Generated Code Blocks

#### Session 1: Heuristic Credit Scoring Formula & Boundary Rules (FR-001)
- **Context & Prompt Provided:**
  ```text
  // Prompt: Create a Python dataclass FinancialProfile (monthly_income, existing_monthly_debt,
  // employment_tenure_months, is_salaried, repayment_history_ratio).
  // Write a class CreditRiskAssessor with an evaluate() method implementing:
  // 1. DTI = (existing_monthly_debt / monthly_income) * 100
  // 2. Reject if DTI > 60%
  // 3. Composite score = 300 + 5.5 * (0.45*dti_score + 0.30*repayment_score + 0.25*employment_score)
  // 4. Categorize risk tier: >=720 Low, >=600 Med, >=450 High, <450 Reject.
  // Enforce defensive validation for negative values.
  ```
- **Copilot Contribution:**
  - Scaffolded the `FinancialProfile` and `AssessmentResult` dataclasses with strict typing.
  - Implemented the boundary checks ensuring negative values raise `ValueError`.
  - Added clamp functions (`min(850, max(300, score))`) to prevent score overflow.
- **Manual Verification & Refinement:**
  - Adjusted the salaried multiplier to 1.10x to reward steady payroll employment.
  - Set the explicit max borrowing caps (Low: ₹1,00,000, Medium: ₹50,000, High: ₹15,000).

#### Session 2: Reducing Balance EMI Amortization Schedule (FR-002)
- **Context & Prompt Provided:**
  ```text
  // Prompt: Write an AmortizationEngine class in Python to calculate monthly reducing balance EMI
  // using formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1).
  // Then write generate_schedule() returning a breakdown of Month, DueDate (+30 days),
  // OpeningBalance, EMI, PrincipalComponent, InterestComponent, and ClosingBalance.
  // IMPORTANT: Fix final month rounding drift so closing balance is strictly 0.0.
  ```
- **Copilot Contribution:**
  - Correctly wrote the monthly rate conversion `(apr / 100) / 12` and exponential power factor.
  - Suggested using the final-month reconciliation logic:
    ```python
    if month == tenure_months:
        principal_comp = round(current_balance, 2)
        month_emi = round(principal_comp + interest_comp, 2)
        closing_balance = 0.0
    ```
- **Manual Verification & Refinement:**
  - Audited mathematical conservation: checked that `sum(principal_comp) == principal` to within ₹0.01 across various tenures (3, 6, 12, 24 months).

#### Session 3: Escrow Allocation & Overfunding Prevention (FR-003, NFR-001)
- **Context & Prompt Provided:**
  ```text
  // Prompt: In escrow_marketplace.py, implement commit_funding() method where peer lenders
  // contribute partial funds to a loan listing.
  // Ensure ACID checks: verify lender wallet balance, prevent overfunding beyond requested principal,
  // deduct wallet, increment escrow, and set status to FULLY_FUNDED when target is reached.
  ```
- **Copilot Contribution:**
  - Generated wallet tracking dictionary and escrow balance ledger.
  - Generated the remaining needed check:
    ```python
    remaining_needed = listing.requested_amount - listing.funded_amount
    if commitment_amount > remaining_needed:
        raise ValueError(...)
    ```

#### Session 4: Tiered Default Alerting Rules (FR-005)
- **Context & Prompt Provided:**
  ```text
  // Prompt: Implement DefaultMonitor class with check_installment_status().
  // Calculate overdue_days = (current_date - due_date).days.
  // If <= 0 -> ON_TIME.
  // If 1..3 days -> GRACE_PERIOD_REMINDER (no fee).
  // If 4..14 days -> FIRST_OVERDUE_WARNING (2% late fee).
  // If >= 15 days -> DEFAULT_NOTICE (5% penalty, downgrade_risk_tier=True).
  ```
- **Copilot Contribution:**
  - Generated enum `AlertLevel` and alert notification dataclass.
  - Created descriptive, user-friendly notification messages for each escalation step.

---

### 3. Key Observations & Best Practices
1. **Mathematical Accuracy:** Financial calculations require explicit rounding (`round(x, 2)`) at each intermediate step to prevent IEEE 754 floating-point drift.
2. **Defensive Validation:** Copilot-generated methods were augmented with strict input validation guarding against zero-division (e.g., zero tenure or zero monthly income).
3. **Traceability:** All code snippets directly map back to requirements `FR-001` through `FR-005` in the Requirements Engineering specification.
