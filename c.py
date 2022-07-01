import socket
import sys

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 1373        # Port to listen on (non-privileged ports are > 1023)

def main():
    print(format(sys.argv) )
    
    if len(sys.argv) <= 3:
        print("invalid:/")
        sys.exit()

    if sys.argv[1] == "127.0.0.1" and sys.argv[2] == "1373" :
        #its OK
        HOST = '127.0.0.1' 
        PORT = 1373

    else:
        print("Cannot connect to server:(")
        sys.exit()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_information = (HOST, PORT)

    try:
        s.connect(server_information)
        print("Client connected :)")
    except:
        print("cannot connect :(")

    client_send_msg(s)


def client_send_msg(s: socket.socket):
    while True:
        rule_msg = sys.argv[3]
        if rule_msg == "subscribe":
            ####
            if len(sys.argv[4:]) == 0:
                print("write some titles :(")
                sys.exit()
            data_sub = "subscribe"
            for msg in sys.argv[4:]:
                data_sub += " " + msg
            send(s, data_sub)
            ####
        elif rule_msg == "publish":
            ###
            data_pub = "publish"
            if len(sys.argv[4:]) == 0:
                print("write some titles :(")
                sys.exit()
            if len(sys.argv[4:]) == 1:
                print("write some messages :(")
                sys.exit()

            for msg in sys.argv[4:]:
                data_pub += " " + msg
            send(s, data_pub)
            ###
        elif rule_msg == "ping":
            send(s, "ping")
        else:
            print("rule_msg was not subscribe / publish / ping")
            sys.exit()
        try:
            ####
            s.settimeout(10.0)
            print("settime 10.0")
            while True:
                #print("while true")
                data_server = s.recv(1024)

                if data_server:
                    #print("if data_server:")
                    s.settimeout(None)
                    data_server = data_server.decode('ascii')
                    print(data_server)
                    Reaction = data_server.split()
                    if "subAck:" in data_server:
                        print("Subscribing: ")
                        for title in Reaction[1:]:
                            print(title)
                    elif Reaction[0] == 'pong':
                        sys.exit()
                    elif data_server == "pubAck":
                        print("message published")
                        sys.exit()
                    elif data_server =="invalid title_pub":
                        sys.exit()
            ####
        except socket.error:
            #print(socket.error)
            print("timeout")

def send(client, message):
    client.send(message.encode('ascii'))


if __name__ == "__main__":
    main()