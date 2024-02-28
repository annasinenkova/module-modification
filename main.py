from z3 import *
from alm import ALM
from sat_formation import adding_variables, adding_restrictions, eq_variables
from functions import adding_functions
from math import log2

s = Solver()
sat_vars = {}
alm = ALM

value = adding_functions("text")
for f in range(len(value)):
    size = int(log2(len(value[f][0])))
    adding_variables(sat_vars, alm, f, len(value[f]), size)
    adding_restrictions(s, sat_vars, alm, f, len(value[f]), value[f], size)
eq_variables(s, sat_vars, alm, len(value))
print(len(sat_vars))
if s.check() == unsat:
    print("UNSAT")
else:
    print("SAT")
    model = s.model()
    for k in range(alm.elements[alm.N - 1].inputs_num):
        for j in range(alm.N - 1):
            if model[sat_vars[f"c_{0}_{alm.N - 1}_{k}_{j}"]]:
                print(f"{k}-ый вход подключен к {j}-му элементу")
    for i in range(4, alm.N - 1):
        for k in range(alm.elements[i].inputs_num):
            if model[sat_vars[f"c_{0}_{i}_{k}_{alm.N - 1}"]] == True:
                print(f"{k}-ый вход {i}-го элемента подключен к выходу нового элемента")

    print([model[sat_vars[f"t_{0}_{alm.N - 1}_{i}"]] for i in range(4)])
