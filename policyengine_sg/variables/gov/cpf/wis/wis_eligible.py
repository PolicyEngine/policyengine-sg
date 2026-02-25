from policyengine_sg.model_api import *


class wis_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Workfare Income Supplement"
    definition_period = YEAR
    reference = (
        "https://www.cpf.gov.sg/member/"
        "growing-your-savings/"
        "government-support/"
        "workfare-income-supplement"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.cpf.wis
        age = person("age", period)
        citizen = person("is_citizen", period)
        is_disabled = person("is_disabled", period)
        income = person("employment_income", period)
        monthly = income / 12
        av = person.household("property_annual_value", period)
        n_prop = person("number_of_properties", period)
        age_ok = (age >= p.age_minimum) | is_disabled
        return (
            citizen
            & age_ok
            & (monthly >= p.income_floor)
            & (monthly <= p.income_ceiling)
            & (av <= p.property_av_ceiling)
            & (n_prop <= 1)
        )
