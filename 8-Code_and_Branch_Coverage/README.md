# Lab 6–7: Code and branch coverage
Mudit Chaturvedi — PES1UG24CS279

Application under analysis: `5-Github_Copilot_Generated_Code/credit_risk_assessor.py` (FR-001).
Scope is this application module; percentages do not describe the entire MicroLending project.

Code suite: 11 passing cases; 68/68 statements (100%).
Branch suite: 13 passing cases; 20/20 branches (100%), 0 partial branches.

Tests cover validation failures, repayment ratio boundaries, salaried/self-employed profiles, all risk tiers, excessive DTI, low-score rejection, exact borrowing limits and one unit above each limit.

Reproduce from repository root with Python, pytest and coverage installed:

```sh
python -m coverage run --include='*/credit_risk_assessor.py' -m pytest -q 8-Code_and_Branch_Coverage/CodeCoverageTest_credit_risk_assessor.py
python -m coverage report -m --fail-under=90
python -m coverage run --branch --include='*/credit_risk_assessor.py' -m pytest -q 8-Code_and_Branch_Coverage/BranchCoverageTest_credit_risk_assessor.py
python -m coverage report -m --fail-under=90
```

Reports contain real captured process output. HTML renders that output for viewing; JSON contains machine-readable measurements.
