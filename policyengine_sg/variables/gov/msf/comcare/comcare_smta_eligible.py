from policyengine_sg.model_api import *


class comcare_smta_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for ComCare Short-to-Medium-Term" " Assistance"
    definition_period = YEAR
    reference = (
        "https://www.msf.gov.sg/what-we-do/comcare",
        "https://supportgowhere.life.gov.sg/schemes/"
        "COMCARE-SMTA/comcare-short-to-medium-term"
        "-assistance-smta",
    )

    def formula(person, period, parameters):
        # NOTE: SMTA benefit amounts are determined by
        # caseworker assessment (shortfall between income
        # and basic living expenses), not a fixed formula.
        # This variable models eligibility only.
        # The $800 PCI benchmark is not a hard threshold
        # in practice but is used here as a proxy.
        p = parameters(period).gov.msf.comcare
        citizen = person("is_citizen", period)
        pr = person("is_pr", period)
        income_pc = person("household_income_per_capita", period)
        monthly_pc = income_pc / 12
        return (citizen | pr) & (monthly_pc <= p.income_per_capita_ceiling)
