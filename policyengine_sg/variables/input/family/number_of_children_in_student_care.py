from policyengine_sg.model_api import *


class number_of_children_in_student_care(Variable):
    value_type = int
    entity = Person
    label = "Number of children in MSF-registered" " student care centres"
    definition_period = YEAR
    default_value = 0
