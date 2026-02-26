from policyengine_sg.model_api import *


class comcare_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for ComCare assistance"
    definition_period = YEAR
    reference = "https://www.msf.gov.sg/what-we-do/comcare"

    def formula(person, period, parameters):
        p = parameters(period).gov.msf.comcare
        citizen = person("is_citizen", period)
        pr = person("is_pr", period)
        income_pc = person("household_income_per_capita", period)
        monthly_pc = income_pc / 12
        return (citizen | pr) & (monthly_pc <= p.income_per_capita_ceiling)
