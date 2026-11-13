# LLM Cost and ROI Calculator

демо-реконструкция подхода на синтетических данных

A C-level business-case example separating released staff capacity from realized cash benefit.
Rates and volumes are invented RUB assumptions, not provider prices. No employer economics are used.

- `python calculator.py --compare-cache` evaluates the supplied scenario.
- Open `index.html` for interactive assumptions.
- Open `business_case.xlsx` for editable Excel formulas, cached/no-cache comparison and discounted cash flow.
- `python -m unittest discover -s tests` verifies negative cases and financial arithmetic.

All three interfaces use input and output rates per million tokens, weighted routing and cache misses.
Lookup cost is paid for every request. Monthly cloud cost is added separately. Cache changes token OPEX,
not assumed staff time. Cash realization is explicit. Payback is null when net benefit is nonpositive;
NPV discounts month-end cash flows with `(1+annual_rate)^(1/12)-1`. No tax or terminal value is assumed.
MIT. Business-case formulas are illustrative scenario arithmetic.
