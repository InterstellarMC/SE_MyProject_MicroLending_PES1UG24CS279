# Software Testing & Defect Triage Report
## Micro-Lending & Peer Credit Risk Assessor (Problem Statement #33)

**Course:** Software Engineering (UE24CS341A) — Lab Deliverable (f)  
**Student Name:** Mudit Chaturvedi  
**SRN:** PES1UG24CS279  
**Test Framework:** `pytest` (Version 8.4.2 / Python 3.13)  
**Repository:** `MyProject_MicroLending`  

---

### 1. Test Strategy & Objectives
The testing suite verifies the end-to-end reliability, mathematical accuracy, and transactional safety of the **Micro-Lending & Peer Credit Risk Assessor** platform. Testing focuses on:
- Boundary-value analysis on financial credit parameters (DTI > 60%).
- Numerical invariance and precision conservation on loan amortization schedules.
- Concurrency and escrow constraints (prevention of overfunding and unauthorized commitments).
- Time-based state transitions for default warnings and grace periods.

---

### 2. Test Execution Matrix

| Test Case ID | Test Method Name | Target Requirement | Description / Scenario | Expected Result | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **TC-01** | `test_tc01_low_risk_borrower_approval` | **FR-001** | Borrower with low DTI (15%), 36-month tenure, 100% repayment history. | Evaluated as `Low Risk`, score $\ge 720$, APR $10.5\%$, approved. | **PASSED** |
| **TC-02** | `test_tc02_excessive_dti_rejection` | **FR-001** | Borrower with DTI = 70% exceeding 60% statutory threshold. | Auto-rejected with descriptive message. | **PASSED** |
| **TC-03** | `test_tc03_invalid_input_validation` | **FR-001** | Negative income, negative debt, ratio $> 1.0$. | Raises defensive `ValueError`. | **PASSED** |
| **TC-04** | `test_tc04_amortization_schedule_balance_conservation` | **FR-002** | 12-month reducing balance loan amortization. | $\sum \text{Principal} = P$, month $n$ balance is strictly ₹0.00. | **PASSED** |
| **TC-05** | `test_tc05_escrow_overfunding_prevention` | **FR-003** | Lender attempts funding exceeding remaining loan target. | Raises `ValueError`, prevents overfunding, caps at 100%. | **PASSED** |
| **TC-06** | `test_tc06_insufficient_wallet_balance_rejection` | **FR-003** | Lender attempts commitment with insufficient wallet funds. | Blocked with descriptive balance error. | **PASSED** |
| **TC-07** | `test_tc07_default_monitoring_escalation_lifecycle` | **FR-005** | Simulates day $T+0$, $T+2$ (grace), $T+5$ (late fee), $T+16$ (default). | Escalates alert tiers correctly, flags risk downgrade at $T+16$. | **PASSED** |
| **TC-08** | `test_tc08_proportional_dividend_conservation` | **NFR-001** | 3 lenders with fractional commitments receive repayment shares. | Sum of payouts matches installment amount ($\pm \text{₹}0.02$). | **PASSED** |

---

### 3. Vibe Coding Defect Patch Analysis (Bug ID: BUG-001)

#### 3.1 Defect Discovery
During initial test execution of `TC-04` on a 12-month loan of ₹50,000 at 14.5% APR, an assertion failure occurred:
```text
FAILED test_micro_lending.py::test_tc04_amortization_schedule_balance_conservation
AssertionError: assert abs(0.04 - 0.0) < 0.01
```
**Root Cause:** Standard IEEE 754 floating-point rounding during repeated subtraction (`balance = balance - (emi - interest)`) accumulated an uncollected residue of ₹0.04 in Month 12, leaving the loan in an unclosed state.

#### 3.2 Vibe Coding Patch Applied
Using vibe coding prompt engineering, the amortization loop was patched to implement strict final-month reconciliation:

```python
# --- BEFORE (Defective Code) ---
for month in range(1, tenure_months + 1):
    interest_comp = round(current_balance * monthly_rate, 2)
    principal_comp = round(emi - interest_comp, 2)
    closing_balance = round(current_balance - principal_comp, 2)
    current_balance = closing_balance  # In month 12, closing_balance was 0.04

# --- AFTER (Vibe Coding Patch) ---
for month in range(1, tenure_months + 1):
    interest_comp = round(current_balance * monthly_rate, 2)
    if month == tenure_months:
        # Reconcile final installment to exact remaining balance
        principal_comp = round(current_balance, 2)
        month_emi = round(principal_comp + interest_comp, 2)
        closing_balance = 0.0
    else:
        principal_comp = round(emi - interest_comp, 2)
        closing_balance = round(current_balance - principal_comp, 2)
        month_emi = emi
```

#### 3.3 Retest Verification
After applying the patch, the test suite was re-executed:
```bash
$ pytest -v test_micro_lending.py
============================== 8 passed in 0.04s ===============================
```
All assertions passed, confirming that the residual balance drift is eliminated.

---

### 4. Raw Pytest Execution Log

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
rootdir: /Users/manojkumarchaturvedi/MyProject_MicroLending/6-Software_Testing_Tools
plugins: anyio-4.10.0
collected 8 items

test_micro_lending.py::test_tc01_low_risk_borrower_approval PASSED       [ 12%]
test_micro_lending.py::test_tc02_excessive_dti_rejection PASSED          [ 25%]
test_micro_lending.py::test_tc03_invalid_input_validation PASSED         [ 37%]
test_micro_lending.py::test_tc04_amortization_schedule_balance_conservation PASSED [ 50%]
test_micro_lending.py::test_tc05_escrow_overfunding_prevention PASSED    [ 62%]
test_micro_lending.py::test_tc06_insufficient_wallet_balance_rejection PASSED [ 75%]
test_micro_lending.py::test_tc07_default_monitoring_escalation_lifecycle PASSED [ 87%]
test_micro_lending.py::test_tc08_proportional_dividend_conservation PASSED [100%]

============================== 8 passed in 0.04s ===============================
```
