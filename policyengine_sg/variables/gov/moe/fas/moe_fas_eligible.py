from policyengine_sg.model_api import *


class moe_fas_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for MOE Financial Assistance Scheme"
    definition_period = YEAR
    reference = (
        "https://www.moe.gov.sg/" "financial-matters/financial-assistance"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.moe.fas
        citizen = person("is_citizen", period)
        ghi = person("gross_monthly_household_income", period)
        pci = person("household_income_per_capita", period)
        income_ok = (ghi <= p.ghi_ceiling) | (pci <= p.pci_ceiling)
        return citizen & income_ok
