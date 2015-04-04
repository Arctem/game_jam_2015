

def main():
    #Room Additions
    #name;keyword:keyword:...:keyword;attribute:attribute;short_desc;description;possible_start
	f = open('list_rooms.txt', 'r')
    rooms = f.read()
    rooms = rooms.split()
    for i in rooms:
        if i[0] != '#':
            name, keyword, attribute, short_desc, description, possible_start = i.split(';');
            print (name)
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            if possible_start == 0:
                    possible_start = False
            else:
                    possible_start = True
            world.add_room(Room(name, short_desc, description,keyword,attribute, possible_start))
    f.close()
	
    #Decoration Additions
    #name;keyword:keyword:...:keyword;attribute:attribute;short_desc;description;room

	f = open('list_decs.txt', 'r')
    decs = f.read()
    decs = decs.split()
    for i in decs:
        if i[0] != '#':
            name, keyword, attribute, short_desc, description, room = i.split(';');
            print (name)
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            for r in world.rooms:
                if room in r.keywords:
                    r.add_content(decoration(name, keyword,attribute,short_desc, description))
                    break
    f.close()

    #Item Additions

	f = open('list_items.txt', 'r')
    decs = f.read()
    decs = decs.split()
    for i in decs:
        if i[0] != '#':
            name, keyword, attribute, short_desc, description, room = i.split(';');
            print (name)
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            for r in world.rooms:
                if room in r.keywords:
                    r.add_content(item(name, keyword,attribute,short_desc, description))
                    break
    f.close()
    
    #Connections Additions

	f = open('list_cons.txt', 'r')
    decs = f.read()
    decs = decs.split()
    for i in decs:
        if i[0] != '#':
            name, keyword, attribute, short_desc, description, source, destination, pass_desc, locked, locked_desc = room.split(';');
            print (name)
            keyword = keyword.split(':')
            attribute = attribute.split(':')
            attribute = list(map(lambda a: a.split(',', 1), attribute))
            if locked == 0:
                    locked = False
            else:
                    locked = True
            for s in world.rooms:
                if source in s.keywords:
                    for d in s.keywords:
                        if destination in d.keywords:
                            s.add_connection(connection(s,d, short_desc, description, pass_desc, keyword,attribute, locked))
                            break
    f.close()
    
    

if __name__ == '__main__':
    main()