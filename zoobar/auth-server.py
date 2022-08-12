#!/usr/bin/python

import rpclib
import sys
import auth
from debug import *
from zoodb import *
import hashlib
import pbkdf2
import os
import random
import bank_client

class AuthRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_login(self, username, password):
        db = cred_setup()
        person = db.query(Cred).get(username)
        if not person:
            return None
        if person.password == pbkdf2.PBKDF2(password, person.salt.decode('base-64')).hexread(32):
            return newtoken(db, person)
        else:
            return None
    
    def rpc_register(self, username, password):
        cred_db = cred_setup()
        person = cred_db.query(Cred).get(username)
        if person:
            return None
        newperson = Cred()
        newperson.username = username
        salt = os.urandom(5)
        password = pbkdf2.PBKDF2(password, salt).hexread(32)
        newperson.salt = salt.encode('base-64')
        newperson.password = password
        cred_db.add(newperson)
        cred_db.commit()
        bank_client.new_bank(username)
        return newtoken(cred_db, newperson)

    def rpc_check_token(self, username, token):
        db = cred_setup()
        person = db.query(Cred).get(username)
        if person and person.token == token:
            return True
        else:
            return False
        

def newtoken(db, person):
    hashinput = "%s%.10f" % (person.password, random.random())
    person.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return person.token

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)
