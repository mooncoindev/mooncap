# mooncap
#
# coin daemon must have sync'd with -txindex
#
# install deps using pip:
# python-bitcoinrpc

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time
import os,sys

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# user-config section
rpchost = '127.0.0.1'
rpcuser = 'rpcuser'
rpcpass = 'rpcpassword'
print ''
curblock=0
coinmarketcap=0
rpcpipe = AuthServiceProxy('http://' + rpcuser + ':' + rpcpass + '@' + rpchost + ':44663')
while(curblock!=rpcpipe.getblockcount()):

   #decode them blocks
   curblock=curblock+1
   rawblockhash=rpcpipe.getblockhash(curblock)
   rawblockdata=rpcpipe.getblock(rawblockhash)
   print 'checking block %08d' % (curblock),

   #get coinbase transaction
   blockdata=str(rawblockdata)
   coinbase_txid=find_between(blockdata, 'u\'tx\': [u\'', '\'],')[:64]
   print ' ['+str(coinbase_txid)+']',

   #isolate the output
   rawtxdata=rpcpipe.getrawtransaction(str(coinbase_txid))
   txdata=rpcpipe.decoderawtransaction(str(rawtxdata))
   cbout=find_between(str(txdata), 'Decimal(\'', '\')')
   true_cbout=float(str(cbout))
   coinmarketcap=coinmarketcap+true_cbout
   print '  thistx: %0.8f     totalgen: %0.8f' % (true_cbout, coinmarketcap)
