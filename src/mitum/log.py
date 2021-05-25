# method constants
LOG_SUM256 = 'sum256'
LOG_SHA256 = 'sha256'
LOG_BCONCAT = 'bconcat'
LOG_TO_BYTES = 'to_bytes'

# log: call method
def clog(caller, func, msg):
    if func == LOG_SHA256:
        print('[CALL] ' + func + '(' + str(msg) + ')')
    elif func == LOG_BCONCAT:
        print('[CALL] ' + func + ': '+ str(msg))
    elif func == LOG_TO_BYTES:
        print('[CALL] ' + caller + '.' + func + '()')
    

# log: print result
def rlog(caller, func, msg, *result):
    clog(caller, func, msg)
    for r in result:
        print('-', r)
    print()