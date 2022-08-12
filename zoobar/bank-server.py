#!/usr/bin/python
#
# Insert bank server code here.
import rpclib
import sys
import auth
from debug import *
from zoodb import *
import hashlib
import pbkdf2
import os
import bank
import random

class BankRpcServer(rpclib.RpcServer):
    def rpc_new_bank(self, username):
        bank.new_bank(username);
    def rpc_transfer(self, sender, recipient, zoobars):
        bank.transfer(sender, recipient, zoobars)
    def rpc_balance(self, username):
        return bank.balance(username)
    def rpc_get_log(self, username):
        return bank.get_log(username)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)
