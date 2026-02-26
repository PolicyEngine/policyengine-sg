# PolicyEngine Singapore - Gaps & Adjustments Tracker

Status: 82 variables, ~123 parameter files, 71 tests (all passing)
Branch: `implement-sg-tax-benefit-system` (PR #5)

---

## 1. Adjustments Needed to Existing Implementations

### 1.1 WIS Income-Based Tapering (HIGH)
**File:** `variables/gov/cpf/wis/wis_amount.py`
**Issue:** Currently awards full maximum annual amount by age band.
Real WIS tapers linearly: full amount up to $500/mo income, then
linearly decreasing to $0 at $2,500/mo income ceiling.
**Fix:** Replace flat `select()` with linear taper formula:
`amount * max(0, (ceiling - monthly_income) / (ceiling - floor))`.
Need to add income_floor parameter ($500/mo) to the taper calc.

### 1.2 NSman Relief Categories (MEDIUM)
**File:** `variables/gov/iras/income_tax/nsman_relief.py`
**Issue:** Only uses `p.active` ($3,000). Parameters exist for all
five categories (active=$3,000, non_active=$1,500,
key_appointment=$3,500, parent=$750, wife=$750) but the formula
only ever returns the active amount.
**Fix:** Add input variables for NSman category (active/non-active/
key-appointment) and separate parent/wife NSman relief inputs.
Use `select()` over categories + add parent/wife amounts.

### 1.3 Dependant Income Threshold Not Enforced (MEDIUM)
**File:** `parameters/gov/iras/income_tax/reliefs/dependant_income_threshold.yaml`
**Issue:** Parameter exists ($4,000 for 2024, $8,000 for 2025) but
is NEVER referenced by any relief formula. Spouse relief, child
relief, and parent relief should all check that the dependant's
income is below this threshold before granting the relief.
**Current impact:** Spouse, child, and parent reliefs are granted
unconditionally (no dependant income check).
**Fix:** Add a `spouse_income` input variable and check
`spouse_income <= p.dependant_income_threshold` in `spouse_relief.py`.
For child/parent reliefs this is harder to model without individual
dependant data - may need to accept as a simplification.

### 1.4 WMCR Uses Fixed Amounts Only (MEDIUM)
**File:** `variables/gov/iras/income_tax/wmcr.py`
**Issue:** Uses fixed amounts ($8k/$10k/$12k per child). This is
correct for children born/adopted on or after 1 Jan 2024. For
children born BEFORE 2024, WMCR is percentage-of-income
(15%/20%/25%). Parameters for both exist (first_child.yaml +
first_child_rate.yaml) but only fixed amounts are used.
**Fix:** Add input `number_of_children_born_before_2024` or a
boolean toggle, then use `where()` to apply rate-based WMCR for
pre-2024 children vs fixed amounts for post-2024 children.
Low priority since fixed amounts apply to YA 2025+.

### 1.5 GSTV MediSave Missing Income Ceiling Check (LOW)
**File:** `variables/gov/mof/gstv/gstv_medisave.py`
**Issue:** GSTV Cash checks `income <= p.income_ceiling` ($34k)
but MediSave implementation does not. GSTV MediSave may have a
separate assessable income ceiling. Need to verify from MOF source
whether MediSave has its own income test (official MOF page
returned 403 during research).
**Fix:** If income ceiling applies, add parameter + check.

### 1.6 PTR Parameters Unused (LOW / BY DESIGN)
**Files:** `parameters/gov/iras/income_tax/rebates/parenthood_*.yaml`
**Issue:** Three parameters exist (first_child=$5k, second=$10k,
third+=$20k) but the PTR variable uses only `ptr_balance` input.
This is BY DESIGN because PTR is a one-time grant per child birth
with carry-forward, which PolicyEngine's single-period architecture
cannot track. The parameters serve as documentation.
**Fix:** No fix needed, but consider adding a comment in the
variable or removing the unused parameters to avoid confusion.

### 1.7 ComCare SMTA Not Modeled (LOW)
**File:** `variables/gov/msf/comcare/`
**Issue:** Only LTA (Long-Term Assistance) is modeled. SMTA
(Short-to-Medium-Term Assistance) has different eligibility
criteria (temporarily unable to work, not permanently). Both fall
under ComCare but have distinct rules.
**Fix:** Add `comcare_smta.py` if sufficient documentation exists.
SMTA amounts are determined by holistic assessment so may not be
fully modelable.

### 1.8 Silver Support CPF Savings Check Missing (LOW)
**File:** `variables/gov/cpf/silver_support/silver_support_eligible.py`
**Issue:** Eligibility checks age, citizenship, and per-capita
income. Real Silver Support also checks lifetime CPF savings
(payout amounts only available for those with low lifetime CPF
contributions). PolicyEngine cannot model CPF lifetime savings.
**Fix:** Document as a known limitation. No fix possible without
CPF balance data.

---

## 2. Missing Programs - High Priority

### 2.1 Baby Bonus Cash Gift
**Agency:** MSF
**Amount:** $11,000 (1st-2nd child), $13,000 (3rd+ child)
**Eligibility:** All Singapore citizen children
**Modelability:** HIGH - straightforward calculation from
number_of_children
**Reference:** https://www.babybonus.msf.gov.sg

### 2.2 Child Development Account (CDA) First Step Grant
**Agency:** MSF
**Amount:** $5,000 (1st-2nd child), $8,000 (3rd-4th),
$10,000 (5th+)
**Eligibility:** Singapore citizen children
**Modelability:** HIGH - lookup by birth order

### 2.3 Childcare / Infant Care Subsidies
**Agency:** ECDA
**Basic subsidy:** Up to $600/mo (childcare), $600/mo (infant)
**Additional subsidy:** Up to $467/mo (means-tested by income)
**Modelability:** MEDIUM - needs working_mother flag, child age,
gross household income tiers
**Reference:** https://www.ecda.gov.sg/parents/subsidies-financial-assistance

### 2.4 KiFAS (Kindergarten Fee Assistance Scheme)
**Agency:** MOE
**Subsidy:** Up to $170/mo for gross HH income <= $3,000/mo
**Modelability:** MEDIUM - income-tiered subsidies
**Reference:** https://www.moe.gov.sg/preschool/kifas

### 2.5 MOE Financial Assistance Scheme
**Agency:** MOE
**Benefits:** Free textbooks, school meals, transport, uniform
**Eligibility:** Gross HH income <= $3,000/mo or per capita
<= $750/mo
**Modelability:** MEDIUM - could model monetary value of benefits

### 2.6 CHAS (Community Health Assist Scheme)
**Agency:** MOH
**Tiers:** Blue (income <= $900 per capita), Orange (<=1,200),
Green (all citizens)
**Benefits:** Subsidised GP/dental/specialist visits
**Modelability:** MEDIUM-LOW - could model subsidy tier assignment
but not actual subsidy amounts (depend on visit type)
**Reference:** https://www.chas.sg

### 2.7 MediShield Life Premium Subsidies
**Agency:** MOH / CPF
**Subsidies:** Up to 50% premium subsidy (means-tested)
**Modelability:** LOW - complex premium schedule by age + subsidy
tiers by income
**Reference:** https://www.cpf.gov.sg/member/healthcare-financing/medishield-life

### 2.8 Enhanced CPF Housing Grant (EHG)
**Agency:** HDB
**Amount:** Up to $120,000 for first-time buyers
**Eligibility:** Income ceiling, first-timer, buying from HDB
**Modelability:** MEDIUM - income-tiered grant amounts
**Reference:** https://www.hdb.gov.sg/residential/buying-a-flat/flat-booking/cpf-housing-grants

### 2.9 FDW (Foreign Domestic Worker) Levy Concession
**Agency:** MOM
**Amount:** $60/mo vs $300/mo standard levy
**Eligibility:** Household with child < 16 or elderly >= 67
or disabled member
**Modelability:** HIGH - simple eligibility check + fixed amounts
**Reference:** https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-domestic-worker/foreign-domestic-worker-levy

### 2.10 Seller's Stamp Duty (SSD)
**Agency:** IRAS
**Rates:** 12%/8%/4% based on holding period (1/2/3 years)
**Modelability:** HIGH - similar to BSD, needs holding_period input
**Reference:** https://www.iras.gov.sg/taxes/stamp-duty/for-property/selling-or-disposing-of-property/seller's-stamp-duty-(ssd)

---

## 3. Missing Programs - Medium Priority

### 3.1 Assurance Package Cash
**Agency:** MOF
**Amount:** $200-$400 cash (GST offset, income-tiered)
**Modelability:** MEDIUM - similar to GSTV Cash

### 3.2 Higher Education Bursaries (MOE/University)
**Agency:** MOE
**Amount:** Varies by institution and income tier
**Modelability:** LOW - many institution-specific schemes

### 3.3 CareShield Life Premium Subsidies
**Agency:** MOH
**Modelability:** LOW - requires income tier + premium schedule

### 3.4 Student Care Fee Assistance (SCFA)
**Agency:** MSF
**Modelability:** MEDIUM - means-tested subsidy for after-school
care

### 3.5 SkillsFuture Credit
**Agency:** SSG
**Amount:** $500 one-time (age 25+), periodic top-ups
**Modelability:** LOW - balance tracking not possible

### 3.6 Edusave Merit Bursary
**Agency:** MOE
**Amount:** $200-$350 by school level
**Eligibility:** Citizen, income <= $6,900/mo
**Modelability:** MEDIUM

---

## 4. Not Modelable (PolicyEngine Limitations)

| Program | Reason |
|---------|--------|
| CPF LIFE payouts | Needs individual CPF balance history |
| MediFund | Discretionary, case-by-case assessment |
| ComCare SMTA amounts | Holistic assessment, no fixed formula |
| WIS time-based tapering | Employment month tracking required |
| PTR birth-order tracking | Multi-year carry-forward needed |
| Progressive wage model | Sector-specific, employer-side |
| SkillsFuture balance | Balance tracking across periods |

---

## 5. Implementation Summary

### Currently Implemented (82 variables)

| Area | Variables | Tests |
|------|-----------|-------|
| Personal Income Tax | 20 (13 reliefs + rates + rebates + PTR) | 27 |
| CPF Contributions | 3 (employee + employer + total) | 6 |
| Property Tax | 1 (owner/non-owner occupied) | 3 |
| Stamp Duty | 3 (BSD + ABSD + total) | 7 |
| GST | 1 | 1 |
| SDL | 1 | 2 |
| GSTV | 4 (cash + U-Save + MediSave + S&CC) | 17 |
| CDC Vouchers | 1 | 2 |
| WIS | 3 (eligible + amount + cash) | 3 |
| Silver Support | 2 (eligible + amount) | 3 |
| ComCare LTA | 2 (eligible + LTA) | 2 |
| Input variables | ~40 | - |

### Parameter Files: ~123
### Total Tests: 71 (all passing)
