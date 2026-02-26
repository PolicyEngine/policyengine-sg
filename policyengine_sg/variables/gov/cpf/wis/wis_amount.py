from policyengine_sg.model_api import *


class wis_amount(Variable):
    value_type = float
    entity = Person
    label = "Workfare Income Supplement amount"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.cpf.gov.sg/member/"
        "growing-your-savings/"
        "government-support/"
        "workfare-income-supplement",
        "https://www.cpf.gov.sg/member/"
        "tools-and-services/calculators/"
        "workfare-income-supplement-employee"
        "-work-year-2025-calculator",
    )

    def formula(person, period, parameters):
        eligible = person("wis_eligible", period)
        age = person("age", period)
        disabled = person("is_disabled", period)
        income = person("employment_income", period)
        gmi = income / 12

        # Piecewise linear monthly amounts by age band
        # from CPF Board's official WIS calculator.
        m_30 = _monthly_30_34(gmi)
        m_35 = _monthly_35_44(gmi)
        m_45 = _monthly_45_59(gmi)
        m_60 = _monthly_60_plus(gmi)

        monthly = select(
            [age < 35, age < 45, age < 60],
            [m_30, m_35, m_45],
            default=m_60,
        )
        monthly = where(disabled, m_60, monthly)
        annual = monthly * 12
        return where(eligible, max_(annual, 0), 0)


def _monthly_30_34(gmi):
    """Age 30-34 piecewise linear WIS (monthly)."""
    return select(
        [
            gmi < 500,
            gmi < 1400,
            gmi < 1700,
            gmi < 2300,
            gmi <= 3000,
        ],
        [
            0,
            gmi / 8 + 19.0 / 6,
            gmi * 13.0 / 150 + 341.0 / 6,
            204.17,
            15247.0 / 21 - gmi * 953.0 / 4200,
        ],
        default=0,
    )


def _monthly_35_44(gmi):
    """Age 35-44 piecewise linear WIS (monthly)."""
    return select(
        [
            gmi < 500,
            gmi < 1400,
            gmi < 1700,
            gmi < 2300,
            gmi <= 3000,
        ],
        [
            0,
            gmi * 643.0 / 3600 + 40.0 / 9,
            gmi * 223.0 / 1800 + 1459.0 / 18,
            291.67,
            43553.0 / 42 - gmi * 1361.0 / 4200,
        ],
        default=0,
    )


def _monthly_45_59(gmi):
    """Age 45-59 piecewise linear WIS (monthly)."""
    return select(
        [
            gmi < 500,
            gmi < 700,
            gmi < 1200,
            gmi < 1700,
            gmi < 2300,
            gmi <= 3000,
        ],
        [
            0,
            gmi * 329.0 / 1200 + 49.0 / 4,
            gmi / 6 + 175.0 / 2,
            gmi / 8 + 275.0 / 2,
            350,
            34847.0 / 28 - gmi * 1089.0 / 2800,
        ],
        default=0,
    )


def _monthly_60_plus(gmi):
    """Age 60+ piecewise linear WIS (monthly)."""
    return select(
        [
            gmi < 500,
            gmi < 1200,
            gmi < 1700,
            gmi < 2300,
            gmi <= 3000,
        ],
        [
            0,
            gmi * 1163.0 / 4200 + 512.0 / 21,
            gmi * 31.0 / 300 + 698.0 / 3,
            408.33,
            40651.0 / 28 - gmi * 3811.0 / 8400,
        ],
        default=0,
    )
