"""Illustrative RUB scenario model, not market pricing or financial advice."""
from dataclasses import dataclass,asdict
import argparse,json,math
from pathlib import Path

@dataclass
class Inputs:
    monthly_requests: int=10000
    input_tokens: int=900
    output_tokens: int=160
    small_input_rate: float=60
    small_output_rate: float=120
    strong_input_rate: float=700
    strong_output_rate: float=1400
    strong_share: float=0.25
    cache_hit_rate: float=0.3
    lookup_per_request: float=0.01
    cloud_monthly: float=2000
    hours_saved_monthly: float=100
    loaded_hourly_rate: float=900
    cash_realization: float=0.4
    implementation: float=180000
    annual_discount: float=0.12
    horizon_months: int=12
    def __post_init__(self):
        for k,v in asdict(self).items():
            if not isinstance(v,(float,int)) or not math.isfinite(v) or v<0: raise ValueError(f"Invalid {k}")
        for k in ("cache_hit_rate","strong_share","cash_realization"):
            if not 0<=getattr(self,k)<=1: raise ValueError(f"Invalid {k}")
        if self.horizon_months<1 or int(self.horizon_months)!=self.horizon_months: raise ValueError("Invalid horizon")

def calculate(i):
    small=(i.input_tokens*i.small_input_rate+i.output_tokens*i.small_output_rate)/1e6
    strong=(i.input_tokens*i.strong_input_rate+i.output_tokens*i.strong_output_rate)/1e6
    mix=i.strong_share*strong+(1-i.strong_share)*small
    unit=i.lookup_per_request+(1-i.cache_hit_rate)*mix
    opex=i.monthly_requests*unit+i.cloud_monthly
    capacity=i.hours_saved_monthly*i.loaded_hourly_rate
    cash=capacity*i.cash_realization
    net=cash-opex
    monthly_discount=(1+i.annual_discount)**(1/12)-1
    npv=-i.implementation+sum(net/(1+monthly_discount)**m for m in range(1,i.horizon_months+1))
    return {"unit_cost_rub":unit,"monthly_opex_rub":opex,"monthly_capacity_value_rub":capacity,
            "monthly_realized_benefit_rub":cash,"monthly_net_cash_rub":net,
            "payback_months":i.implementation/net if net>0 else None,"npv_rub":npv,
            "horizon_roi":(net*i.horizon_months-i.implementation)/i.implementation if i.implementation else None}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--inputs",default="scenario.json");p.add_argument("--compare-cache",action="store_true");a=p.parse_args()
    i=Inputs(**json.loads(Path(a.inputs).read_text()));out={"cached":calculate(i)}
    if a.compare_cache: out["without_cache"]=calculate(Inputs(**{**asdict(i),"cache_hit_rate":0}))
    print(json.dumps(out,indent=2))
