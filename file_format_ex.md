Any line starting with a # will be ignored, allowing for comments.

#Room
name;keyword:keyword:...:keyword;attribute,arg1,arg2:attribute,arg1,arg2;short_desc;description;possible_start

Possible_start should be 1 if true, 0 if false, or something else similarly convenient.

No room should have the same keyword to avoid ambiguity.

#Decoration
name;keyword:keyword:...:keyword;attribute,arg1,arg2:attribute,arg1,arg2;short_desc;description;room

'room' should be a keyword of the room it appears in.

#Item
name;keyword:keyword:...:keyword;attribute,arg1,arg2:attribute,arg1,arg2;short_desc;description;room

'room' should be a keyword of the room it appears in.

#Connection
name;keyword:keyword:...:keyword;attribute,arg1,arg2:attribute,arg1,arg2;short_desc;description;source;destination;pass_desc;locked;locked_desc

locked should be 1 if true, 0 if false, or something else similarly convenient.

locked_desc can be empty if the passage will never lock.

'source' and 'destination' should each be a keyword of the relevant rooms.