#define N   6	/* number of processes */

mtype = {l1, l2, l3, l4, l5, ws, l7, l8, l9, l10, l11, fs, ss, cs};
int nop = N;

int glock = nop;
mtype pc[N] = ss;
int next[N] = nop;
bool lock[N] = false;
int pred[N] = nop;
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
        // want
        pc[idx] == ss ->
        pc[idx] = l1;
    }
    :: atomic {
        // stnxt
        pc[idx] == l1 ->
        pc[idx] = l2;
        next[idx] = nop;
    }
    :: atomic {
        // stprd
        pc[idx] == l2 ->
        pc[idx] = l3;
        pred[idx] = glock;
        glock = idx;
    }
    :: atomic {
        // chprd
        pc[idx] == l3 ->
        pc[idx] = (pred[idx] == nop -> cs : l4);
    }
    :: atomic {
        // stlck
        pc[idx] == l4 ->
        pc[idx] = l5;
        lock[idx] = true;
    }
    :: atomic {
        // stnpr
        pc[idx] == l5 ->
        pc[idx] = ws;
        next[pred[idx]] = idx;
    }
    :: atomic {
        // chlck
        pc[idx] == ws && lock[idx] == false ->
        pc[idx] = cs;
    }
    :: atomic {
        // exit
        pc[idx] == cs ->
        pc[idx] = l7;
    }
    :: atomic {
        // rpnxt
        pc[idx] == l7 ->
        pc[idx] = (next[idx] == nop -> l8 : l11);
    }
    :: atomic {
        // chglk
        pc[idx] == l8 ->
        pc[idx] = (glock == idx -> l9 : l10);
        glock = (glock == idx -> nop : glock);
    }
    :: atomic {
        // go2rs
        pc[idx] == l9 ->
        pc[idx] = fs;
        cnt--;
    }
    :: atomic {
        // rpnxt
        pc[idx] == l10 && next[idx] != nop ->
        pc[idx] = l11;
    }
    :: atomic {
        // stlnx
        pc[idx] == l11 ->
        pc[idx] = fs;
        lock[next[idx]] = false;
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

// spins -o3 mcs.pml
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' mcs.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' mcs.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' mcs.pml.spins
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='<> (pc\[0\] == "fs")' mcs.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='<> (pc\[0\] == "fs")' mcs.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='<> (pc\[0\] == "fs")' mcs.pml.spins