function calculate(i){
 const small=(i.input_tokens*i.small_input_rate+i.output_tokens*i.small_output_rate)/1e6;
 const strong=(i.input_tokens*i.strong_input_rate+i.output_tokens*i.strong_output_rate)/1e6;
 const unit=i.lookup_per_request+(1-i.cache_hit_rate)*(i.strong_share*strong+(1-i.strong_share)*small);
 const opex=i.monthly_requests*unit+i.cloud_monthly;
 const capacity=i.hours_saved_monthly*i.loaded_hourly_rate,cash=capacity*i.cash_realization,net=cash-opex;
 const discount=(1+i.annual_discount)**(1/12)-1;
 let npv=-i.implementation;for(let m=1;m<=i.horizon_months;m++)npv+=net/(1+discount)**m;
 return {unit_cost_rub:unit,monthly_opex_rub:opex,monthly_capacity_value_rub:capacity,monthly_realized_benefit_rub:cash,monthly_net_cash_rub:net,payback_months:net>0?i.implementation/net:null,npv_rub:npv,horizon_roi:i.implementation?(net*i.horizon_months-i.implementation)/i.implementation:null};
}
if(typeof module!=="undefined")module.exports={calculate};
