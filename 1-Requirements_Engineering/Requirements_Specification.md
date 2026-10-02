# Requirements Engineering & Traceability Specification
## Micro-Lending & Peer Credit Risk Assessor (Problem Statement #33)

**Course:** Software Engineering (UE24CS341A) — Lab 1  
**Department:** Computer Science & Engineering, PES University  
**Student Name:** Mudit Chaturvedi  
**SRN:** PES1UG24CS279  
**Domain:** Retail, E-Commerce & Finance  

---

### 1. Problem Context & Overview

The **Micro-Lending & Peer Credit Risk Assessor** platform is a decentralized peer-to-peer (P2P) micro-finance system designed to connect unbanked and underbanked individual borrowers with retail peer lenders. Conventional banking institutions enforce rigid underwriting guidelines that often exclude individuals with thin credit files or informal income sources.

This platform bridges that credit gap by:
1. **Evaluating Borrower Risk:** Calculating borrower creditworthiness using objective heuristic rules based on debt-to-income (DTI) ratio, historical repayment discipline, and employment stability indices.
2. **Structured Amortization Schedules:** Producing transparent, reducing-balance Equated Monthly Installment (EMI) schedules upon loan approval.
3. **Escrow-Backed P2P Funding:** Allowing peer lenders to review anonymized loan listings and commit capital in fractional amounts while locking funds in compliant escrow accounts.
4. **Automated Risk & Default Monitoring:** Tracking repayment timelines in real-time, executing atomic dividend distributions to lenders, and automatically issuing tiered default warnings and penalty workflows when payment windows lapse.

**Primary System Actors:**
- **Borrower:** Applies for micro-loans, provides financial/KYC credentials, views repayment schedules, and fulfills installment obligations.
- **Peer Lender:** Browses vetted loan requests filtered by risk tiers, commits funding allocations, and receives automated dividend payouts.
- **Payment Gateway (Secondary Actor):** Processes outward and inward payment settlements via bank transfers/UPI.
- **Automated Scheduler / Notification Daemon (Secondary Actor):** Triggers daily batch monitoring for due dates, grace periods, and escalation notices.

---

### 2. Functional Requirements (FR-001 to FR-005)

| Requirement ID | Priority | Description | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **FR-001** | **High** | The system shall compute borrower credit risk ratings and numerical scores (range: 300–850) using deterministic heuristic rules derived from debt-to-income (DTI) ratio, verified repayment history, and employment stability indicators. | **Pass:** Risk tier (`Low`, `Medium`, `High`) is accurately assigned based on validated financial data, accompanied by a calculated maximum borrowing limit and benchmark interest rate.<br>**Fail:** The system approves credit or assigns a risk tier when mandatory financial parameters (monthly income, existing debts, employment tenure) are missing, incomplete, or out of range. | Underwrites loan requests without human bias while protecting peer lender capital against non-creditworthy applicants. |
| **FR-002** | **High** | The system shall generate a structured loan repayment schedule detailing the reducing-balance EMI, monthly principal/interest split, payment deadlines, and residual balance upon application approval. | **Pass:** A full amortization schedule is computed where the aggregate sum of principal payments exactly equals the sanctioned principal (rounding difference $\le \text{₹}0.50$) and installments follow reducing balance formulas.<br>**Fail:** The schedule exhibits negative amortization, mismatched aggregate principal, or generates without binding loan terms. | Gives borrowers predictable repayment obligations and provides peer lenders with projected cash flow horizons. |
| **FR-003** | **High** | The system shall enable authenticated Peer Lenders to browse active, verified loan requests, inspect anonymized risk profiles, and commit fractional or full funding up to the requested loan target. | **Pass:** Committed funds are deducted from the lender's wallet into an escrow hold, aggregate progress updates atomically, and the listing closes to 'Fully Funded' once target capital is met.<br>**Fail:** The system permits overfunding beyond the requested principal, or deducts lender funds without an atomic escrow lock. | Enables fractional micro-lending diversification, allowing lenders to distribute risk across multiple borrowers. |
| **FR-004** | **Medium** | The system shall process borrower installment repayments through an integrated payment gateway and execute atomic, proportional dividend disbursements directly to participating lenders' escrow ledgers. | **Pass:** Upon receipt of verified gateway callback, the installment status is marked `PAID`, borrower balance updates, and all participating lenders receive their exact fractional share of principal plus interest in a single database transaction.<br>**Fail:** Installment is debited from borrower but lenders' ledger balances fail to update, or payment is applied without gateway confirmation. | Preserves financial ledger integrity, ensures lender trust, and prevents discrepancies in peer profit distribution. |
| **FR-005** | **High** | The system shall monitor installment due dates and automatically trigger tiered default warnings, penalty interest additions, and borrower rating downgrades when grace periods expire. | **Pass:** At $T+3$ days past due date (grace period expiry), automated email/SMS reminders are dispatched; at $T+15$ days, formal default notices are issued, penalty interest is applied, and borrower risk tier is downgraded to `High`.<br>**Fail:** Default warnings trigger on on-time paid accounts, or warnings fail to fire within 24 hours of grace period lapse. | Enforces disciplined repayment cycles, minimizes non-performing assets (NPAs), and keeps lenders updated on delinquent loans. |

---

### 3. Non-Functional Requirements (NFR-001 & NFR-002)

| NFR ID | Category / Type | Priority | Requirement Description | Acceptance Criteria | Engineering Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NFR-001** | **Performance & Security** | **High** | Loan repayment processing, escrow allocations, and lender dividend disbursements must execute inside ACID-compliant database transactions with strict serializability to prevent double-spending and ledger inconsistency under concurrent load. | **Pass:** Load testing under 200 concurrent repayment requests demonstrates zero ledger discrepancies, 100% atomic rollbacks on simulated gateway failures, and 99th-percentile response latency $< 350\text{ ms}$.<br>**Fail:** Race conditions resulting in double debit/credit, phantom reads, or partial ledger state commits. | Financial micro-lending platforms manage real monetary balances. Even minor ledger drift or non-atomic commits create catastrophic financial liability and breach regulatory mandates. |
| **NFR-002** | **Reliability & Data Privacy** | **High** | All borrower Personally Identifiable Information (PII), bank account details, and credit records must be encrypted at rest using AES-256 and in transit using TLS 1.3, supported by automated incremental backups ensuring Recovery Point Objective (RPO) $\le 15\text{ minutes}$ and Recovery Time Objective (RTO) $\le 1\text{ hour}$. | **Pass:** Independent automated security scans verify no plaintext PII in databases or logs, all external communications enforce TLS 1.3 with HSTS, and disaster recovery simulation restores operational state within 45 minutes.<br>**Fail:** Plaintext storage of tax identifiers, banking tokens, or recovery time exceeding 60 minutes after primary node outage. | Protects sensitive financial data against unauthorized exfiltration, adheres to RBI NBFC-P2P regulatory guidelines, and ensures platform survivability. |

---

### 4. Requirements Traceability Matrix (RTM)

The Requirements Traceability Matrix bridges business problem specifications to software design elements, implementation modules, and test verification procedures:

| Req ID | Requirement Summary | Stakeholder / Source | Use Case ID | Architecture Component | Test Case ID | Status |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **FR-001** | Credit Risk Assessment | Borrower, Platform Underwriter | `UC-03` | Credit Risk Evaluation Engine | `TC-01`, `TC-02`, `TC-03` | Verified |
| **FR-002** | Repayment Schedule Generation | Borrower, Peer Lender | `UC-04` | Amortization & Schedule Engine | `TC-04` | Verified |
| **FR-003** | Peer Loan Marketplace & Funding | Peer Lender | `UC-05`, `UC-06` | P2P Marketplace & Escrow Service | `TC-05` | Verified |
| **FR-004** | Repayment & Dividend Distribution | Borrower, Peer Lender | `UC-07` | Payment & Settlement Gateway | `TC-06`, `TC-08` | Verified |
| **FR-005** | Automated Default Warnings | System Scheduler, Borrower | `UC-08`, `UC-09` | Default Monitor & Alerting Component | `TC-07` | Verified |
| **NFR-001** | ACID Transaction Integrity | Core Platform Architect | `UC-06`, `UC-07` | Payment & Settlement Gateway | `TC-08` | Verified |
| **NFR-002** | Data Privacy & Availability | Compliance Officer, System Admin | Cross-cutting | Infrastructure & Data Persistence Layer | `TC-03`, `TC-08` | Verified |
