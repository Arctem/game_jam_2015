import select
import socket
import sys
import pickle

from attribute.weapon import RangedWeapon
from connection import Connection
from decoration import Decoration
from special.clone import ClonePod
from item import Item
from room import Room
from player import Player
from world import World

def valid_name(name, player_data):
    if ' ' in name:
        return False
    for k in player_data:
        if player_data[k] and player_data[k].name == name:
            return False
    return True

def handle_message(client, player_data, msg, world):
    player = player_data[client]
    if player is None:
        if valid_name(msg, player_data):
            player_data[client] = Player(client, msg, world)
            client.sendall(pickle.dumps('Welcome, {}.'.format(msg)))
            client.sendall(pickle.dumps('This is Vessel XIV. Please report to the briefing room.'.format(msg)))
            world.add_player(player_data[client])
        else:
            client.sendall(pickle.dumps('Invalid username.'))
            client.sendall(pickle.dumps('What is your name?'))
    else:
        cmd = msg.split(' ')[0]
        args = ' '.join(msg.split(' ')[1:])
        cmd = cmd.upper()
        if cmd == 'LOOK':
            if len(args) == 0:
                player.send_room_description()
            else:
                looked_at = False
                for obj in player.room.contents + player.room.connections:
                    if args.lower() in (obj.keywords if\
                        isinstance(obj, Connection) else obj.name.lower()):
                        looked_at = True
                        player.send_msg(obj.description())
                if not looked_at:
                    player.send_msg('There is no {} here.'
                        .format(args))
        elif cmd == 'GO':
            if len(args) == 0:
                player.send_msg('Where do you want to go?')
            else:
                went = False
                for con in player.room.connections:
                    if args.lower() in con.keywords:
                        if con.locked:
                            player.send_msg(con.locked_desc)
                        else:
                            player.move_through(con)
                        went = True
                        break
                if not went:
                    player.send_msg("Can't go {}.".format(args))
        elif cmd == 'SAY':
            player.inform_others('{} says "{}".'.format(player.name, args))
            player.send_msg('You say "{}".'.format(args))
        elif cmd == 'TAKE':
            player.take_item(args)
        else:
            extras = player.gather_actions()
            if cmd in extras:
                extras[cmd](player, args)
            else:
                player.send_msg("You can't {} here.".format(cmd))

def create_world():
    world = World()

    """"barracks = Room('Barracks', 'the barracks',
        'a barracks, cleaned with military efficiency.', ['barracks'],
        possible_start=True)
    canteen = Room('Canteen', 'a canteen',
        'a canteen, cleaned with civilian efficiency.', ['canteen'],
        possible_start=True)
    barracks.add_content(Item("Ray's Gun", 'a small pistol',
        'A gun with "Ray" embossed on the side.', ['pistol', 'gun', 'ray',
        'ray gun'], [RangedWeapon()]))
    canteen.add_content(Decoration('Skeletons', 'a pile of spooky skeletons',
        'A pile of assorted human bones.', ['pile', 'skeleton', 'skeletons',
        'bones']))
    canteen.add_content(ClonePod())
    barracks.add_connection(Connection(barracks, canteen, 'a hallway',
        'A hallway leading to the canteen.',
        'You walk through the hallway.', ('hall',)))
    canteen.add_connection(Connection(canteen, barracks, 'a hallway',
        'A hallway leading to the barracks.',
        'You walk through the hallway.', ('hall',)))
    world.add_room(barracks)
    world.add_room(canteen)"""

    #Room Additions #name;keyword:keyword:...:keyword;attribute:attribute;short_desc;description;possible_start
    f = open('list_rooms.txt', 'r')
    rooms = f.read()
    rooms = rooms.split('\n')
    for i in rooms:
        if i and i[0] != '#':
            name, keyword, attribute, short_desc, description, possible_start = i.split(';')
            print (i)
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            if possible_start == "0":
                    possible_start = False
            else:
                    possible_start = True
            world.add_room(Room(name, short_desc, description,keyword,attribute, possible_start))
    f.close()
 
    
    #Decoration Additions
    #name;keyword:keyword:...:keyword;attribute:attribute;short_desc;description;room

    f = open('list_decorations.txt', 'r')
    decs = f.read()
    decs = decs.split('\n')
    for i in decs:
        if i and i[0] != '#':
            name, keyword, attribute, short_desc, description, room = i.split(';');
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            for r in world.rooms:
                if room in r.keywords:
                    r.add_content(Decoration(name, keyword,attribute,short_desc, description))
                    break
    f.close()
    
    #Item Additions
    f = open('list_items.txt', 'r')
    decs = f.read()
    decs = decs.split('\n')
    for i in decs:
        if i and i[0] != '#':
            name, keyword, attribute, short_desc, description, room = i.split(';');
            print (name)
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            for r in world.rooms:
                if room in r.keywords:
                    r.add_content(Item(name, keyword,attribute,short_desc, description))
                    break
    f.close()
    
    #Connections Additions

    f = open('list_connections.txt', 'r')
    decs = f.read()
    decs = decs.split('\n')
    for i in decs:
        if i and i[0] != '#':
            name, keyword, attribute, short_desc, description, source, destination, pass_desc, locked, locked_desc = i.split(';');
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            if locked == 0:
                    locked = False
            else:
                    locked = True
            for s in world.rooms:
                if source in s.keywords:
                    for d in world.rooms:
                        if destination in d.keywords:
                            s.add_connection(Connection(s,d, short_desc, description, pass_desc, keyword,attribute, locked))
                            break
    f.close()
    
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
