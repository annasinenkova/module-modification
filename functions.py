def adding_functions(file_name):
    '''value = []
    with open(file_name) as f:
        num = f.readline()
        while num:
            v = []
            for i in range(int(num)):
                line = f.readline().strip()
                v.append([int(c) for c in line])
            value.append(v)
            num = f.readline()
    return value'''
    
    func = []
    for i in range(2 ** (2 ** 2)):
        l = [0, 0, 0, 0]
        l[3] = (i >> 0) & 1
        l[2] = (i >> 1) & 1
        l[1] = (i >> 2) & 1
        l[0] = (i >> 3) & 1
        func.append(l)
    value = []
    for i in range(len(func)):
        for j in range(i + 1, len(func)):
            for k in range(j + 1, len(func)):
                for l in range(k + 1, len(func)):
                    g = [func[i], func[j], func[k], func[l]]
                    value.append(g)
    return(value)
