# Use-Case Flow Specification
## UC-01: Apply for Micro-Loan & Assess Credit Risk

**System:** Micro-Lending & Peer Credit Risk Assessor (Problem Statement #33)  
**Author:** Mudit Chaturvedi (SRN: PES1UG24CS279)  
**Use Case ID:** UC-01 (includes `UC-02`, `UC-03`, `UC-04`)  
**Primary Actor:** Borrower  
**Secondary Actors:** Credit Risk Evaluation Engine, Payment Gateway, Notification Service  

---

### 1. Description & Goal
The Borrower initiates a micro-loan application by specifying requested principal, loan duration, and submitting supporting financial indicators. The system synchronously validates the financial profile, calculates debt-to-income (DTI) metrics, runs deterministic heuristic credit risk scoring (`Low`, `Medium`, or `High`), computes risk-adjusted interest rates, produces an amortization schedule, and publishes the verified listing to the Peer Lender marketplace.

---

### 2. Preconditions
1. The Borrower is registered and authenticated with verified email/phone credentials.
2. The Borrower has no active default notices or delinquent unpaid installments on existing loans.
3. The core Credit Risk Evaluation Engine and Database are operational.

---

### 3. Postconditions
- **Success Postconditions:**
  1. The Borrower's credit score (300–850) and risk tier (`Low` / `Medium` / `High`) are recorded in the system ledger.
  2. A verified loan application record is created with an attached reducing-balance EMI schedule.
  3. The loan status transitions to `OPEN_FOR_FUNDING` and becomes discoverable by Peer Lenders on the marketplace.
  4. Confirmation SMS/Email with the approved schedule is transmitted to the Borrower.
- **Failure Postconditions:**
  1. No loan record is published to the marketplace.
  2. The application is tagged as `REJECTED` or `PENDING_DOCUMENTS`, with clear feedback logged for the Borrower.

---

### 4. Main Success Scenario (MSS)
1. **Application Submission:** The Borrower navigates to the loan portal, inputs the requested loan amount (e.g., ₹25,000), preferred tenure (e.g., 6 months), and primary purpose of borrowing.
2. **Financial Profile Ingestion (`«include» UC-02`):** The Borrower provides verified financial parameters: monthly net income, existing monthly debt obligations, employment category (Salaried/Self-Employed), and employment tenure in months.
3. **Data Sanity Check:** The system verifies that all mandatory fields are populated, numeric inputs fall within permitted ranges, and documentation formats comply with platform rules.
4. **Heuristic Risk Computation (`«include» UC-03`):** The system invokes the heuristic rule engine:
   - Calculates Debt-to-Income (DTI) ratio: $\text{DTI} = \frac{\text{Existing Monthly Debt}}{\text{Monthly Net Income}} \times 100\%$.
   - Evaluates past platform repayment consistency index.
   - Calculates employment stability coefficient based on tenure and job sector.
   - Computes weighted credit score: $\text{Score} \in [300, 850]$.
5. **Tier & Pricing Assignment:** The system maps the score to a risk tier:
   - $\text{Score} \ge 720 \implies \textbf{Low Risk}$ (Benchmark APR: $10.5\%$).
   - $600 \le \text{Score} < 720 \implies \textbf{Medium Risk}$ (Benchmark APR: $15.0\%$).
   - System checks if requested amount is within the maximum borrowing limit for the evaluated tier.
6. **Amortization Generation (`«include» UC-04`):** The system generates a structured reducing-balance repayment schedule (monthly installment, principal component, interest breakdown, and due dates).
7. **Borrower Confirmation:** The system displays the summary terms (Loan Amount, APR, Monthly EMI, Schedule) for Borrower review. The Borrower confirms acceptance.
8. **Marketplace Publication:** The system marks the application status as `OPEN_FOR_FUNDING`, generates an anonymized investor card (displaying Risk Tier, DTI, Purpose, ROI), and notifies registered Peer Lenders.

---

### 5. Alternate Flows

#### Alternate Flow A1: Sub-threshold Score Resulting in High-Risk Categorization
- **At Step 5:** The calculated credit score falls into the high-risk bracket ($450 \le \text{Score} < 600$), or DTI is between $45\%$ and $60\%$.
- **A1.1:** The system classifies the application as $\textbf{High Risk}$ (Benchmark APR: $22.0\%$) and restricts maximum principal to ₹15,000.
- **A1.2:** If the Borrower's requested amount exceeds this ceiling, the system prompts the Borrower to accept a reduced principal or provide a co-guarantor.
- **A1.3:** If accepted, the schedule is recalculated at the higher interest bracket, and the listing is posted with high-yield disclosure warnings for lenders. Resume at Step 7.

#### Alternate Flow A2: Automated Rejection Due to Excessive Debt Burden
- **At Step 4:** The calculated DTI exceeds the statutory risk limit ($> 60\%$), or credit score is below $450$.
- **A2.1:** The system halts loan generation, sets application status to `REJECTED_HIGH_RISK`.
- **A2.2:** The system generates an actionable advisory report detailing rejection reasons (excessive current leverage, insufficient tenure) and recommends a 90-day cooling period before reapplication. The use case terminates.

---

### 6. Exception Flow (Network / Persistence Fault)
- **At Step 8:** A database failure or distributed lock timeout occurs while persisting the loan record to the marketplace.
- **E1.1:** The database transaction initiates an immediate rollback to prevent orphaned application states.
- **E1.2:** The system informs the Borrower: *"We encountered an issue saving your application. Your credit assessment is saved. Please retry final submission in a moment."*
- **E1.3:** An incident alert is logged to the system observability dashboard.
