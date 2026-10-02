# Work Breakdown Structure (WBS)
## Micro-Lending & Peer Credit Risk Assessor (Problem Statement #33)

**Course:** Software Engineering (UE24CS341A)  
**Student Name:** Mudit Chaturvedi (SRN: PES1UG24CS279)  
**Agile Project Reference:** `KBPS33` & `SBPS33` (`mudit300477.atlassian.net`)  

---

### 1. Hierarchical Work Breakdown Structure

```
1.0 Inception & Requirements Engineering (Lab 1)
  ├── 1.1 Problem Statement Analysis & Stakeholder Identification
  ├── 1.2 Functional Requirements Formulation (FR-001 to FR-005)
  ├── 1.3 Non-Functional Requirements Definition (NFR-001 & NFR-002)
  ├── 1.4 Use-Case Identification & Actor Modeling
  ├── 1.5 UML Use-Case Diagram Construction (Draw.io)
  └── 1.6 Use-Case Flow Specification (UC-01 Core Scenario & Alternates)

2.0 Architectural Design & Component Modeling (Lab 3)
  ├── 2.1 Architectural Style Evaluation (Layered vs Microservices vs Client-Server)
  ├── 2.2 3-Tier Layered Architecture Pattern Selection
  ├── 2.3 Identification of Core Subsystem Components (6 Components)
  ├── 2.4 Interface Definition with Ball & Socket Notation (4+ Interfaces)
  ├── 2.5 UML Component Diagram Rendering & Validation
  └── 2.6 Written Architectural Justification (Word/PDF Documentation)

3.0 Agile Planning & Project Creational Tracking (Lab 2)
  ├── 3.1 Atlassian Jira Cloud Workspace Provisioning
  ├── 3.2 Kanban Board Configuration (WIP Limits, Epic Categorization)
  ├── 3.3 Scrum Project Setup & Story Point Estimation (Fibonacci Scale)
  ├── 3.4 Sprint 1 Backlog Grooming & Execution (Velocity: 21 pts)
  ├── 3.5 Sprint 2 Backlog Grooming & Execution (Velocity: 26 pts)
  └── 3.6 Defect Logging, Triage & Burndown Analysis

4.0 Core Micro-Lending Implementation (Implementation & Copilot)
  ├── 4.1 Borrower Credit Risk Evaluation Engine (`credit_risk_assessor.py`)
  │     ├── 4.1.1 Debt-to-Income (DTI) Heuristic Calculation
  │     ├── 4.1.2 Repayment History Scoring Index
  │     ├── 4.1.3 Employment Stability & Category Weighting
  │     └── 4.1.4 Risk Tiering (`Low`, `Med`, `High`) & Interest Rate Mapping
  ├── 4.2 Reducing Balance Amortization Engine (`amortization_schedule.py`)
  │     ├── 4.2.1 Monthly EMI Mathematical Formulation
  │     ├── 4.2.2 Principal and Interest Component Split
  │     └── 4.2.3 Amortization Schedule Table Generation
  ├── 4.3 P2P Marketplace & Escrow Module (`escrow_marketplace.py`)
  │     ├── 4.3.1 Fractional Lender Funding Commitments
  │     ├── 4.3.2 Escrow Balance Reservation & Locking
  │     └── 4.3.3 Overfunding Guardrails & Automatic State Transition
  ├── 4.4 Repayment & Dividend Distribution Ledger (`main.py`)
  │     ├── 4.4.1 ACID Repayment Settlement Processing
  │     └── 4.4.2 Proportional Lender Dividend Disbursement
  └── 4.5 Automated Default Monitoring Service (`default_monitor.py`)
        ├── 4.5.1 Grace Period (T+3) Tracking & Notification Dispatch
        └── 4.5.2 Delinquency (T+15) Default Warning & Risk Downgrade

5.0 Software Testing & Quality Verification (Testing Practice)
  ├── 5.1 Test Plan & Test Case Formulation (TC-01 through TC-08)
  ├── 5.2 Unit Testing for Heuristic Underwriting (Pytest)
  ├── 5.3 Boundary Value & Equivalence Partitioning Analysis (DTI > 60%, Negative Tenure)
  ├── 5.4 Financial Precision Testing (Float Variance & Rounding $\le$ ₹0.50)
  ├── 5.5 ACID Rollback Simulation & Ledger Consistency Verification
  └── 5.6 Vibe Coding Defect Patching & Retesting Documentation
```

---

### 2. Work Package Dictionary & Effort Estimation

| WBS Code | Work Package Title | Primary Deliverable | Sprint | Est. Hours | Lead |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1.1–1.3** | Requirements Elicitation | `Requirements_Specification.md`, RTM Table | Sprint 1 | 8 hrs | Mudit C. |
| **1.4–1.6** | Use-Case Modeling | `UML_Use_Case_Diagram.png`, Flow Spec | Sprint 1 | 6 hrs | Mudit C. |
| **2.1–2.6** | Component Modeling | `Component_Diagram.png`, Justification Doc | Sprint 1 | 10 hrs | Mudit C. |
| **3.1–3.6** | Agile Setup & Jira Tracking | Jira Boards, Burndown Reports, Bug Log | Sprints 1–2 | 8 hrs | Mudit C. |
| **4.1** | Credit Risk Engine | `credit_risk_assessor.py` | Sprint 1 | 12 hrs | Mudit C. |
| **4.2** | Amortization Scheduler | `amortization_schedule.py` | Sprint 1 | 8 hrs | Mudit C. |
| **4.3** | P2P Escrow Marketplace | `escrow_marketplace.py` | Sprint 2 | 14 hrs | Mudit C. |
| **4.4** | Payment Ledger & Payouts | `main.py` (Core Engine) | Sprint 2 | 16 hrs | Mudit C. |
| **4.5** | Default Monitoring Daemon | `default_monitor.py` | Sprint 2 | 10 hrs | Mudit C. |
| **5.1–5.6** | Automated Test Verification | `test_micro_lending.py`, Test Report | Sprint 2 | 14 hrs | Mudit C. |
| **Total** | **Project Lifecycle** | **Complete Submission Repository** | **All** | **106 hrs** | — |
