def buildInit(prog, sf, n):
    # counter
    cnt = prog.parseTerm(f"getCnt(downTerm(getState({sf}), errState))")
    cnt.reduce()
    # queue
    queue = prog.parseTerm(f"getQueue(downTerm(getState({sf}), errState))")
    queue.reduce()
    # locations
    pc = []
    for i in range(n):
        p = prog.parseTerm(f"getLoc(downTerm(getState({sf}), errState), p{i + 1})")
        p.reduce()
        pc.append(p)
    
    print(f"[Handling] queue: {queue}, pc: {pc}, cnt: {cnt}")

    # build the initialization
    init = f"cnt = {cnt};"
    for i in range(n):
        init += f"\n\t\tpc[{i}] = {pc[i]};"
    elements = []
    if str(queue) != "empq":
        elements = str(queue).split(" | ")

    for ele in elements:
        idx = int(ele.replace("p", ""))
        init += f"\n\t\tqueue!{idx - 1};"

    return init