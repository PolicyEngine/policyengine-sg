from policyengine_sg.model_api import *
import numpy as np


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

        p = parameters(period).gov.cpf.wis
        a = p.age_thresholds

        s_30 = parameters(period).gov.cpf.wis.schedule.age_30_to_34
        s_35 = parameters(period).gov.cpf.wis.schedule.age_35_to_44
        s_45 = parameters(period).gov.cpf.wis.schedule.age_45_to_59
        s_60 = parameters(period).gov.cpf.wis.schedule.age_60_plus

        m_30 = _interp(gmi, s_30)
        m_35 = _interp(gmi, s_35)
        m_45 = _interp(gmi, s_45)
        m_60 = _interp(gmi, s_60)

        monthly = select(
            [age < a.band_35, age < a.band_45, age < a.band_60],
            [m_30, m_35, m_45],
            default=m_60,
        )
        monthly = where(disabled, m_60, monthly)
        annual = monthly * 12
        return where(eligible, max_(annual, 0), 0)


def _interp(gmi, scale):
    """Piecewise linear interpolation from a bracket schedule."""
    thresholds = np.array(scale.thresholds)
    amounts = np.array(scale.amounts)
    return np.interp(gmi, thresholds, amounts)
