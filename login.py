import pymongo
import random
from pymongo import MongoClient
import time
import config
cluster = MongoClient(config.mongo_url)
db = cluster["logins"]
collection = db["logins"]
collection1 = db["keys"]

def main():
    print("[1] Login: ")
    print("[2] Register: ")
    print("[3] Admin: ")
    print("[4] Generate Key: ")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        log.login()
    elif choice == 2:
        reg.register()
    elif choice == 4:
        keys.gen()
    else:
        print("Invalid Choice")
        main()

class log():
    def db(username, password):
        if collection.find_one({"username": username, "password": password}) is not None:
            log.logedin(username)
        else:
            return print("Login failed")
            main()
    def logedin(username):
        print("Welcome "+ username)
        if collection.find_one({"username": username, "sub": True}):
            print("You have an active subscription")
        else:
            print("You do not have a subscription")
        print("[1] Redeem Key: ")
        print("[2] logout: ")
        choicelogin = int(input("Enter your choice: "))
        if choicelogin == 1:
            key = input("Enter your key: ")
            keys.redeem(username, key)
        elif choicelogin == 2:
            print("Logged Out")
            main()

    def login():
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        log.db(username, password)

class reg():
    def db(username, password):
        post = {"username": username, "password": password, "sub": False, "creation": time.strftime("%d/%m/%Y")}
        if collection.insert_one(post):
            return print("Account Created, Welcome "+ username)
            
            main()
        else:
            return print("Account Creation Failed")
            
            main()

    def register():
        username = input("Make A Username: \n")
        if collection.find_one({"username": username}):
            print("Username Taken")
        else:
            password = input("Make A Password: \n")
            password2 = input("Confirm Password: \n")
            if password == password2:
                reg.db(username, password)
                main()
            else:
                print("Passwords do not match")
                main()


class keys():
    # def gen():
    #     #generate a sting of random characters
    #     chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456%()`$??! "
    #     key=""
    #     for x in range(0,15):
    #         charc = random.choice(chars)
    #         key  = key + charc
    #     print(key)
    #     post = {"key": key, "redeemed": False}
    #     if collection1.insert_one(post):
    #         print("Key Generated")
    #         main()
    #     else:
    #         print("Key Generation Failed")
    #         main()

    def redeem(username, key):
        #check if key is valid
        if collection1.find_one({"key": key}):
            if collection1.find_one({"key": key, "redeemed": True}):
                print("Key already redeemed")
                log.logedin()
            else:
                collection1.update_one({"key": key}, {"$set": {"redeemed": True}})
                collection.update_one({"username": username}, {"$set": {"sub": True}})
                print("Key Redeemed")
                log.logedin()




main()


