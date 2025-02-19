#define N   9	/* number of processes */

mtype = {rs, ws, cs, fs};
mtype pc[N] = rs;
int place[N] = 0;
bool array[N] = false;
int next = 0;
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
    atomic {
        if
        :: idx == 0 ->
            array[idx] = true;
        :: else ->
            skip;
        fi
    }
    do
	:: atomic {
        pc[idx] == rs ->
        pc[idx] = ws;
        place[idx] = next;
        next = (next + 1) % N;
    }
    :: atomic {
        pc[idx] == ws && array[place[idx]] == true ->
        pc[idx] = cs;
    }
    :: atomic {
        pc[idx] == cs ->
        pc[idx] = fs;
        array[place[idx]] = false;
        array[(place[idx] + 1) % N] = true;
        cnt--;
    }
    :: cnt == 0 ->
        break;
    od
    assert(cnt == 0);
}

// ltl mutex { [] !(pc[0] == cs && pc[1] == cs) }
// ltl lofree { [] ((pc[0] == ws) -> (<> (pc[0] == cs))) }
// ltl halt { <> (pc[0] == fs) }

// spins -o3 anderson.pml
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' anderson.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' anderson.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' anderson.pml.spins
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='<> (pc\[0\] == "fs")' anderson.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='<> (pc\[0\] == "fs")' anderson.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='<> (pc\[0\] == "fs")' anderson.pml.spins