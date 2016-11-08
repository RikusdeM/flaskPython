__author__ = 'rikus'
from datetime import datetime
from pysnapscan.api import SnapScan
from constantsAndCollections import ItemsDAO
SNAPCODE = 'abcd'
API_KEY = '8130a729-552d-4eb6-bc3a-726e9c326c1c'

ss = SnapScan(SNAPCODE, API_KEY)

def generateURL(basketList):
    unique_id = str(datetime.now()).replace(" ","")
    print("basketList[2] : ",basketList)
    totalPrice = 0
    for basketItem in basketList:
        # "#" -> Basket_BasketId
        # "&" -> Catalog_CatalogId
        unique_id = unique_id +"#" + str(basketItem[1]) + "&" + str(basketItem[2])
        totalPrice = totalPrice + int(ItemsDAO[basketItem[2]].getPrice().replace("R",""))
    # print("PRICE : " , totalPrice)
    # print("Uid : ",unique_id)
    url = ss.generate_qr_code_url(
        uid=unique_id,# unique identifier for payment
        amount=totalPrice,# amount in Rands
        snap_code_size=250, # 50 - 500
        img_type='.svg', # .svg or .png
        strict=True # amount cannot be edited, QR cannot be reused
    )
    return url

def getPayments():
    payments = ss.get_payments(
        page=1, # if pagination is needed
        per_page=10,
        offset=0
    )
    return payments

# cashup_period = ss.create_cash_up_period(datetime.now(), 'adg322sgq3')

