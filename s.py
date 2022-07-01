import socket
import threading
#define host number and port number and array of tittles those listened
HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 1373        # Port to listen on (non-privileged ports are > 1023)
titles = {}

def main():
    host = (HOST, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(host)
    s.listen()
    print("listening by Server")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()


def handle_client(conn, addr):
    print("[new connection] connected from{}".format(addr))

    while True:
        try:
            data = conn.recv(1024)
            if data:
                data = data.decode('ascii')
                print("massage: ")
                print(data)
                check_ping_sub_pub(data, conn)
        except:
            for title in titles.keys():
                if conn in titles[title]:
                    titles[title].remove(conn)
            conn.close()
            print('Disconnected by', addr)
            break


def check_ping_sub_pub(data, conn):
    rule_msg = data.split()
    if rule_msg[0] == "subscribe":
        ####
        data_sub = "subAck:"
        for title_sub in rule_msg[1:]:
            data_sub += " " + title_sub
            if title_sub in titles.keys():
                titles[title_sub].append(conn)
            else:
                titles[title_sub] = [conn]

        send(conn, data_sub)
        ####
    elif rule_msg[0] == "publish":
        title_pub = rule_msg[1]
        data_pub = title_pub + " :"
        for msg in rule_msg[2:]:
            data_pub += " " + msg
        if title_pub not in titles.keys():
            send(conn, "invalid title_pub")
        else:
            send(conn, "pubAck")
            for c in titles[title_pub]:
                try:
                    send(c, data_pub)
                except:
                    for l in titles.keys():
                        if c in titles[l]:
                            titles[l].remove(c)
                    c.close()
        ####
    elif rule_msg[0] == "ping":
        send(conn, "pong")


def send(server, msg):
    server.send(msg.encode('ascii'))

if __name__ == "__main__":
    main()
