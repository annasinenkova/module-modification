from z3 import *
from table import table


def adding_variables(sat_vars, alm, f, m, in_num):

    # переменные типа t
    for i in range(4):
        for b in range(2 ** 4):
            sat_vars[f"t_{f}_{i}_{b}"] = Bool(f"t_{f}_{i}_{b}")

    for i in range(4, alm.N - 1):
        for b in range(2 ** alm.elements[i].inputs_num):
            sat_vars[f"t_{f}_{i}_{b}"] = BoolVal(table[alm.elements[i].elem_type][b])
    
    for b in range(4):
        sat_vars[f"t_{f}_{alm.N - 1}_{b}"] = Bool(f"t_{f}_{alm.N - 1}_{b}")
        
    for i in range(alm.N, alm.N + alm.n):
        for b in range(2):
            sat_vars[f"t_{f}_{i}_{b}"] = BoolVal(bool(b))

    
    # переменные типа c
    for i in range(4):
        for k, j in enumerate(alm.elements[i].inputs):
            sat_vars[f"c_{f}_{i}_{k}_{j}"] = BoolVal(True)
        for k in range(alm.elements[alm.N - 1].inputs_num):
            sat_vars[f"c_{f}_{alm.N - 1}_{k}_{i}"] = Bool(f"c_{f}_{alm.N - 1}_{k}_{i}")
    
    for i in range(4, alm.N - 1):
        for k, j in enumerate(alm.elements[i].inputs):
            sat_vars[f"c_{f}_{i}_{k}_{j}"] = Bool(f"c_{f}_{i}_{k}_{j}")
            sat_vars[f"c_{f}_{i}_{k}_{alm.N - 1}"] = Bool(f"c_{f}_{i}_{k}_{alm.N - 1}")
        for k in range(alm.elements[alm.N - 1].inputs_num):
            sat_vars[f"c_{f}_{alm.N - 1}_{k}_{i}"] = Bool(f"c_{f}_{alm.N - 1}_{k}_{i}")
            
    for i in range(alm.N, alm.N + alm.n):
        for j in range(alm.N + alm.n, alm.N + alm.n + in_num + 2):
            sat_vars[f"c_{f}_{i}_{j}"] = Bool(f"c_{f}_{i}_{j}")


    # переменные типа o
    for i in alm.outputs:
        for j in range(m):
            sat_vars[f"o_{f}_{i}_{j}"] = Bool(f"o_{f}_{i}_{j}")


    # переменные типа v
    for i in range(alm.N + alm.n + in_num + 2):
        for t in range(2 ** in_num):
            sat_vars[f"v_{f}_{i}_{t}"] = Bool(f"v_{f}_{i}_{t}")


def eq_variables(s, sat_vars, alm, value_len):    
    for i in range(4, alm.N - 1):
        s.add([Or(Not(sat_vars[f"c_{0}_{i}_{a}_{alm.N - 1}"]), Not(sat_vars[f"c_{0}_{i}_{b}_{alm.N - 1}"]))
            for a in range(alm.elements[i].inputs_num) for b in range(a + 1, alm.elements[i].inputs_num)])
        
    for i in range(4, alm.N - 1):
        s.add(Or(Not(sat_vars[f"c_{0}_{alm.N - 1}_{0}_{i}"]), Not(sat_vars[f"c_{0}_{alm.N - 1}_{1}_{i}"])))
        
    for k in [0]:
        s.add([And(Not(sat_vars[f"c_{0}_{i}_{k}_{alm.N - 1}"]), Not(sat_vars[f"c_{0}_{j}_{k}_{alm.N - 1}"])) 
               for i in range(4, alm.N - 1) for j in range(i + 1, alm.N - 1)])
               
    for k in [1]:
        s.add([Or(Not(sat_vars[f"c_{0}_{i}_{k}_{alm.N - 1}"]), Not(sat_vars[f"c_{0}_{j}_{k}_{alm.N - 1}"])) 
               for i in range(4, alm.N - 1) for j in range(i + 1, alm.N - 1)])
        
        
    l = [4, 5, 6, 7, 9, 14]
    for k in [2]:
        s.add([And(Not(sat_vars[f"c_{0}_{i}_{k}_{alm.N - 1}"]), Not(sat_vars[f"c_{0}_{j}_{k}_{alm.N - 1}"])) 
               for i in l for j in l[:l.index(i)]   ])      
    
    for f in range(1, value_len):
        for b in range(4):
            s.add(sat_vars[f"t_{0}_{alm.N - 1}_{b}"] == sat_vars[f"t_{f}_{alm.N - 1}_{b}"])

    for f in range(1, value_len):
        for i in range(4, alm.N - 1):
            for k, j in enumerate(alm.elements[i].inputs):
                s.add(sat_vars[f"c_{0}_{i}_{k}_{j}"] == sat_vars[f"c_{f}_{i}_{k}_{j}"])
                s.add(sat_vars[f"c_{0}_{i}_{k}_{alm.N - 1}"] == sat_vars[f"c_{f}_{i}_{k}_{alm.N - 1}"])
            for k in range(alm.elements[alm.N - 1].inputs_num):
                s.add(sat_vars[f"c_{0}_{alm.N - 1}_{k}_{i}"] == sat_vars[f"c_{f}_{alm.N - 1}_{k}_{i}"])


def adding_restrictions(s, sat_vars, alm, f, m, value, in_num):
    elem_num = alm.N + alm.n

    # ограничение 1 типа
    for k in range(alm.elements[alm.N - 1].inputs_num):
        s.add(Or([sat_vars[f"c_{f}_{alm.N - 1}_{k}_{j}"] for j in range(alm.N - 1)]))
        s.add([Or(Not(sat_vars[f"c_{f}_{alm.N - 1}_{k}_{a}"]), Not(sat_vars[f"c_{f}_{alm.N - 1}_{k}_{b}"])) 
               for a in range(alm.N - 1) for b in range(a + 1, alm.N - 1)])  
               
    for i in range(alm.N, elem_num):
        s.add(Or([sat_vars[f"c_{f}_{i}_{j}"] for j in range(elem_num, elem_num + in_num + 2)]))
        s.add([Or(Not(sat_vars[f"c_{f}_{i}_{a}"]), Not(sat_vars[f"c_{f}_{i}_{b}"])) 
               for a in range(elem_num, elem_num + in_num + 2) for b in range(a + 1, elem_num + in_num + 2)])          


    # ограничение 2 типа
    for j in range(m):
        s.add(Or([sat_vars[f"o_{f}_{i}_{j}"] for i in alm.outputs]))
        s.add([Or(Not(sat_vars[f"o_{f}_{a}_{j}"]), Not(sat_vars[f"o_{f}_{b}_{j}"])) 
               for a in alm.outputs for b in alm.outputs[:alm.outputs.index(a)]])


    # ограничение 3 типа
    for i in range(elem_num, elem_num + in_num):
        for t in range(2 ** in_num):
            s.add(sat_vars[f"v_{f}_{i}_{t}"] == bool((t >> (i - elem_num)) & 1))

    for t in range(2 ** in_num):
        s.add(sat_vars[f"v_{f}_{elem_num + in_num}_{t}"] == False)
        s.add(sat_vars[f"v_{f}_{elem_num + in_num + 1}_{t}"] == True)


    # ограничение 5 типа
    for k in range(m):
        for r in range(2 ** in_num):
            for i in alm.outputs:
                s.add(Or(Not(sat_vars[f"o_{f}_{i}_{k}"]), sat_vars[f"v_{f}_{i}_{r}"] == bool(value[k][r])))


    # ограничение 6 типа
    for i in range(4, alm.N - 1):
        for k, j in enumerate(alm.elements[i].inputs):
            s.add(
                Or(
                    And(sat_vars[f"c_{f}_{i}_{k}_{j}"], Not(sat_vars[f"c_{f}_{i}_{k}_{alm.N - 1}"])),
                    And(
                        Not(sat_vars[f"c_{f}_{i}_{k}_{j}"]),          
                        sat_vars[f"c_{f}_{i}_{k}_{alm.N - 1}"],
                        And([Not(sat_vars[f"c_{f}_{alm.N - 1}_{b}_{a}"])
                             for b in range(alm.elements[alm.N - 1].inputs_num) for a in alm.elements[i].next])
                    )
                )
            )


    # ограничение 4 типа
    for i in range(alm.N, elem_num):
        for r in range(2 ** in_num):
            for j in range(elem_num, elem_num + in_num + 2):
                for b in [0, 1]:
                    s.add(
                        Or(
                            Not(sat_vars[f"c_{f}_{i}_{j}"]),
                            Not(sat_vars[f"v_{f}_{j}_{r}"] == bool(b)),
                            sat_vars[f"v_{f}_{i}_{r}"] == sat_vars[f"t_{f}_{i}_{b}"]
                        )
                    )

    for r in range(2 ** in_num):
        for j0 in range(alm.N - 1):
            for j1 in range(j0 + 1, alm.N - 1):
                for b in range(2 ** 2):
                    i0 = (b >> 0) & 1
                    i1 = (b >> 1) & 1
                    s.add(
                        Not(And(
                            sat_vars[f"c_{f}_{alm.N - 1}_{0}_{j0}"], 
                            sat_vars[f"c_{f}_{alm.N - 1}_{1}_{j1}"],
                            sat_vars[f"v_{f}_{j0}_{r}"] == bool(i0),
                            sat_vars[f"v_{f}_{j1}_{r}"] == bool(i1),
                            Not(sat_vars[f"v_{f}_{alm.N - 1}_{r}"] == sat_vars[f"t_{f}_{alm.N - 1}_{b}"])
                        ))
                    )

    for i in range(alm.N - 1):
        if alm.elements[i].inputs_num == 2:
            for r in range(2 ** in_num):
                for j0 in [alm.elements[i].inputs[0], alm.N - 1]:
                    for j1 in [alm.elements[i].inputs[1], alm.N - 1]:
                        for b in range(2 ** 2):
                            i0 = (b >> 0) & 1
                            i1 = (b >> 1) & 1
                            s.add(
                                Not(And(
                                    sat_vars[f"c_{f}_{i}_{0}_{j0}"], 
                                    sat_vars[f"c_{f}_{i}_{1}_{j1}"],
                                    sat_vars[f"v_{f}_{j0}_{r}"] == bool(i0),
                                    sat_vars[f"v_{f}_{j1}_{r}"] == bool(i1),
                                    Not(sat_vars[f"v_{f}_{i}_{r}"] == sat_vars[f"t_{f}_{i}_{b}"])
                                ))
                            )
        elif alm.elements[i].inputs_num == 3:
            for r in range(2 ** in_num):
                for j0 in [alm.elements[i].inputs[0], alm.N - 1]:
                    for j1 in [alm.elements[i].inputs[1], alm.N - 1]:
                        for j2 in [alm.elements[i].inputs[2], alm.N - 1]:
                            for b in range(2 ** 3):
                                i0 = (b >> 0) & 1
                                i1 = (b >> 1) & 1
                                i2 = (b >> 2) & 1
                                s.add(
                                    Not(And(
                                        sat_vars[f"c_{f}_{i}_{0}_{j0}"], 
                                        sat_vars[f"c_{f}_{i}_{1}_{j1}"],
                                        sat_vars[f"c_{f}_{i}_{2}_{j2}"],
                                        sat_vars[f"v_{f}_{j0}_{r}"] == bool(i0),
                                        sat_vars[f"v_{f}_{j1}_{r}"] == bool(i1),
                                        sat_vars[f"v_{f}_{j2}_{r}"] == bool(i2),
                                        Not(sat_vars[f"v_{f}_{i}_{r}"] == sat_vars[f"t_{f}_{i}_{b}"])
                                    ))
                                )
        elif alm.elements[i].inputs_num == 4:
            for r in range(2 ** in_num):
                j0 = alm.elements[i].inputs[0]
                j1 = alm.elements[i].inputs[1]
                j2 = alm.elements[i].inputs[2]
                j3 = alm.elements[i].inputs[3]
                for b in range(2 ** 4):
                    i0 = (b >> 0) & 1
                    i1 = (b >> 1) & 1
                    i2 = (b >> 2) & 1
                    i3 = (b >> 3) & 1
                    s.add(
                        Not(And(
                            sat_vars[f"v_{f}_{j0}_{r}"] == bool(i0),
                            sat_vars[f"v_{f}_{j1}_{r}"] == bool(i1),
                            sat_vars[f"v_{f}_{j2}_{r}"] == bool(i2),
                            sat_vars[f"v_{f}_{j3}_{r}"] == bool(i3),
                            Not(sat_vars[f"v_{f}_{i}_{r}"] == sat_vars[f"t_{f}_{i}_{b}"])
                        ))
                    )

