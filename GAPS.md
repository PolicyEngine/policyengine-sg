# PolicyEngine Singapore - Gaps & Adjustments Tracker

Status: ~105 variables, ~155 parameter files, 122 tests (all passing)
Branch: `implement-sg-tax-benefit-system` (PR #5)

---

## 1. Adjustments Needed to Existing Implementations

### 1.1 ~~WIS Income-Based Tapering~~ RESOLVED
Implemented exact piecewise linear formulas from CPF Board's
official WIS calculator for all 4 age bands (30-34, 35-44,
45-59, 60+). Each band has multi-segment ramp-up, plateau
($1,700-$2,300), and ramp-down. 7 tests covering plateau,
ramp-up, ramp-down, and boundary cases.

### 1.2 ~~NSman Relief Categories~~ RESOLVED
Added NsmanStatus enum (5 categories), is_wife_of_nsman and
is_parent_of_nsman inputs. Formula uses select() over enum +
max_() for mutual exclusivity (cannot combine self + wife/parent).
Fixed key_appointment_non_active parameter: $3,000 -> $3,500.

### 1.3 ~~Dependant Income Threshold Not Enforced~~ RESOLVED
Added spouse_income input variable. spouse_relief.py now checks
spouse_income <= dependant_income_threshold ($4k for 2024,
$8k for 2025). Child/parent reliefs remain simplified (no
individual dependant income tracking).

### 1.4 ~~WMCR Uses Fixed Amounts Only~~ RESOLVED
Added number_of_children_born_before_2024 input. Formula now
splits: pre-2024 children use rate-based (15%/20%/25% of earned
income), post-2024 children use fixed ($8k/$10k/$12k).

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

### 2.1 ~~Baby Bonus Cash Gift~~ IMPLEMENTED
$11,000 (1st-2nd child), $13,000 (3rd+). Requires married & citizen.
4 tests.

### 2.2 ~~CDA First Step Grant~~ IMPLEMENTED
$5,000 (1st-2nd), $5,000/$10,000 (3rd+ pre/post Feb 2025).
Requires citizen. 3 tests.

### 2.3 ~~Childcare / Infant Care Subsidies~~ IMPLEMENTED
Basic: $300/mo childcare, $600/mo infant care (working mothers).
Additional: $467-$0/mo by GHI bracket. 4 tests.

### 2.4 ~~KiFAS~~ IMPLEMENTED
$163-$0/mo by GHI bracket. Requires citizen. 4 tests.

### 2.5 ~~MOE Financial Assistance Scheme~~ IMPLEMENTED
Eligibility variable: GHI <= $3,000 or PCI <= $750. 4 tests.

### 2.6 ~~CHAS Tier~~ IMPLEMENTED
Enum tiers: Blue (PCI <= $1,500), Orange (PCI <= $2,300),
Green (all other citizens). 4 tests.

### 2.7 MediShield Life Premium Subsidies (LOW)
**Agency:** MOH / CPF
**Subsidies:** Up to 50% premium subsidy (means-tested)
**Modelability:** LOW - complex premium schedule by age + subsidy
tiers by income. Skipped for now.

### 2.8 ~~Enhanced CPF Housing Grant (EHG)~~ IMPLEMENTED
Up to $120,000 for first-time buyers by GHI bracket. 4 tests.

### 2.9 ~~FDW Levy Concession~~ IMPLEMENTED
$300/mo standard, $60/mo concessionary. Concession if child < 16,
elderly >= 67, or disabled member. 4 tests.

### 2.10 ~~Seller's Stamp Duty (SSD)~~ IMPLEMENTED
12%/8%/4% by holding period (1/2/3 years). 4 tests.

---

## 3. Missing Programs - Medium Priority

### 3.1 ~~Assurance Package Cash~~ IMPLEMENTED
$600 (low income <= $34k), $350 (mid <= $100k), $200 (higher).
Multi-property owners get $200. 5 tests.

### 3.2 Higher Education Bursaries (MOE/University) (DEFERRED)
Varies by institution and income tier. Too many institution-specific
schemes to model comprehensively.

### 3.3 CareShield Life Premium Subsidies (DEFERRED)
Requires income tier + premium schedule. Complex and data-limited.

### 3.4 ~~Student Care Fee Assistance (SCFA)~~ IMPLEMENTED
$290-$0/mo by GHI bracket. Requires citizen. 4 tests.

### 3.5 SkillsFuture Credit (NOT MODELABLE)
Balance tracking not possible in single-period architecture.

### 3.6 ~~Edusave Contribution~~ IMPLEMENTED
$230 (primary), $290 (secondary). Requires citizen + school level.
4 tests.

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
| MediShield Life subsidies | Complex age+income premium matrix |
| CareShield Life subsidies | Complex premium/subsidy schedule |

---

## 5. Implementation Summary

### Currently Implemented (~105 variables)

| Area | Variables | Tests |
|------|-----------|-------|
| Personal Income Tax | 20 (13 reliefs + rates + rebates + PTR) | 27 |
| CPF Contributions | 3 (employee + employer + total) | 6 |
| Property Tax | 1 (owner/non-owner occupied) | 3 |
| Stamp Duty | 4 (BSD + ABSD + SSD + total) | 11 |
| GST | 1 | 1 |
| SDL | 1 | 2 |
| GSTV | 4 (cash + U-Save + MediSave + S&CC) | 17 |
| CDC Vouchers | 1 | 2 |
| Assurance Package | 1 | 5 |
| WIS | 3 (eligible + amount + cash) | 7 |
| Silver Support | 2 (eligible + amount) | 3 |
| ComCare LTA | 2 (eligible + LTA) | 2 |
| Baby Bonus | 1 (cash gift) | 4 |
| CDA First Step | 1 | 3 |
| Childcare Subsidy | 1 | 4 |
| KiFAS | 1 | 4 |
| MOE FAS | 1 (eligibility) | 4 |
| Edusave | 1 | 4 |
| CHAS | 1 (tier) | 4 |
| EHG | 1 | 4 |
| FDW Levy | 1 | 4 |
| SCFA | 1 | 4 |
| Input variables | ~59 | - |

### Parameter Files: ~155
### Total Tests: 122 (all passing)
