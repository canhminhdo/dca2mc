#define N	13	/* number of processes */

mtype = {ss, ws, cs, fs};
mtype pc[N] = ss;
bool locked = false;
int cnt = N;

init {
    atomic {
        int idx = 0;
        do 
        :: (idx < N) -> 
            run proc(idx);
            idx++;
        :: else -> break;
        od
    }
}

proctype proc(int idx)
{
    do
	:: atomic {
        pc[idx] == ss ->
        pc[idx] = ws;
    }
    :: atomic {
        pc[idx] == ws && locked == false ->
        pc[idx] = cs;
        locked = true;
    }
    :: atomic {
        pc[idx] == cs ->
        pc[idx] = fs;
        cnt--;
        locked = false;
    }
    :: cnt == 0 ->
        break;
    od
    assert(cnt == 0);
}

// ltl mutex { [] !(pc[0] == cs && pc[1] == cs) }
// ltl lofree { [] ((pc[1] == ws) -> (<> (pc[1] == cs))) }
// ltl halt { <> (pc[0] == fs) }

// spins -o3 tas.pml
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' tas.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' tas.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' tas.pml.spins
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='<> (pc\[0\] == "fs")' tas.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='<> (pc\[0\] == "fs")' tas.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='<> (pc\[0\] == "fs")' tas.pml.spins