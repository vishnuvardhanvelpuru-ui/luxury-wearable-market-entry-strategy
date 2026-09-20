# Case 3: Luxury Brand Paradox

**Fictional company: Maison Valenne, owned by Valenne Group. All customer records, financial inputs and scenario results are synthetic.** USD, US launch, 2027–2029. Reference date: 19 September 2026.

## Decision
Defer a commercial launch. The highest base-case entry NPV is co-branding at **-$2.55m**, compared with **$0 incremental NPV for no entry**. A separate sibling brand delivers **-$3.52m** and therefore does not win the investment test. It is a plausible architecture to test, not an approved launch. Even the defined upside scenarios remain negative (see strategy_summary.csv).

No entry is a modeled benchmark, not proof that delay is free: foregone learning, competitor response and long-term relevance are not valued. Three years may understate a durable brand investment, but there is no evidence here to justify a terminal value. Do not interpret synthetic findings as real consumer research.

## Business question and decision rules
Can wearables create incremental parent-company value while protecting mechanical profits? Require NPV > 0 at a 12% discount rate, annual displaced mechanical units <= 2% of baseline, and annual brand haircut <= 0.5%. These are explicit fictional management tolerances, applied equally to all options; they are not external industry standards. Avoid a subjective weighted score that could conceal a loss-making launch.

The baseline is 10,000 annual mechanical units, $6,000 net manufacturer revenue per unit and 65% contribution margin: $39m annual contribution before corporate fixed cost. It remains flat. Wearable operating cash is incremental; it excludes the baseline rather than adding it twice.

## Options and trade-offs
| Option | Base NPV | Main strength | Main weakness |
|---|---:|---|---|
| Heritage extension | -$6.27m | Recognition and premium pricing | Small affordable audience and 1.5% brand haircut |
| Separate sibling brand | -$3.52m | Lower assumed spillover; broader audience | $4m setup plus $1.8m yearly overhead |
| Co-brand partnership | -$2.55m | Lower investment and acquisition cost | 0.6% haircut exceeds 0.5% gate; shared control |
| Heritage licensing | -$4.18m | Limited capital requirement | Only 10% royalty realization; displaced mechanical margin overwhelms royalty |
| Modular hybrid | -$3.06m | Craft continuity and modest cannibalization | Niche demand and expensive hardware |

These are five mutually exclusive business packages, not a factorial experiment. Pricing, control and product form vary alongside branding. Supplier partnerships can support any architecture. The modular option is a heritage-branded analog-style hybrid with a service-replaceable electronic module; it is not a mechanical movement plus a full smartwatch. Licensing uses the heritage name, not the sibling name.

## Market and customer interpretation
The model defines a reachable US planning universe of 200,000 unique people across four mutually exclusive primary-need segments; this is an assumed serviceable audience, **not an estimate of the total smartwatch market**. Segment order resolves overlap: heritage collecting first, design-led professional second, wellness third, remaining price-led technology buyers last. The synthetic sample has 30 people per segment (120 total), with each rating five concepts (600 responses). Equal quotas are not population weights. Weight qualification rates by each assumed segment audience before projecting sales.

Qualified means interested AND stated maximum willingness-to-pay >= option price. A 12% calibration converts qualified reachable people to annual purchases, adjusted by option demand factor and year ramp (0.6, 1.0, 1.3). These are judgmental assumptions. The reach is an annual refreshed audience, so the three-year sum is not a unique customer count. No repeat-purchase behavior is inferred.

For the sibling concept at $950, prioritize design-led professionals for discovery, with wellness enthusiasts a secondary audience. Use segment_analysis.csv to compare qualified rates and projected units rather than sample interest alone. Heritage collectors have purchasing capacity but are a limited niche; value-focused buyers face a price mismatch. Ownership is descriptive and does not estimate actual switching.

## Competitor context
Apple's September 2025 Ultra 3 release gives a $799 US starting launch price and illustrates a technology-led proposition. TAG Heuer's specific E5 titanium reference was listed at $2,450 on the accessed US page, showing heritage extension exists. Withings' 2023 Nova announcement illustrates the hybrid route; its PDF has a placeholder price, so no price is used. These three references bound possible positioning; they do not establish market share, strategy success or a causal premium. Sources and dates: ../data/competitor_references.csv. Consumer features and commercial availability should be rechecked before an actual launch.

## Pricing and channel economics
The sibling option's $950 price is a test anchor between technology-led and heritage luxury references. A discrete $750/$950/$1,150/$1,350 test recalculates qualified demand using the same synthetic WTP responses, retaining concept interest. This is a rough demand screen, not a price-elasticity experiment. See pricing_test.csv; no tested price fixes the investment case. At $950 the company realizes $836 per sold unit and pays $330 hardware, $75 service/returns reserve and $95 acquisition: $336 contribution before fixed costs and heritage effects.

For a future sibling launch, assume 60% direct online at 96% net realization and 40% selected specialist retail at 76% wholesale realization: blended 88%. Excludes sales tax. These planning deductions include payment fees, planned discounts and channel economics; service reserve covers returns/warranty to avoid adding it again. Separate website and retail fixtures, no routine mechanical-watch bundles, no discounting through heritage boutiques. Validate this mix and cost of acquisition with real tests. Other strategies use their own blended realization assumptions, not this channel mix.

## Financial and brand risk
NPV = discounted annual incremental operating cash less initial investment at time zero. Cash = company revenue - variable costs - annual fixed cost - lost mechanical contribution - brand haircut on remaining mechanical contribution. Displaced mechanical units = wearable units × switching probability. A 1.2% switching assumption means 1.2 mechanical sales lost per 100 sibling devices; it is not a 1.2% drop in total mechanical sales. Brand haircut applies after displacement, avoiding double counting. It proxies price/mix erosion, not a measured valuation of brand equity.

The downside cuts demand 30%, raises variable cost 10% and multiplies switching and brand risk by 1.5. The upside raises demand 20%, lowers variable cost 5% and multiplies risks by 0.75. These bundles have no assigned probabilities. Volume-only sensitivity separately holds risk and costs fixed. Break-even multiples use unrounded annual units and are approximate. Licensing has negative contribution after displacement even before fixed costs; greater volume can destroy more value.

Model excludes tax, financing, terminal value, incremental working capital and post-2029 support obligations beyond the per-unit reserve. Cash therefore means an unlevered pre-tax operating-cash proxy, not audited free cash flow. Initial investment includes launch development/tooling; annual overhead includes ongoing software and team support. Supplier quotes must validate adequacy of reserves and end-of-support costs. No value assigned to customer data or halo effects.

## MECE issue tree
1. Demand: reachable segment size; need; willingness-to-pay; calibrated conversion. Outputs: units and mix.
2. Wearable economics: realized price; hardware/service/acquisition costs; fixed costs; initial investment. Outputs: direct contribution and cash.
3. Heritage externalities: displaced units; residual brand price/mix haircut. Outputs: incremental mechanical contribution lost.
4. Delivery feasibility: capabilities; supplier dependence; reliability; privacy and service commitments. Outputs: execution gates, not another financial penalty.
5. Decision resilience: scenario reversals; cash exposure; options to delay. Outputs: go/no-go and evidence thresholds.
Branches separate revenue drivers, direct cost, heritage effects, operational feasibility and decision uncertainty; qualitative risks are not charged twice in NPV.

## SWOT for a potential sibling brand
| Strengths | Weaknesses |
|---|---|
| Parent design, quality and supplier knowledge; separate identity offers a barrier to spillover | Unknown new name; software skills gap; setup costs and customer acquisition |
| Opportunities | Threats |
| Design-led users who want premium materials without heritage pricing; selective retail | Strong technology ecosystems; fast obsolescence; privacy failures; sibling identity may still be linked publicly to parent |

## Conditional entry design and execution
**Entry:** no commercial launch now. A proposed discovery budget capped at $100,000 would reduce no-entry NPV by $100,000 if spent; it is a separate future decision, excluded from the current comparison. Test sibling and partner concepts side by side before selecting an architecture.

**Target:** design-led professionals initially; verify purchase behavior and acquisition cost rather than trusting stated intent.

**Brand:** if evidence later supports the sibling architecture, create a distinct consumer name owned by Valenne Group, with truthful parent disclosure on corporate/legal materials, separate logo, website, service proposition and pricing. Never imply a mechanical product or guaranteed resale value. This is a sibling brand, not a visibly endorsed heritage sub-line.

**Product:** one premium-material wellness wearable with restrained notifications and interchangeable straps, compatible with major phone platforms subject to validation. Avoid a proprietary app store and medical diagnostic promises at launch. Favor replaceable battery/serviceable electronics where supplier feasibility permits; do not promise unlimited upgrades.

**Technology/manufacturing:** competitively source a proven electronics/firmware platform and contract manufacturer; retain industrial design, quality acceptance and customer experience. Require security updates, data portability, replacement parts and an explicit support sunset budget. Manufacturing partnership does not require consumer co-branding.

**Price:** start paid demand testing at $950 alongside $750, $1,150 and $1,350; no price is approved by this model. Maintain separation from $6,000 net mechanical economics.

**Distribution:** test 60% direct / 40% specialist retail; use separate display and service training. Do not depend on legacy boutiques for volume.

## Gates and owners (proposed)
Within 0–6 weeks, strategy/insights runs real concept and price tests, including a mechanical-owner holdout. Within 6–12 weeks, procurement/engineering obtains supplier and support quotes, and finance rebuilds economics. Release tooling only when positive NPV, <=2% annual displacement and <=0.5% brand haircut are supported. Stop if support obligations or unit contribution fail validation. Monitor paid conversion, returns, acquisition cost, deferred mechanical purchases and parent-brand association, each against baseline/control. Survey estimates are not causal proof: track actual cohort purchase behavior over 6–12 months before scaling.

## Limitations and portfolio claim
This project demonstrates structured analysis, MySQL, formula-based Excel and a Power BI build specification. It does not claim a live dashboard, real research, actual commercial results or statistically validated brand damage. Do not describe modeled NPV as realized profit.

## When could the answer change?
At unchanged unit economics the sibling needs approximately 1.705× demand for zero NPV, while its 2% displacement tolerance binds at 1.678×. Therefore, increased volume must be accompanied by lower switching or lower fixed/setup costs. The modular hybrid needs about 2.243× demand and could stay within the 2% displacement threshold until 4.121×, but that demand has not been established. Co-branding needs about 1.958× demand and still must reduce its 0.6% brand haircut below 0.5%. These are decision boundaries, not forecasts. The four sibling test prices all remain negative; $950 is the least-negative of those tested.
