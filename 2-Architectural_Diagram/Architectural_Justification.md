# Architectural Pattern Selection & Justification

**Course:** Software Engineering (UE24CS341A) — Lab 3: Component Modelling & Architectural Pattern Selection  
**Department:** Computer Science & Engineering, PES University  
**Student Name:** Mudit Chaturvedi  
**SRN:** PES1UG24CS279  
**Assigned System:** Problem Statement #33 — Micro-Lending & Peer Credit Risk Assessor  

---

### Architecture Selection
> **"We chose a 3-Tier Layered Architecture with Service-Oriented Component Decoupling for the Micro-Lending & Peer Credit Risk Assessor System."**

---

### 1. Architectural Choice
For the Micro-Lending & Peer Credit Risk Assessor platform, we selected a **3-Tier Layered Architecture** augmented with clear component-level boundary encapsulation (Presentation Layer, Business Application Layer, and Data Persistence / External Integration Layer). Each layer interacts strictly through well-defined provided and required interfaces (such as `ICreditAssessment`, `IScheduleGenerator`, `IEscrowFunding`, and `IPaymentSettlement`). This structure maintains high cohesion within modules while decoupling volatile front-end investor/borrower workflows from mission-critical risk underwriting and financial settlement operations.

---

### 2. Two Specific Scenario-Related Reasons

1. **Strict Separation of Non-Deterministic Heuristic Risk Logic from Transactional Settlement:**  
   The platform’s core functional requirement (`FR-001`) relies on heuristic credit scoring algorithms based on Debt-to-Income (DTI) ratios, employment stability, and repayment history indices. These mathematical heuristics and credit policy thresholds evolve rapidly as underwriting models are tuned. By isolating the `CreditRiskEngine` behind the `ICreditAssessment` interface within the Business Layer, algorithm modifications or weight adjustments can be iterated, re-tested, and deployed without risking side-effects on the double-entry accounting ledger, loan disbursement logic, or database schema.

2. **Guaranteed Transactional Atomicity and Escrow State Consistency (`FR-003`, `FR-004`):**  
   In a peer-to-peer lending ecosystem, fractional lender commitments and borrower repayments must strictly preserve ledger balance conservation (i.e., money debited from a borrower must match the exact proportional credits disbursed across participating lenders' escrow accounts). A layered architecture allows transactional management to be centralized strictly within the `Payment Gateway & Settlement Service` and the underlying ACID relational database, completely preventing presentation components or unprivileged services from directly executing uncontrolled ledger mutations.

---

### 3. Security Advantage
**Isolation of Sensitive Financial PII and Escrow Funds via Tiered Access Control:**  
Borrower financial profiles, bank account numbers, tax identifiers, and credit bureau histories represent highly sensitive Personally Identifiable Information (PII) governed by strict financial data privacy regulations (RBI NBFC-P2P norms). The layered architecture establishes strict network and permission boundaries: client-facing presentation components (`Borrower Portal UI`, `Peer Lender UI`) never have direct database access. All data access requests pass through the application layer where authentication, authorization, and AES-256 field-level encryption/decryption are enforced. Consequently, even if a client portal interface is compromised, an attacker cannot execute raw SQL injections or access unencrypted financial ledgers.

---

### 4. Performance Benefit
**Asynchronous Batch Processing and Targeted Query Caching Without Contention on Financial Writes:**  
The layered component structure separates high-throughput, read-heavy operations (e.g., hundreds of peer lenders browsing active loan opportunities on the marketplace) from write-intensive, ACID-locked operations (loan disbursements and installment settlements). Read-heavy marketplace queries can be cached at the Application Layer using an in-memory Redis cache without placing lock contention on the relational ledger. Concurrently, compute-intensive processes such as daily default monitoring (`DefaultMonitorService`) and amortization schedule recalculations run as decoupled background jobs, ensuring that the interactive user response latency for repayment processing remains consistently below $250\text{ ms}$.
