#define N   10	/* number of processes */

mtype = {ss, ws, cs, fs};
mtype pc[N] = ss;
int cnt = N;
chan queue = [N] of { int };

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
        queue!idx;
    }
    :: atomic {
        pc[idx] == ws; queue?<eval(idx)>; ->
        pc[idx] = cs;
    }
    :: atomic {
        pc[idx] == cs ->
        queue?_;
        pc[idx] = fs;
        cnt--;
    }
    :: cnt == 0 ->
        break;
    od
    assert(cnt == 0);
}

// [Spin] uncomment one of the following properties and run `spin -run qlock.pml`
// ltl mutex { [] !(pc[0] == cs && pc[1] == cs) }
// ltl lofree { [] ((pc[0] == ws) -> (<> (pc[0] == cs))) }
// ltl halt { <> (pc[0] == fs) }

// [LTSmin] comment all properties above and run as follows in the terminal
// spins -o3 qlock.pml
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' qlock.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' qlock.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='[] ((pc\[0\] == "ws") -> (<> (pc\[0\] == "cs")))' qlock.pml.spins
// prom2lts-seq --por --proviso=color --strategy=scc --ltl='<> (pc\[0\] == "fs")' qlock.pml.spins
// prom2lts-mc --strategy=cndfs --threads=8 --ltl='<> (pc\[0\] == "fs")' qlock.pml.spins
// prom2lts-mc --strategy=ufscc --threads=8 --ltl='<> (pc\[0\] == "fs")' qlock.pml.spins