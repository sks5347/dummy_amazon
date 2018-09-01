from flask import Flask, render_template, request, redirect, url_for, session
from models.user_model import user_signup, user_signin
from models.product_model import *

app = Flask(__name__)
app.secret_key = 'secret key'


@app.route("/")
def login():
    if 'user_name' in session.keys():
        return render_template('login.html', login='True')
    else:
        return render_template('login.html', login='False')


@app.route("/login", methods=['POST'])
def user_login():
    if request.form['loginbutton'] == 'login':
        signinuser_info = {}
        inputEmail = request.form['inputEmail']
        inputPassword = request.form['inputPassword']
        signinuser_info = {'user_email': inputEmail, 'user_password': inputPassword}
        userlogin = user_signin(signinuser_info)
        if userlogin:
            session['logedinuser'] = {'user_id': str(userlogin['_id']), 'accounttype': userlogin["accounttype"],
                                      'email': userlogin['email']}
            # session['logedinuser'] = json.dumps(userlogin)
            allproductslist = viewproduct()
            print(allproductslist)
            for list in allproductslist:
                print(list['_id'])
            return render_template("product.html", allproductslist=allproductslist)
        else:
            return render_template("signup.html")
    else:
        return render_template("signup.html")


@app.route("/signup", methods=['POST'])
def signup():
    user_info = {}
    user_info["firstname"] = request.form["firstname"]
    user_info["lastname"] = request.form["lastname"]
    user_info["email"] = request.form["email"]
    user_info["password"] = request.form["password"]
    user_info['accounttype'] = request.form['accounttype']
    user_result = user_signup(user_info)

    if user_result != "unsuccessful":
        print("saved success message")
        return render_template('login.html')
    else:
        print("not saved")


@app.route("/product", methods=['GET'])
def add_product():
    prds = view_product()
    addedproductinfo = {}
    addedproductinfo['productname'] = request.args['productname']
    addedproductinfo['productprice'] = request.args['productprice']
    addedproductinfo['productdesc'] = request.args['productdesc']
    addedproductinfo['brandname'] = request.args['brandname']
    if addedproductinfo:
        prdresult = addproduct(addedproductinfo)
        if prdresult == "successful":
            addedproductinfo['_id'] = str(addedproductinfo['_id'])
            allproductslist = view_product()
            return render_template('product.html', allproductslist=allproductslist)


def viewproduct():
    prodslist = view_product()
    return prodslist


def viewcart():
    userid = session['logedinuser'].get('user_id')
    cartproductslist = view_cart(userid)
    return cartproductslist


@app.route("/mycart", methods=['GET'])
def my_cart():
    cartproductslist=viewcart()
    print(cartproductslist)
    return render_template('cart.html', cartproductslist=cartproductslist)


@app.route("/cart_products", methods=['POST'])
def add_to_cart():
    prdid = request.form["btnaddtocart"]
    userid = session['logedinuser'].get('user_id')
    usercartproduct = addtocart(prdid, userid)
    if usercartproduct:
        allproductslist = viewproduct()
        return render_template('product.html', allproductslist=allproductslist)


if __name__ == "__main__":
    app.run(debug=True)
