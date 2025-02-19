def buildInit(prog, sf, n):
    # counter
    cnt = prog.parseTerm(f"getCnt(downTerm(getState({sf}), errState))")
    cnt.reduce()
    # glock
    glock = prog.parseTerm(f"getGlock(downTerm(getState({sf}), errState))")
    glock.reduce()
    # locations & nexts & locks & preds
    pc = []
    nexts = []
    locks = []
    preds = []
    for i in range(n):
        # locations
        p = prog.parseTerm(f"getLoc(downTerm(getState({sf}), errState), p{i + 1})")
        p.reduce()
        pc.append(p)
        # nexts
        next = prog.parseTerm(f"getNext(downTerm(getState({sf}), errState), p{i + 1})")
        next.reduce()
        nexts.append(next)
        # locks
        lock = prog.parseTerm(f"getLock(downTerm(getState({sf}), errState), p{i + 1})")
        lock.reduce()
        locks.append(lock)
        # preds
        pred = prog.parseTerm(f"getPred(downTerm(getState({sf}), errState), p{i + 1})")
        pred.reduce()
        preds.append(pred)

    print(f"[Handling] glock: {glock}, pc: {pc}, next: {next}, lock: {locks}, pred: {preds}, cnt: {cnt}")

    # build the initialization
    init = f"cnt = {cnt};"
    init += f"\n\t\tglock = {glock};"
    for i in range(n):
        init += f"\n\t\tpc[{i}] = {pc[i]};"
        init += f"\n\t\tnext[{i}] = {nexts[i]};"
        init += f"\n\t\tlock[{i}] = {locks[i]};"
        init += f"\n\t\tpred[{i}] = {preds[i]};"

    return init