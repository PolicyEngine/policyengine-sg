from policyengine_sg.model_api import *


class income_tax_before_rebate(Variable):
    value_type = float
    entity = Person
    label = "Income tax before rebate"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-residency-and-tax-rates/"
        "individual-income-tax-rates"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax
        chargeable = person("chargeable_income", period)
        is_resident = person("is_resident", period)
        resident_tax = p.rates.calc(chargeable)
        non_resident_tax = chargeable * p.non_resident.flat_rate
        progressive_higher = max_(resident_tax, non_resident_tax)
        return where(
            is_resident,
            resident_tax,
            progressive_higher,
        )
