# Lab 5 submission

Read `Lab_5_Report.md` for the issue table and reflections, or use the PDF
in `output/pdf/`. The corrected code is in
`../5-Github_Copilot_Generated_Code/`.

From the repository root, create a separate environment and run:

```sh
python3 -m venv .venv-lab5
.venv-lab5/bin/python -m pip install -r 7-Static_Code_Analysis/requirements.txt
.venv-lab5/bin/pylint 5-Github_Copilot_Generated_Code/*.py
.venv-lab5/bin/bandit -r 5-Github_Copilot_Generated_Code
.venv-lab5/bin/flake8 5-Github_Copilot_Generated_Code
.venv-lab5/bin/pytest -q 6-Software_Testing_Tools/test_micro_lending.py
.venv-lab5/bin/python 5-Github_Copilot_Generated_Code/main.py
```

Pylint's refactor suggestions give exit code 8; its final score is 9.61.
The Flake8 report is empty because there are no findings.
The Bandit review commit records zero original security findings.
No security bug is claimed to have been fixed.
