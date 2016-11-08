__author__ = 'rikus'

class User(object):
    def __init__(self,id,name,passw,email,basketId=None):
        self._id = id
        self._name = name
        self._passw = passw
        self._email = email
        self._userbasketId = basketId

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getEmail(self):
        return self._email

    def getUserBasketId(self):
        return self._userbasketId

    def setUserBasketId(self,id):
        self._userbasketId = id

class UserHelpers(object):
    def getUserInfo(self,mysql,userName):
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from Users where UserEmail='" + userName + "'")
        return list(cursor)

    def getBasketId(self,userId,mysql):
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from Basket where Users_UserId=" + str(userId))
        return list(cursor)

    def listBasket(self,mysql,userObj):
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from BasketItems where Basket_BasketId='" + str(userObj.getUserBasketId()) + "'")
        return list(cursor)

