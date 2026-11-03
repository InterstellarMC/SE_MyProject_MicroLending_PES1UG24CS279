import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '5-Github_Copilot_Generated_Code'))
from credit_risk_assessor import CreditRiskAssessor, FinancialProfile, RiskTier

@pytest.mark.parametrize('debt,tenure,history,salaried,tier,apr,limit', [
    (0,40,1,True,RiskTier.LOW,10.5,100000),
    (20000,20,0.9,False,RiskTier.MEDIUM,15,50000),
    (30000,12,0.8,True,RiskTier.HIGH,22,15000),
])
def test_tiers_and_limits(debt,tenure,history,salaried,tier,apr,limit):
    p=FinancialProfile(50000,debt,tenure,salaried,history)
    for amount,approved in [(limit,True),(limit+1,False)]:
        r=CreditRiskAssessor().evaluate(p,amount)
        assert (r.risk_tier,r.recommended_apr,r.max_borrowing_limit)==(tier,apr,limit)
        assert r.is_approved is approved
        assert (r.rejection_reason is None) is approved
        assert r.debt_to_income_ratio == debt/500

@pytest.mark.parametrize('debt,tenure,history',[(30001,40,1),(30000,0,0)])
def test_rejections(debt,tenure,history):
    r=CreditRiskAssessor().evaluate(FinancialProfile(50000,debt,tenure,False,history),1)
    assert r.risk_tier == RiskTier.REJECTED
    assert not r.is_approved and r.max_borrowing_limit == 0
    assert r.rejection_reason

@pytest.mark.parametrize('values,amount,message',[
    ((0,0,0,False,1),1,'income'),
    ((50000,-1,0,False,1),1,'debt'),
    ((50000,0,-1,False,1),1,'tenure'),
    ((50000,0,0,False,-0.01),1,'ratio'),
    ((50000,0,0,False,1.01),1,'ratio'),
    ((50000,0,0,False,1),0,'positive'),
])
def test_validation(values,amount,message):
    with pytest.raises(ValueError,match=message):
        CreditRiskAssessor().evaluate(FinancialProfile(*values),amount)
