import subprocess
import random
import socket
import maude
import json
import sys

# setup the protocol under verification
TAS_PROG, QLOCK_PROG, ANDERSON_PROG, TICKET_PROG, MCS_PROG = ["tas", "qlock", "anderson", "ticket", "mcs"]
NAME = QLOCK_PROG
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

# processed items
COUNT = 0

# create a folder for the session
subprocess.run(["mkdir", "-p", FOLDER])

# load the Maude module
maude.init()
if NAME == TAS_PROG:
    from parsing.tas import buildInit
    maude.load('parsing/tas-loader.maude')
    prog = maude.getModule('TAS-DB')
elif NAME == QLOCK_PROG:
    from parsing.qlock import buildInit
    maude.load('parsing/qlock-loader.maude')
    prog = maude.getModule('QLOCK-DB')
elif NAME == ANDERSON_PROG:
    from parsing.anderson import buildInit
    maude.load('parsing/anderson-loader.maude')
    prog = maude.getModule('ANDERSON-DB')
elif NAME == MCS_PROG:
    from parsing.mcs import buildInit
    maude.load('parsing/mcs-loader.maude')
    prog = maude.getModule('MCS-DB')
elif NAME == TICKET_PROG:
    from parsing.ticket import buildInit
    maude.load('parsing/ticket-loader.maude')
    prog = maude.getModule('TICKET-DB')

def modelCheck(sf, n):
    # prepare specification
    file = open(SPEC_TEMP_FILE, "r", encoding="utf-8")
    content = file.read()
    file.close()
    
    # prepare the number of processes
    content = content.replace("<procs>", str(n))

    # prepare initialization for processes
    init = buildInit(prog, sf, n)
    # print(f"[Init] {init}")
    content = content.replace("<init>", init)
    
    # preapre the formula
    formulas = prog.parseTerm(f"AFL2Json(getAndFormulas({sf}))")
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
                # print(result.stdout)
                # subprocess.run("rm -rf " + f"{FOLDER}/*", shell=True)
            if orFLRes :
                andFLRes = True
                break
        if not andFLRes:
            flag = False
            break
    return flag

def connectionSetup():
    global COUNT
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
            new_data = data.decode('utf-8')
            buffer += new_data
            if new_data.find('#') == -1:
                continue;
            sf, buffer = buffer.split('#', 1)
            res = modelCheck(sf, PROCS)
            COUNT += 1
            # Send a response to the server
            client_socket.send((str(res) + "#").encode('utf-8'))
            print(f"[Sent] {res} - {COUNT} items")
            if not res:
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")
        subprocess.run("rm -rf " + FOLDER, shell=True)

if __name__ == "__main__":
    connectionSetup()