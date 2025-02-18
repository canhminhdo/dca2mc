import subprocess
import random
import socket
import maude
import json
import sys

# setup for Qlock
NAME = "qlock"
PROCS = 2
if len(sys.argv) > 1:
    SESS = sys.argv[1]
else:
    SESS = random.randint(1, 1000000)
FOLDER = f"{NAME}-{SESS}"
SPEC_TEMP_FILE = f"specs/{NAME}.pml.tmp"

# setup for socket
HOST = 'localhost'
PORT = 8811

# create a folder for the session
subprocess.run(["mkdir", "-p", FOLDER])

# load the Maude module
maude.init()
maude.load('qlock-loader.maude')
qlock = maude.getModule('QLOCK-DB')

def modelCheck(sf, n):
    global COUNT
    queue = qlock.parseTerm(f"getQueue(downTerm(getState({sf}), errState))")
    queue.reduce()
    pc = []
    for i in range(n):
        p = qlock.parseTerm(f"getLoc(downTerm(getState({sf}), errState), p{i + 1})")
        p.reduce()
        pc.append(p)

    cnt = qlock.parseTerm(f"getCnt(downTerm(getState({sf}), errState))")
    cnt.reduce()
    print(f"[Handling] queue: {queue}, pc: {pc}, cnt: {cnt}")

    # prepare specification
    file = open(SPEC_TEMP_FILE, "r", encoding="utf-8")
    content = file.read()
    
    # prepare the number of processes
    content = content.replace("<procs>", str(n))
    # prepare initialization for processes
    init = f"cnt = {cnt};"
    for i in range(n):
        p = qlock.parseTerm(f"getLoc(downTerm(getState({sf}), errState), p{i + 1})")
        p.reduce()
        init += f"\n\t\tpc[{i}] = {p};"
    elements = []
    if str(queue) != "empq":
        elements = str(queue).split(" | ")

    for ele in elements:
        idx = int(ele.replace("p", ""))
        init += f"\n\t\tqueue!{idx - 1};"
    content = content.replace("<init>", init)

    # preapre the formula
    formulas = qlock.parseTerm(f"AFL2Json(getAndFormulas({sf}))")
    formulas.reduce()
    JsonFLs = json.loads(str(formulas))
    # print(JsonFLs)

    flag = True
    for andFL in JsonFLs:
        # if andFL holds, continue. Otherwise, return False
        # print ("andFL: " + str(andFL))
        andFLRes = False
        for orFL in andFL:
            # if one orFL holds, return True. Otherwise, return False
            # print("orFL: " + str(orFL))
            orFLRes = True
            for fl in orFL:
                # if fl holds, return True. Otherwise, return False
                # print("fl: " + str(fl))
                spec = content.replace("<formula>", str(fl))
                with open(f"{FOLDER}/{NAME}.pml", "w", encoding="utf-8") as file:
                    file.write(spec)
                result = subprocess.run(["spin", "-run", f"{NAME}.pml"], cwd=FOLDER, capture_output=True, text=True)
                if "errors: 0" not in result.stdout:
                    orFLRes = False
                    print(result.stdout)
                # subprocess.run("rm -rf " + f"{FOLDER}/*", shell=True)
            if orFLRes :
                andFLRes = True
                break
        if not andFLRes:
            flag = False
            break
    return flag

def connectionSetup():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer = ""
    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT} with session {SESS}")
        
        while True:
            # Wait for any data from the server and print immediately
            data = client_socket.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')
            sf, buffer = buffer.split('#', 1)
            res = modelCheck(sf, PROCS)
            # Send a response to the server
            client_socket.send((str(res) + "#").encode('utf-8'))
            print(f"[Sent] {res}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")
        subprocess.run("rm -rf " + FOLDER, shell=True)

# modelCheck(
#     r"{ '`{_`} ['__ ['queue:_ ['p1.Pid ],'cnt:_ ['s_ ['0.Zero ]],'pc`[_`]:_ ['p1.Pid ,'ws.Loc ],'pc`[_`]:_ ['p2.Pid ,'fs.Loc ]]]: [{ ('_R_ ['False.FalseFormula ,'_\/_ ['~_ ['inWs1.Prop ],'_U_ ['True.TrueFormula ,'inCs1.Prop ]]]) | ('_U_ ['True.TrueFormula ,'inCs1.Prop ])}]}",
#     2
# )

if __name__ == "__main__":
    connectionSetup()