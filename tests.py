__author__ = 'rikus'
from Models.Item import *
from os import path,makedirs
from PIL import Image

userDict = {'1':'Rikus'}
print(userDict)

userDict['2'] = 'Lize'

print(userDict)

lst = [1,2,3,4,5,6]
print(lst[1])

userDict['1'] = "Renier"

print(userDict['1'])

emptyDict = {}
emptyDict['1'] = "a"
print(emptyDict)

lst2 = [x*x for x in range(1,10)]
print(lst2)

#range(*lst)

print(userDict['1'])
print(userDict)
for usr in userDict:
    print(userDict[usr])
    print(int(1.11))

itm1 = Item(1,"disc","www.google.com",100,"internet")
itm1.getItemId()

dic1 = { 'a':{'1':1} , 'b':{'2':2}}
print(dic1['a'])
dic2 = {}
dic2["a"] = {'1':1}
dic2["a"] = {'3':3}
print(dic2)

if ((3 > 2) & (3 < 4)):
    print('a')

chars = {'a':1,'b':2,'c':3,'d':4}

dic3 = {"a":1,"b":2}
print dic3["a"]
print dic3.keys()[0]

from datetime import *
timeNow = datetime.now()
print ("currentTime : " , str(timeNow).replace(" ",""))

try:
    a = 10/0
except :
    print("exception")

#password hash
import uuid
import hashlib

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    print("salt : " , salt)
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

passHash = hash_password("abc")
print('hash : ' , passHash)
print(check_password(passHash,"abc"))

lis4 = ['a','b']
print('c' in lis4)


currentPath = path.dirname(path.realpath(__file__))

def ensure_dir(f):
    # d = path.dirname(f)
    # print("d " + d )
    print("f " + f)
    if not path.exists(f):
        makedirs(f)

# ensure_dir(currentPath + "/static/pictures")

def createPicDir(picDir):
    currentPath = path.dirname(path.realpath(__file__))
    picPath = currentPath + "/static/pictures/" + picDir
    if not path.exists(picPath):
        makedirs(picPath)


# createPicDir("pants")
picPath = "/home/rikus/Desktop"
picURL = "/home/rikus/Desktop/pants2.jpg"
picName = "newPIC1.jpg"
try:
    im = Image.open(picURL)
    im.save(picPath+"/"+picName)
except:
    print("error")


def uploadPicture(picDir,picURL,picName):
    currentPath = path.dirname(path.realpath(__file__))
    picPath = currentPath + "/static/pictures/" + picDir
    if not path.exists(picPath):
        makedirs(picPath)
    try:
        im = Image.open(picURL)
        im.save(picPath+"/"+picName)
    except:
        print(picURL)
        print("no such file")

# uploadPicture("pants",picURL,picName)
picURLS = picURL.split("/")
print(picURLS)
print(picURLS.pop(-1))
