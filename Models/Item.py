__author__ = 'rikus'

class Item(object):
    def __init__(self,itemId,desc,picURL,price,category):
        self._itemId = itemId
        self._desc = desc
        self._picURL = picURL
        self._price = price
        self._category = category

    def getItemId(self):
        return self._itemId
    def getDesc(self):
        return self._desc
    def getPicURL(self):
        return self._picURL
    def getPrice(self):
        return self._price
    def getCategory(self):
        return self._category

class ItemHelpers(object):
    def getAllItems(self,mysql):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from Catalog ")
        result = list(cursor)
        conn.close()
        return result

    def addToBasket(self,mysql,basketId,catalogId):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("Insert into BasketItems (Basket_BasketId,Catalog_CatalogId) values ('"+str(basketId)+"','"+str(catalogId)+"')")
        conn.commit()
        conn.close()

    def removeFromBasket(self,mysql,basketId,catalogId):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("Delete from BasketItems where Basket_BasketId=" + "'"+str(basketId)+"'" + "and Catalog_CatalogId="+ "'"+str(catalogId)+"'")
        conn.commit()
        conn.close()

    def addToDB(self,mysql,desc,picURL,price,category):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Catalog (CatalogDescription, CatalogPictureURL, CatalogPrice, CatalogCategory)  VALUES ('"+str(desc)+"','"+str(picURL)+"','"+str(price)+"','"+str(category)+"')")
        conn.commit()
        conn.close()

    def remoteFromDB(self,mysql,desc,category):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("Delete from Catalog where CatalogDescription=" + "'"+str(desc)+"'" + "and CatalogCategory="+ "'"+str(category)+"'")
        conn.commit()
        conn.close()