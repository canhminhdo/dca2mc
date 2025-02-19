def buildInit(prog, sf, n):
    # counter
    cnt = prog.parseTerm(f"getCnt(downTerm(getState({sf}), errState))")
    cnt.reduce()
    # lock
    lock = prog.parseTerm(f"getLock(downTerm(getState({sf}), errState))")
    lock.reduce()
    # locations
    pc = []
    for i in range(n):
        p = prog.parseTerm(f"getLoc(downTerm(getState({sf}), errState), p{i + 1})")
        p.reduce()
        pc.append(p)

    print(f"[Handling] lock: {lock}, pc: {pc}, cnt: {cnt}")

    # build the initialization
    init = f"cnt = {cnt};"
    init += f"\n\t\tlocked = {lock};"
    for i in range(n):
        init += f"\n\t\tpc[{i}] = {pc[i]};"
    
    return init