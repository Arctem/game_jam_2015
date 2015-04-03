import select
import socket
import sys
import pickle

def main():
    host = ''
    port = 50001
    backlog = 5
    size = 1024
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(backlog)

    clients = [server]

    running = True
    while running:
        input_ready, output_ready, except_ready = select.select(clients, [], [])
        
        for s in input_ready:
            if s == server:
                client, address = server.accept()
                print("Received connection from {}.".format(address))
                clients.append(client)

            else:
                #handle other sockets
                try:
                    data = s.recv(size)
                except (ConnectionResetError, TimeoutError) as e:
                    #count as closed if other connection terminated early
                    data = None
                #print(data)
                if data:
                    data = pickle.loads(data)
                    print(data)
                    for c in clients:
                        if c is not server:
                            c.sendall(pickle.dumps(data))
                else:
                    #this socket closed
                    print("Connection closed remotely.")
                    s.close()
                    clients.remove(s)

    server.close()


if __name__ == '__main__':
    main()
