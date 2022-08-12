
from debug import *
from zoodb import *
import rpclib

def new_bank(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        c.call('new_bank', username=username)
def transfer(sender, recipient, zoobars):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        c.call('transfer', sender=sender, recipient=recipient, zoobars=zoobars)
def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance', username=username)
        return ret
def get_log(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('get_log', username=username)
        return ret

