import select
import socket
import sys
import pickle

from room import Room
from player import Player
from world import World

def valid_name(name):
    if ' ' in name:
        return False
    return True

def handle_message(client, player_data, msg, world):
    if player_data[client] is None:
        if valid_name(msg):
            player_data[client] = Player(client, msg)
            client.sendall(pickle.dumps('Welcome, {}'.format(msg)))
            world.add_player(player_data[client])
        else:
            client.sendall(pickle.dumps('Invalid username.'))
            client.sendall(pickle.dumps('What is your name?'))

def create_world():
    world = World()

    barracks = Room('Barracks',
        'a barracks, cleaned with military efficiency.', possible_start=True)
    world.add_room(barracks)

    return world

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
    player_data = {}

    world = create_world()

    running = True
    while running:
        input_ready, output_ready, except_ready = select.select(clients, [], [])
        
        for s in input_ready:
            if s == server:
                client, address = server.accept()
                print("Received connection from {}.".format(address))
                clients.append(client)
                player_data[client] = None
                client.sendall(pickle.dumps('What is your name?'))

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
                    handle_message(s, player_data, data, world)
                else:
                    #this socket closed
                    print("Connection closed remotely.")
                    s.close()
                    clients.remove(s)
                    del player_data[s]

    server.close()


if __name__ == '__main__':
    main()
