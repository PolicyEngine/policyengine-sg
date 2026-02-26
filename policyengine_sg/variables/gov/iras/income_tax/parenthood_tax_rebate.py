from policyengine_sg.model_api import *


class parenthood_tax_rebate(Variable):
    value_type = float
    entity = Person
    label = "Parenthood tax rebate"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/"
        "parenthood-tax-rebate-(ptr)"
    )

    def formula(person, period, parameters):
        # NOTE: PTR is a one-time rebate per child birth
        # ($5k 1st, $10k 2nd, $20k 3rd+) with indefinite
        # carry-forward. PolicyEngine cannot track multi-year
        # balances, so we model the remaining balance as an
        # input variable. The per-child parameters under
        # gov.iras.income_tax.rebates.parenthood_* exist
        # as reference documentation only.
        tax = person("income_tax_before_rebate", period)
        pit = person("pit_rebate", period)
        tax_after_pit = max_(tax - pit, 0)
        balance = person("ptr_balance", period)
        return min_(balance, tax_after_pit)
