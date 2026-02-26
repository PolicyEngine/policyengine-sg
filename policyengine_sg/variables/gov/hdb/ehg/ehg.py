from policyengine_sg.model_api import *


class ehg(Variable):
    value_type = float
    entity = Person
    label = "Enhanced CPF Housing Grant"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.hdb.gov.sg/residential/"
        "buying-a-flat/understanding-your-eligibility"
        "-and-housing-loan-options/flat-and-grant"
        "-eligibility/couples-and-families/"
        "enhanced-cpf-housing-grant-families"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.hdb.ehg
        citizen = person("is_citizen", period)
        first_time = person("is_first_time_homebuyer", period)
        ghi = person("gross_monthly_household_income", period)
        grant = p.grant.calc(ghi)
        return where(citizen & first_time, grant, 0)
