from pymongo import MongoClient

client = MongoClient()
db = client['dummy-amazon']

def user_signin(signinuser_info):
    usersigninrecord = db['users'].find_one({'email': signinuser_info["user_email"],'password': signinuser_info["user_password"]})
    return usersigninrecord



def user_signup(user_info):
    # import pdb;pdb.set_trace()
    # fetch the user Info
    # db.user_info.find()
    # here wew have to save the user info
        acknowledgedresult = db['users'].insert_one(user_info)
        if acknowledgedresult.acknowledged == True:
            message = user_info['accounttype']
        else:
            message = "unsuccessful"
        return message


'''def addproduct(proddetails):
    prodadded = db = ['products'].insert_one(proddetails)
    if prodadded == True:
        return True'''
