function calculate(i){
 const required=['monthly_requests','input_tokens','output_tokens','small_input_rate','small_output_rate','strong_input_rate','strong_output_rate','strong_share','cache_hit_rate','lookup_per_request','cloud_monthly','hours_saved_monthly','loaded_hourly_rate','cash_realization','implementation','annual_discount','horizon_months'];
 for(const key of required)if(typeof i[key]!=='number'||!Number.isFinite(i[key])||i[key]<0)throw new Error('Invalid '+key);
 for(const key of ['strong_share','cache_hit_rate','cash_realization'])if(i[key]>1)throw new Error('Share outside 0..1: '+key);
 for(const key of ['monthly_requests','input_tokens','output_tokens','horizon_months'])if(!Number.isInteger(i[key]))throw new Error('Integer required: '+key);
 if(i.horizon_months<1||i.horizon_months>120)throw new Error('Horizon must be 1..120');
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
