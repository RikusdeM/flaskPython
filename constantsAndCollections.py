__author__ = 'rikus'

################################################################################################################
#Constants
################################################################################################################
SESSIONTIMEOUT = 1800 #//default timeout in seconds for a session



################################################################################################################
#Collections
################################################################################################################
ItemsDAO = {} #all items in store .{ItemId:ItemObj}
UsersDAO = {} #all users in store .{}

################################################################################################################
#Admins
################################################################################################################
AdminUsers = ["rikus@gmail.com"] #all admin users that may change db entries