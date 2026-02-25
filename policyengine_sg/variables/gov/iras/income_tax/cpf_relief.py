from policyengine_sg.model_api import *


class cpf_relief(Variable):
    value_type = float
    entity = Person
    label = "CPF relief for employee contributions"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/"
        "central-provident-fund(cpf)-relief-"
        "for-employees"
    )

    def formula(person, period, parameters):
        return person("cpf_employee_contribution", period)
