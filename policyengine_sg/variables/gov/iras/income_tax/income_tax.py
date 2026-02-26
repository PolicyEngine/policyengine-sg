from policyengine_sg.model_api import *


class income_tax(Variable):
    value_type = float
    entity = Person
    label = "Income tax"
    unit = SGD
    definition_period = YEAR
    reference = "https://www.iras.gov.sg/taxes/" "individual-income-tax"

    def formula(person, period, parameters):
        before_rebate = person("income_tax_before_rebate", period)
        pit = person("pit_rebate", period)
        ptr = person("parenthood_tax_rebate", period)
        return max_(before_rebate - pit - ptr, 0)
