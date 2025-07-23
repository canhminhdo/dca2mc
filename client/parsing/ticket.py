def buildInit(prog, sf, n):
    # counter
    cnt = prog.parseTerm(f"getCnt(downTerm(getState({sf}), errState))")
    cnt.reduce()
    # next
    next = prog.parseTerm(f"getNext(downTerm(getState({sf}), errState))")
    next.reduce()
    # serve
    serve = prog.parseTerm(f"getServe(downTerm(getState({sf}), errState))")
    serve.reduce()
    # locations & places & array
    pc = []
    tickets = []
    for i in range(n):
        # locations
        p = prog.parseTerm(f"getLoc(downTerm(getState({sf}), errState), p{i + 1})")
        p.reduce()
        pc.append(p)
        # tickets
        ticket = prog.parseTerm(f"getTicket(downTerm(getState({sf}), errState), p{i + 1})")
        ticket.reduce()
        tickets.append(ticket)

    print(f"[Handling] next: {next}, pc: {pc}, ticket: {tickets}, cnt: {cnt}")

    # build the initialization
    init = f"cnt = {cnt};"
    init += f"\n\t\tnext = {next};"
    init += f"\n\t\tserve = {serve};"
    for i in range(n):
        init += f"\n\t\tpc[{i}] = {pc[i]};"
        init += f"\n\t\tticket[{i}] = {tickets[i]};"
    
    return init