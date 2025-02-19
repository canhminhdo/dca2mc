def buildInit(prog, sf, n):
    # counter
    cnt = prog.parseTerm(f"getCnt(downTerm(getState({sf}), errState))")
    cnt.reduce()
    # next
    next = prog.parseTerm(f"getNext(downTerm(getState({sf}), errState))")
    next.reduce()
    # locations & places & array
    pc = []
    places = []
    arrs = []
    for i in range(n):
        # locations
        p = prog.parseTerm(f"getLoc(downTerm(getState({sf}), errState), p{i + 1})")
        p.reduce()
        pc.append(p)
        # places
        place = prog.parseTerm(f"getPlace(downTerm(getState({sf}), errState), p{i + 1})")
        place.reduce()
        places.append(place)
        # array
        arr = prog.parseTerm(f"getArray(downTerm(getState({sf}), errState), {i})")
        arr.reduce()
        arrs.append(arr)

    print(f"[Handling] next: {next}, pc: {pc}, place: {places}, array: {arrs}, cnt: {cnt}")

    # build the initialization
    init = f"cnt = {cnt};"
    init += f"\n\t\tnext = {next};"
    for i in range(n):
        init += f"\n\t\tpc[{i}] = {pc[i]};"
        init += f"\n\t\tplace[{i}] = {places[i]};"
        init += f"\n\t\tarray[{i}] = {arrs[i]};"
    
    return init