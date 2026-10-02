# Software Requirements Specification (SRS)
## Micro-Lending & Peer Credit Risk Assessor (Problem Statement #33)
### Standard: IEEE Std 830-1998

**Prepared by:** Mudit Chaturvedi (SRN: PES1UG24CS279)  
**Department:** Computer Science & Engineering, PES University  
**Course:** Software Engineering (UE24CS341A)  
**Version:** 1.0.0  
**Date:** October 2026  

---

### Table of Contents
1. **Introduction**
   - 1.1 Purpose
   - 1.2 Document Conventions
   - 1.3 Intended Audience & Reading Suggestions
   - 1.4 Project Scope
   - 1.5 References
2. **Overall Description**
   - 2.1 Product Perspective
   - 2.2 Product Functions
   - 2.3 User Classes & Characteristics
   - 2.4 Operating Environment
   - 2.5 Design & Implementation Constraints
   - 2.6 User Documentation
   - 2.7 Assumptions & Dependencies
3. **External Interface Requirements**
   - 3.1 User Interfaces
   - 3.2 Hardware Interfaces
   - 3.3 Software Interfaces
   - 3.4 Communications Interfaces
4. **System Features & Functional Requirements**
   - 4.1 Credit Risk Heuristic Evaluation Engine (FR-001)
   - 4.2 Amortization & Repayment Schedule Generator (FR-002)
   - 4.3 P2P Lending Marketplace & Escrow Allocation (FR-003)
   - 4.4 Repayment Settlement & Proportional Dividend Distribution (FR-004)
   - 4.5 Automated Default Monitoring & Warning Service (FR-005)
5. **Non-Functional & Quality Attributes**
   - 5.1 Performance & Concurrency (NFR-001)
   - 5.2 Security, Confidentiality & Data Privacy (NFR-002)
   - 5.3 Reliability, Availability & Disaster Recovery
   - 5.4 Maintainability & Extensibility

---

### 1. Introduction

#### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) is to establish a rigorous, comprehensive baseline for the design, implementation, and verification of the **Micro-Lending & Peer Credit Risk Assessor** platform. It defines all functional capabilities, performance expectations, external interfaces, and security constraints governing peer-to-peer micro-finance transactions.

#### 1.2 Document Conventions
- Requirements are uniquely identified using alphanumeric codes: `FR-xxx` for functional requirements, `NFR-xxx` for non-functional requirements, `UC-xx` for use cases, and `TC-xx` for test verification suites.
- Priority levels are categorized as **High**, **Medium**, or **Low** based on MoSCoW prioritization.
- Mathematical formulations follow standard financial amortization and risk scoring notations.

#### 1.3 Intended Audience & Reading Suggestions
This document is targeted towards academic evaluators, software architects, backend engineers, QA automation engineers, and financial compliance officers. Evaluators should review Section 2 for problem context, Section 4 for detailed functional requirements, and Section 5 for quality engineering benchmarks.

#### 1.4 Project Scope
The platform provides a decentralized marketplace connecting micro-borrowers seeking small-ticket loans (₹5,000 to ₹1,00,000) with retail peer lenders. It automates credit risk underwriting using deterministic heuristic algorithms, calculates structured reducing-balance repayment schedules, manages escrow-backed fractional loan commitments, handles payment gateway settlement callbacks, and enforces automated default warning escalations.

#### 1.5 References
1. IEEE Std 830-1998: *Recommended Practice for Software Requirements Specifications*.
2. Reserve Bank of India (RBI): *Master Directions – Non-Banking Financial Company - Peer to Peer Lending Platform (Reserve Bank) Directions, 2017*.
3. Use-Case & Component Modeling Guidelines, PES University Dept. of CSE (Labs 1 & 3).

---

### 2. Overall Description

#### 2.1 Product Perspective
The Micro-Lending platform operates as an independent web- and API-driven financial system. It replaces high-friction manual underwriting with algorithmic assessment and interfaces with third-party payment gateways (UPI/IMPS/NetBanking) and automated SMS/email communication gateways.

```
+-------------------------------------------------------------------+
|                        Client Applications                        |
|       [Borrower Web/Mobile UI]        [Peer Lender Investor UI]   |
+---------------------------------+---------------------------------+
                                  | HTTPS / REST / JSON
+---------------------------------v---------------------------------+
|               3-Tier Application & Business Logic Layer           |
|  +--------------------+  +------------------+  +---------------+  |
|  | Loan & KYC Manager |  | Credit Risk Eng. |  | Amortization  |  |
|  +--------------------+  +------------------+  +---------------+  |
|  +--------------------+  +------------------+  +---------------+  |
|  | P2P Escrow Market  |  | Settlement Svc.  |  | Default Watch |  |
|  +--------------------+  +------------------+  +---------------+  |
+---------------------------------+---------------------------------+
                                  | SQL / ACID Transactions
+---------------------------------v---------------------------------+
|                   Data Persistence & External APIs                |
|       [PostgreSQL Ledger]   [Payment Gateway]   [SMS/Email API]   |
+-------------------------------------------------------------------+
```

#### 2.2 Product Functions
1. **Borrower Ingestion & KYC:** Capturing verifiable borrower data (income, debt obligations, employment category, tenure).
2. **Deterministic Heuristic Risk Scoring:** Computing Debt-to-Income (DTI), stability indices, risk tiers (`Low`, `Medium`, `High`), and risk-adjusted APRs.
3. **Amortization Scheduling:** Emitting monthly reducing-balance EMI schedules.
4. **Peer Funding & Escrow Allocation:** Aggregating fractional investments from multiple peer lenders until loan is 100% committed.
5. **Installment Processing & Payouts:** Splitting borrower repayments into proportional lender dividends inside atomic database transactions.
6. **Default & Delinquency Management:** Monitoring due dates, issuing $T+3$ day grace period warnings, applying late penalties, and triggering $T+15$ day formal default proceedings.

#### 2.3 User Classes & Characteristics
- **Borrower:** Individuals seeking short-term micro-loans; expected to have basic smartphone/web literacy; interacts with loan application, KYC upload, and repayment modules.
- **Peer Lender:** Retail investors seeking yield; interacts with loan discovery filters, risk tier analytics, investment commitment, and portfolio dividend reports.
- **Platform Administrator / Compliance Auditor:** Inspects platform-wide non-performing asset (NPA) rates, escrow ledger reconciliation, and regulatory compliance logs.

#### 2.4 Operating Environment
- **Server OS:** Ubuntu Linux 22.04 LTS / macOS Darwin (arm64/x86_64).
- **Backend Runtime:** Python 3.10+ / FastAPI / Flask with ASGI server (Uvicorn).
- **Database:** PostgreSQL 15+ supporting serializable transactions and row-level locking.
- **Client Requirements:** Modern web browsers (Chrome 110+, Safari 16+, Firefox 110+).

#### 2.5 Design & Implementation Constraints
1. **Regulatory Mandate:** NBFC-P2P regulations dictate that lender funds must remain strictly segregated in nodal/escrow accounts and cannot touch company operational balance sheets.
2. **ACID Transaction Constraint:** Ledger balance conservation must be guaranteed mathematically ($\sum \Delta \text{Debits} = \sum \Delta \text{Credits}$).
3. **Zero Plaintext Storage:** Sensitive bank account details and tax identification numbers must be encrypted via AES-256-GCM.

---

### 3. External Interface Requirements

#### 3.1 User Interfaces
- **Borrower Dashboard:** Responsive web interface providing a 3-step application wizard, interactive EMI calculator, KYC upload status, and installment repayment button.
- **Lender Marketplace:** Searchable grid displaying open loans with filter chips for Risk Tier (`Low`, `Medium`, `High`), Tenure, Interest Rate, and funding progress bar.

#### 3.2 Software Interfaces
- **Payment Gateway API:** Webhook and REST API (e.g., Razorpay/Cashfree) supporting payment initiation, instant settlement verification, and automated refunds.
- **Notification Dispatcher:** REST API integration with SMS and transactional email services (Twilio, SendGrid) for automated due-date notifications.
- **Database Engine:** PostgreSQL via SQLAlchemy / Psycopg3 connection pooling with strict isolation levels.

---

### 4. System Features & Functional Requirements

#### 4.1 Credit Risk Heuristic Evaluation Engine (FR-001)
- **Description:** Evaluates borrower creditworthiness using deterministic heuristic scoring rules.
- **Inputs:** Monthly Income ($I$), Existing Monthly Debt Payments ($D$), Employment Category (Salaried / Self-Employed), Employment Tenure ($M$ months), Past On-time Payment Ratio ($R$).
- **Heuristic Formulas:**
  1. $\text{Debt-to-Income (DTI)} = \frac{D}{I} \times 100\%$
  2. $\text{DTI Score} = \max(0, 100 - (\text{DTI} \times 1.5))$
  3. $\text{Employment Score} = \min(100, M \times 2.5) \times (\text{1.1 if Salaried else 1.0})$
  4. $\text{Repayment History Score} = R \times 100$
  5. $\text{Composite Credit Score} = 300 + 5.5 \times (0.45 \cdot \text{DTI Score} + 0.30 \cdot \text{Repayment Score} + 0.25 \cdot \text{Employment Score})$
- **Tier Classification:**
  - $\text{Score} \ge 720 \implies \textbf{Low Risk}$ (APR: $10.5\%$, Max Principal: ₹1,00,000)
  - $600 \le \text{Score} < 720 \implies \textbf{Medium Risk}$ (APR: $15.0\%$, Max Principal: ₹50,000)
  - $450 \le \text{Score} < 600 \implies \textbf{High Risk}$ (APR: $22.0\%$, Max Principal: ₹15,000)
  - $\text{Score} < 450 \text{ or DTI} > 60\% \implies \textbf{Auto-Rejected}$

#### 4.2 Amortization & Repayment Schedule Generator (FR-002)
- **Description:** Produces an exact monthly amortization breakdown based on reducing balance interest.
- **Mathematical Formula:**
  $$\text{EMI} = P \times \frac{r(1+r)^n}{(1+r)^n - 1}$$
  where $P$ is principal, $r = \frac{\text{APR}}{12 \times 100}$ is monthly interest rate, and $n$ is tenure in months.
- **Schedule Table Output:** Month Number, Due Date, Beginning Balance, Monthly EMI, Principal Component, Interest Component, Ending Balance.
- **Validation:** Aggregate sum of principal installments must equal sanctioned principal $P$ to within $\pm \text{₹}0.50$.

#### 4.3 P2P Lending Marketplace & Escrow Allocation (FR-003)
- **Description:** Exposes approved loans to verified peer lenders, accepts fractional funding commitments (minimum ticket: ₹1,000), and locks funds in escrow.
- **Rules:**
  - Prevents overfunding: If loan requested principal is ₹20,000 and current funding is ₹18,000, max allowed commitment is ₹2,000.
  - When total funded amount equals $P$, the loan state atomically transitions from `OPEN_FOR_FUNDING` to `FULLY_FUNDED`.

#### 4.4 Repayment Settlement & Proportional Dividend Distribution (FR-004)
- **Description:** Processes borrower repayments and disburses proportional dividends to all lenders who funded that loan.
- **Mathematical Rule:**
  $$\text{Lender Dividend}_i = \text{Installment Amount} \times \frac{\text{Lender Commitment}_i}{P}$$
- **Execution:** Must execute within an ACID database transaction. If any ledger credit fails, the entire transaction rolls back.

#### 4.5 Automated Default Monitoring & Warning Service (FR-005)
- **Description:** Evaluates all active repayment installments on a daily batch schedule.
- **Workflow:**
  - Due Date Passed ($T+0$ to $T+3$): Normal grace period; gentle email notification.
  - Grace Period Expired ($T+3$): Formal First Overdue Warning; late fee of 2% added to unpaid installment.
  - Delinquent ($T+15$): Formal Default Notice; borrower risk rating downgraded to `High`; platform collection agent alert triggered; lenders notified.

---

### 5. Non-Functional & Quality Attributes

#### 5.1 Performance & Concurrency (NFR-001)
- The system shall sustain 200 concurrent repayment and funding requests with 99th-percentile response latency $< 350\text{ ms}$.
- Database connections shall be managed via connection pooling with row-level pessimistic locking (`SELECT ... FOR UPDATE`) during wallet debit/credit operations to prevent race conditions.

#### 5.2 Security & Data Privacy (NFR-002)
- All network communications shall enforce TLS 1.3 encryption with strict cipher suites.
- Sensitive borrower PII (PAN, Aadhaar, Bank Account Numbers) shall be encrypted at rest using AES-256-GCM.
- Role-Based Access Control (RBAC) shall enforce strict data separation between Borrowers, Lenders, and Administrative staff.

#### 5.3 Reliability, Availability & Disaster Recovery
- Platform uptime target: $99.9\%$ operational availability during business hours.
- Automated daily database dumps and continuous write-ahead logging (WAL) archiving to off-site cloud storage guaranteeing $\text{RPO} \le 15\text{ minutes}$ and $\text{RTO} \le 1\text{ hour}$.

#### 5.4 Maintainability & Extensibility
- Clean modular design adhering to SOLID principles.
- Comprehensive test coverage ($\ge 90\%$ branch coverage) across all heuristic risk evaluation, amortization, and escrow calculation modules.
