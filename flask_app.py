from flask import *
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL
from constantsAndCollections import SESSIONTIMEOUT,ItemsDAO,UsersDAO,AdminUsers
from Models.Item import Item,ItemHelpers
from Models.User import User,UserHelpers
from Models.Payment import *
from os import path,makedirs,urandom
from jinja2 import Template
from PIL import Image

from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

mysql = MySQL()
app = Flask("FlaskApp")
Bootstrap(app)                                                  # Bootstrap config
app.config['MYSQL_DATABASE_USER'] = 'rikus'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rikus'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['PERMANENT_SESSION_LIFETIME'] = SESSIONTIMEOUT
app.jinja_env.add_extension('jinja2.ext.do')
mysql.init_app(app)

app.secret_key = urandom(24)

@app.route('/')
def indexPage():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('bootstrap_index.html'),200,headers)

@app.route('/temp')
def testTemp(name=None):
    return render_template('test_template.html', names=["rikus","lize"])


@app.route('/testdb')
def testDb():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM Users")
    data = cursor.fetchone()
    usersDict = {}
    while (data != None):
        userList = []
        for entry in data:
            userList.append(entry)
        usersDict[data[0]] = userList
        data = cursor.fetchone()
    return jsonify(usersDict)

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST': #auth user
         if auth(request.form['Email'],request.form['Password']) == True:
             session['username'] = request.form['Email'] #assign session to user
             createItemsDAO()
             createUserDAO(session['username'])
             basketList = showBasket(UsersDAO[session['username']])
             return render_template('logged_in.html',itemPics="handbags",items=ItemsDAO,basket=basketList,admin=checkAdmin())

         else:
             # return ("wrong username or password")
            return render_template('failed_login.html')
    else:
        if 'username' in session:
            return render_template('logged_in.html',admin=checkAdmin())
        else:
            return redirect('/')

@app.route('/login/<itemCategory>',methods=['GET']) #alternative login for showing different item cataloges
def loginAlternative(itemCategory):
    error = None
    if 'username' in session:
        basketList = showBasket(UsersDAO[session['username']])
        return render_template('logged_in.html',itemPics=itemCategory,items=ItemsDAO,basket=basketList,admin=checkAdmin())
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')

@app.route('/static/<resource_name>')
def getResource(resource_name):
    return send_from_directory('static',resource_name)

@app.route('/addToBasket/<category>/<catalogId>',methods=['POST'])
def addItem(category,catalogId):
    if request.method == 'POST': #add item to basket
        try:
            usr = UsersDAO[session['username']]
        except:
            render_template('error.html')
        print usr.getName()
        ItemHelpers().addToBasket(mysql,UsersDAO[session['username']].getUserBasketId(),catalogId)
        basketList = showBasket(UsersDAO[session['username']])
        print "basket : ",basketList

    return render_template('logged_in.html',itemPics=category,items=ItemsDAO,basket=basketList,admin=checkAdmin())

@app.route('/removeFromBasket/<category>/<catalogId>',methods=['POST'])
def removeItem(category,catalogId):
    if request.method == 'POST': #add item to basket
        usr = UsersDAO[session['username']]
        print usr.getName()
        ItemHelpers().removeFromBasket(mysql,UsersDAO[session['username']].getUserBasketId(),catalogId)
        basketList = showBasket(UsersDAO[session['username']])
        print "basket : ",basketList

    return render_template('logged_in.html',itemPics=category,items=ItemsDAO,basket=basketList,admin=checkAdmin())

@app.route('/checkOut',methods=['GET'])
def showCheckOut():
    basketList = showBasket(UsersDAO[session['username']])
    print "basket : ",basketList,"Items : ",ItemsDAO
    return render_template('check_out.html',items=ItemsDAO,basket=basketList)

@app.route('/shipping',methods=['GET'])
def showShipping():
    basketList = showBasket(UsersDAO[session['username']])
    url = generateURL(basketList)
    #print("payments : " ,getPayments())
    return render_template('shipping.html',payment=url,items=ItemsDAO,basket=basketList)

def showBasket(userName):
    basket = UserHelpers().listBasket(mysql,userName)
    return basket

def auth(userName = None, password = None):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from Users where UserEmail='" + userName + "' and UserPassw='" + password + "'")
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        return True

@app.route('/settings',methods=['GET'])
def renderSettings(method=None):
    if request.method == 'GET':
        if checkAdmin() == True :
            return render_template('settings.html')
        else:
            return render_template('logged_in.html',admin=checkAdmin())

@app.route('/settings/<method>',methods=['POST'])
def editCatalog(method=None):
    if checkAdmin() == True :
        if method == "upload":
            file = request.files['file']
            print(str(request.form['desc']),request.form['price'],request.form['category'])
            uploadPicture(request.form['category'],file)
            ItemHelpers().addToDB(mysql,request.form['desc'],str(file.filename).split("/").pop(-1),request.form['price'],request.form['category'])
            return render_template('settings.html')
        elif method == "delete":
            ItemHelpers().remoteFromDB(mysql,request.form['desc'],request.form['category'])
            return render_template('settings.html')
    else:
        return render_template('logged_in.html',admin=checkAdmin())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def uploadPicture(picDir,file):
    currentPath = path.dirname(path.realpath(__file__))
    picPath = currentPath + "/static/pictures/" + picDir
    if not path.exists(picPath):
        makedirs(picPath)
    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("picPath : " + picPath)
            file.save(path.join(picPath, filename))
    except:
        print(file.filename)
        print("no such file")

def createPicDir(picDir):
    currentPath = path.dirname(path.realpath(__file__))
    picPath = currentPath + "/static/pictures/" + picDir
    if not path.exists(picPath):
        makedirs(picPath)

def checkAdmin():
    if (session['username'] in AdminUsers):
        return True
    else:
        return False

def createItemsDAO():
    itemsList = ItemHelpers().getAllItems(mysql)
    for item in itemsList:
        itemObj = Item(*item)
        ItemsDAO[itemObj.getItemId()] = itemObj #items dictionary {ItemId:ItemObj}

def createUserDAO(username):
    userInfo = UserHelpers().getUserInfo(mysql,username)
    userObj = User(*userInfo[0])
    basketId,catalogeId = UserHelpers().getBasketId(userObj.getId(),mysql)[0]
    userObj.setUserBasketId(basketId)
    UsersDAO[userObj.getEmail()] = userObj #user dictionary {userEmail:UserObj}



if __name__ == '__main__':
    app.run(debug=True)

