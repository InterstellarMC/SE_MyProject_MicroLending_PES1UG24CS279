# Project Creational & Agile Project Management Documentation
## Jira Software & GitHub Setup (Problem Statement #33)

**Course:** Software Engineering (UE24CS341A) — Lab 2  
**Department:** Computer Science & Engineering, PES University  
**Student Name:** Mudit Chaturvedi  
**SRN:** PES1UG24CS279  
**Jira Site:** `mudit300477.atlassian.net`  
**GitHub Repository:** `MyProject_MicroLending`  

---

### 1. Jira Workspace & Project Structure

The project was managed using Atlassian Jira Software Cloud with two distinct project configurations to practice Agile development frameworks for the **Micro-Lending & Peer Credit Risk Assessor** system:

| Project Name | Project Key | Type | Framework | Core Purpose |
| :--- | :---: | :---: | :---: | :--- |
| **Kanban_BPS#33** | `KBPS33` | Company-Managed | Kanban | Continuous delivery tracking, Epic mapping for FR-001 through FR-005, and workflow bottleneck visualization. |
| **Scrum_BPS#33** | `SBPS33` | Company-Managed | Scrum | Iterative timeboxed sprint execution (Sprint 1: Core Underwriting & Schedules; Sprint 2: Marketplace, Payouts & Alerts) with story point estimation. |

---

### 2. Epics & Requirements Mapping

Every functional requirement from Lab 1 was decomposed into Epics, User Stories, and Technical Tasks in Jira:

1. **Epic 1 (`KBPS33-E1` / `SBPS33-E1`): Borrower Onboarding & Credit Risk Engine (FR-001)**
   - User Story: *As a system underwriter, I want to calculate borrower credit risk tiers based on DTI and employment tenure, so that peer lenders have objective risk indicators.*
   - Estimation: 8 Story Points.
2. **Epic 2 (`KBPS33-E2` / `SBPS33-E2`): Amortization & Repayment Scheduling (FR-002)**
   - User Story: *As a borrower, I want to view a transparent reducing-balance EMI schedule, so that I can budget for monthly installment obligations.*
   - Estimation: 5 Story Points.
3. **Epic 3 (`KBPS33-E3` / `SBPS33-E3`): Peer Lending Marketplace & Escrow Allocation (FR-003)**
   - User Story: *As a peer lender, I want to review vetted loan requests and fund fractional portions, so that I can diversify my lending capital safely.*
   - Estimation: 8 Story Points.
4. **Epic 4 (`KBPS33-E4` / `SBPS33-E4`): Installment Processing & Proportional Payouts (FR-004, NFR-001)**
   - User Story: *As a lender, I want borrower repayments to disburse dividends into my escrow wallet atomically, so that ledger balances remain 100% consistent.*
   - Estimation: 13 Story Points.
5. **Epic 5 (`KBPS33-E5` / `SBPS33-E5`): Automated Default Monitoring & Warning Service (FR-005)**
   - User Story: *As a platform administrator, I want automated daily batch scripts to trigger default notices past grace periods, so that delinquent loans are addressed immediately.*
   - Estimation: 5 Story Points.

---

### 3. Sprint Execution & Burndown Analytics

- **Sprint 1 (Velocity: 21 Points):** Focused on foundational architecture, borrower KYC verification, heuristic credit scoring formulas, and mathematical verification of reducing-balance EMI algorithms. Completed on schedule with zero scope creep.
- **Sprint 2 (Velocity: 26 Points):** Focused on payment gateway integration, ACID escrow ledger guarantees, peer lender fractional funding logic, and automated default alerting triggers.
- **Burndown Analysis:** Monitored daily burnup/burndown trends (`06_scrum_burndown_sprint2.png`, `07_scrum_burndown_sprint1.png`) verifying steady task completion without sprint-end cramming.

---

### 4. Index of Screenshots & Submission Artifacts

| Screenshot / Document | Description |
| :--- | :--- |
| `01_kanban_board_epics_fr.png` | Kanban board showing Work-In-Progress (WIP) limits, columns (`Backlog`, `In Progress`, `Code Review`, `Done`), and active Epics. |
| `02_kanban_board_more_epics.png` | Detailed swimlanes grouped by Epics (FR-001 to FR-005) on the Kanban board. |
| `03_kanban_list_epics_backlog.png` | Product backlog prioritized by risk and dependencies. |
| `04_scrum_backlog_sprint2_points.png` | Scrum Sprint 2 backlog showing story point allocations (Fibonacci scale) and acceptance criteria. |
| `05_scrum_active_sprint_done.png` | Active Scrum sprint board during sprint closure with all sprint goals completed. |
| `06_scrum_burndown_sprint2.png` | Sprint 2 Burndown chart comparing guideline velocity against actual task completion. |
| `07_scrum_burndown_sprint1.png` | Sprint 1 Burndown chart showing initial velocity calibration. |
| `08_bug_board_all_bugs.png` | Dedicated QA defect board showing logged bug tickets (e.g., float rounding variance, edge-case DTI calculations) and their verified resolutions. |
| `Mudit Chaturvedi_PES1UG24CS279-BPS#33.pdf` | Consolidated Lab 2 submission report submitted on PES University portal. |
| `Kanban.PDF` & `Scrum.PDF` | Individual module exports for Kanban and Scrum practices. |
| `BugReport.PDF` | Formal bug triage and defect lifecycle documentation. |
