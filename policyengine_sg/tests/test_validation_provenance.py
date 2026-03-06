"""
Validation tests with provenance metadata.

Each test class references an official source URL and access date so
that future maintainers can re-verify expectations against the
authoritative publication.

These tests use the Simulation API directly (rather than YAML) to
demonstrate programmatic construction and to attach provenance metadata
that YAML tests cannot express.
"""

import pytest
from policyengine_core.simulations import SimulationBuilder
from policyengine_sg.system import SingaporeTaxBenefitSystem

SYSTEM = SingaporeTaxBenefitSystem()
PERIOD = "2025"


def _build(person_vars, household_vars=None):
    """Build a single-person simulation from plain dicts."""
    people = {"person1": {k: {PERIOD: v} for k, v in person_vars.items()}}
    hh = {"members": ["person1"]}
    if household_vars:
        hh.update({k: {PERIOD: v} for k, v in household_vars.items()})
    return SimulationBuilder().build_from_dict(
        SYSTEM,
        {"people": people, "households": {"hh": hh}},
    )


def _calc(sim, variable):
    return float(sim.calculate(variable, PERIOD)[0])


# ------------------------------------------------------------------ #
# CPF contribution rates — all 6 age bands (employee + employer)
# ------------------------------------------------------------------ #
class TestCPFContributionRates:
    """
    Source: CPF Board — Contribution Rates Table
    URL: https://www.cpf.gov.sg/employer/employer-obligations/how-much-cpf-contributions-to-pay
    Access date: March 2025

    Verifies employee and employer rates for each age band at a
    standard income of $100,000 (below the $102,000 annual wage
    ceiling, so capping does not apply).
    """

    @pytest.mark.parametrize(
        "age, label, expected_ee, expected_er",
        [
            (35, "55 and below", 20_000, 17_000),
            (58, "above 55 to 60", 17_000, 15_500),
            (63, "above 60 to 65", 11_500, 12_000),
            (68, "above 65 to 70", 7_500, 9_000),
            (72, "above 70", 5_000, 7_500),
        ],
        ids=["age_55_below", "age_55_60", "age_60_65", "age_65_70", "age_70_above"],
    )
    def test_cpf_rates(self, age, label, expected_ee, expected_er):
        sim = _build({"age": age, "employment_income": 100_000})
        assert _calc(sim, "cpf_employee_contribution") == pytest.approx(
            expected_ee, abs=0.5
        ), f"CPF employee rate wrong for {label}"
        assert _calc(sim, "cpf_employer_contribution") == pytest.approx(
            expected_er, abs=0.5
        ), f"CPF employer rate wrong for {label}"

    def test_cpf_wage_ceiling(self):
        """Income above $102K annual wage ceiling is not subject to CPF."""
        sim = _build({"age": 35, "employment_income": 200_000})
        # Capped at 102,000 * 20% = 20,400
        assert _calc(sim, "cpf_employee_contribution") == pytest.approx(20_400, abs=0.5)


# ------------------------------------------------------------------ #
# PWC comprehensive scenario via Simulation API
# ------------------------------------------------------------------ #
class TestPWCSample:
    """
    Source: PWC Tax Summaries — Singapore Individual Sample Calculation
    URL: https://taxsummaries.pwc.com/singapore/individual/sample-personal-income-tax-calculation
    Access date: March 2025

    Employment income is $118K (net of $2K expenses — model does not
    support employment expense deductions).
    """

    @pytest.fixture
    def sim(self):
        return _build(
            {
                "age": 40,
                "employment_income": 118_000,
                "self_employment_income": 50_000,
                "interest_income": 5_000,
                "rental_income": 2_000,
                "is_resident": True,
                "is_citizen": True,
                "is_married": True,
                "number_of_children": 2,
                "number_of_dependant_parents": 1,
                "donation_amount": 400,
            },
        )

    def test_total_income(self, sim):
        assert _calc(sim, "total_income") == pytest.approx(175_000, abs=0.5)

    def test_cpf(self, sim):
        assert _calc(sim, "cpf_employee_contribution") == pytest.approx(20_400, abs=0.5)

    def test_reliefs(self, sim):
        assert _calc(sim, "earned_income_relief") == pytest.approx(1_000, abs=0.5)
        assert _calc(sim, "cpf_relief") == pytest.approx(20_400, abs=0.5)
        assert _calc(sim, "spouse_relief") == pytest.approx(2_000, abs=0.5)
        assert _calc(sim, "child_relief") == pytest.approx(8_000, abs=0.5)
        assert _calc(sim, "parent_relief") == pytest.approx(9_000, abs=0.5)
        assert _calc(sim, "total_personal_reliefs") == pytest.approx(40_400, abs=0.5)

    def test_deductions(self, sim):
        assert _calc(sim, "donation_deduction") == pytest.approx(1_000, abs=0.5)

    def test_chargeable_income(self, sim):
        assert _calc(sim, "chargeable_income") == pytest.approx(133_600, abs=0.5)

    def test_tax(self, sim):
        assert _calc(sim, "income_tax_before_rebate") == pytest.approx(9_990, abs=0.5)
        assert _calc(sim, "pit_rebate") == pytest.approx(200, abs=0.5)
        assert _calc(sim, "income_tax") == pytest.approx(9_790, abs=0.5)


# ------------------------------------------------------------------ #
# Buyers Stamp Duty — 5 price points
# ------------------------------------------------------------------ #
class TestBuyersStampDuty:
    """
    Source: IRAS — Buyers Stamp Duty
    URL: https://www.iras.gov.sg/taxes/stamp-duty/for-property/buying-or-acquiring-property/buyer's-stamp-duty-(bsd)
    Access date: March 2025

    BSD rates (from 15 Feb 2023):
      First $180K @ 1%, next $180K @ 2%, next $640K @ 3%,
      next $500K @ 4%, next $1.5M @ 5%, remainder @ 6%
    """

    @pytest.mark.parametrize(
        "price, expected_bsd",
        [
            # 180K*1% + 120K*2% = 1,800 + 2,400 = 4,200
            (300_000, 4_200),
            # 180K*1% + 180K*2% + 140K*3% = 1,800 + 3,600 + 4,200 = 9,600
            (500_000, 9_600),
            # 180K*1% + 180K*2% + 640K*3% = 1,800 + 3,600 + 19,200 = 24,600
            (1_000_000, 24_600),
            # + 500K*4% = 24,600 + 20,000 = 44,600
            (1_500_000, 44_600),
            # + 1,500K*5% = 44,600 + 75,000 = 119,600
            (3_000_000, 119_600),
        ],
        ids=["300K", "500K", "1M", "1.5M", "3M"],
    )
    def test_bsd(self, price, expected_bsd):
        sim = _build(
            {"age": 35},
            {"property_purchase_price": price, "buyer_profile": "CITIZEN_FIRST"},
        )
        assert _calc(sim, "buyers_stamp_duty") == pytest.approx(expected_bsd, abs=0.5)

    def test_absd_citizen_first_is_zero(self):
        """Singapore citizens buying their first property pay 0% ABSD."""
        sim = _build(
            {"age": 35, "is_citizen": True},
            {"property_purchase_price": 1_000_000, "buyer_profile": "CITIZEN_FIRST"},
        )
        assert _calc(sim, "additional_buyers_stamp_duty") == pytest.approx(0, abs=0.5)

    def test_absd_foreigner(self):
        """Foreigners pay 60% ABSD."""
        sim = _build(
            {"age": 35},
            {"property_purchase_price": 1_000_000, "buyer_profile": "FOREIGNER"},
        )
        assert _calc(sim, "additional_buyers_stamp_duty") == pytest.approx(
            600_000, abs=0.5
        )


# ------------------------------------------------------------------ #
# Skills Development Levy — SSG / MOM
# ------------------------------------------------------------------ #
class TestSkillsDevelopmentLevy:
    """
    Source: SkillsFuture Singapore — Skills Development Levy
    URL: https://www.ssg.gov.sg/sdl.html
    Access date: March 2025

    SDL = 0.25% of monthly gross wages, with:
      - Minimum $2/month ($24/year)
      - Maximum $11.25/month ($135/year)
    """

    @pytest.mark.parametrize(
        "annual_income, expected_sdl",
        [
            # $2,500/month * 0.25% = $6.25/month * 12 = $75
            (30_000, 75),
            # $400/month * 0.25% = $1/month < $2 min → $2/month * 12 = $24
            (4_800, 24),
        ],
        ids=["standard", "minimum_floor"],
    )
    def test_sdl(self, annual_income, expected_sdl):
        sim = _build({"age": 30, "employment_income": annual_income})
        assert _calc(sim, "skills_development_levy") == pytest.approx(
            expected_sdl, abs=0.5
        )


# ------------------------------------------------------------------ #
# Foreign Domestic Worker Levy — MOM
# ------------------------------------------------------------------ #
class TestFDWLevy:
    """
    Source: MOM — Foreign Domestic Worker Levy
    URL: https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-domestic-worker/foreign-domestic-worker-levy
    Access date: March 2025

    Standard: $300/month ($3,600/year)
    Concessionary: $60/month ($720/year) — if employer has child <16,
    elderly 67+, or person with disability
    """

    def test_standard_levy(self):
        sim = _build({"age": 40, "has_fdw": True})
        assert _calc(sim, "fdw_levy") == pytest.approx(3_600, abs=0.5)

    def test_concessionary_levy(self):
        sim = _build({"age": 40, "has_fdw": True, "has_child_under_16": True})
        assert _calc(sim, "fdw_levy") == pytest.approx(720, abs=0.5)


# ------------------------------------------------------------------ #
# ComCare Long-Term Assistance — MSF
# ------------------------------------------------------------------ #
class TestComCareLTA:
    """
    Source: MSF — ComCare Long-Term Assistance
    URL: https://www.msf.gov.sg/what-we-do/comcare/comcare-long-term-assistance
    Access date: March 2025

    Monthly assistance rates by household size (2025):
      1 person: $640/month → $7,680/year
    Eligibility: citizen/PR, household income per capita <= ceiling
    """

    def test_single_person_lta(self):
        sim = _build(
            {
                "age": 40,
                "is_citizen": True,
                "employment_income": 0,
                "household_income_per_capita": 650,
            },
            {"hdb_flat_type": "TWO_ROOM"},
        )
        assert _calc(sim, "comcare_eligible") == pytest.approx(1, abs=0.5)
        assert _calc(sim, "comcare_lta") == pytest.approx(7_680, abs=0.5)
