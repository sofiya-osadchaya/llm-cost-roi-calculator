const test=require('node:test'),assert=require('node:assert/strict');
const {calculate}=require('../model.js'),base=require('../scenario.json');
test('zero realized cash never gives positive cash payback',()=>assert.equal(calculate({...base,cash_realization:0}).payback_months,null));
test('reject invalid shares, horizon, booleans and missing fields',()=>{for(const patch of [{cache_hit_rate:2},{horizon_months:121},{monthly_requests:true},{input_tokens:1.1},{cloud_monthly:NaN},{cash_realization:undefined}])assert.throws(()=>calculate({...base,...patch}));});
test('NPV with zero discount reconciles to net cash less implementation',()=>{const i={...base,annual_discount:0},r=calculate(i);assert.ok(Math.abs(r.npv_rub-(r.monthly_net_cash_rub*i.horizon_months-i.implementation))<1e-7)});
