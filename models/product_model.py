from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()
db = client['dummy-amazon']


def addproduct(productinfo):
    prdrecord = db['product'].insert_one(productinfo)
    if prdrecord.acknowledged == True:
        message = 'successful'
    else:
        message = 'unsuccessful'
    return message


def view_product():
    prodslist = list(db['product'].find())
    return prodslist


def addtocart(prd_id,user_id):
    prduserinfo={"prd_id":prd_id,"user_id":user_id}
    prduser = db['prduser'].insert_one(prduserinfo)
    return prduser

def view_cart(userid):
    usercardprdlist=[]
    prdidlist=list(db['prduser'].find({"user_id":userid}))
    for prdid in prdidlist:
        cartprdlist=list(db['product'].find({"_id": ObjectId(prdid['prd_id'])}))
        usercardprdlist.append(cartprdlist)
    return usercardprdlist