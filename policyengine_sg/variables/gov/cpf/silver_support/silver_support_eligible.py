from policyengine_sg.model_api import *


class silver_support_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Silver Support Scheme"
    definition_period = YEAR
    reference = (
        "https://www.cpf.gov.sg/member/"
        "retirement-income/"
        "government-support/"
        "silver-support-scheme"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.cpf.silver_support
        age = person("age", period)
        citizen = person("is_citizen", period)
        income_pc = person("household_income_per_capita", period)
        monthly_pc = income_pc / 12
        income_ok = monthly_pc <= p.income_per_capita_ceiling
        return citizen & (age >= p.age_minimum) & income_ok
