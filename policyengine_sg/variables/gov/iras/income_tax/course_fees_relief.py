from policyengine_sg.model_api import *


class course_fees_relief(Variable):
    value_type = float
    entity = Person
    label = "Course fees relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/course-fees-relief"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.course_fees
        fees = person("course_fees", period)
        return min_(fees, p.amount)
