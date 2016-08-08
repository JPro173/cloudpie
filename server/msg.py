import json

def error(msg):
    return json.dumps({'status': 'error', 'message': msg})

def cast_error(n = -1, expected=-1):
    n = ' ({}\'th)'.format(str(n)) if n != -1 else ''
    err = 'Invalid argument type{}'.format(n)
    if expected != -1:
        err += ', expected {}'.format(expected.__name__)
    return error(err)

def args_count_error(got, expected=-1):
    if expected == -1:
        return error('Unexpectd arguments count, {} got'.format(got))
    return error('Expected {} arguments, {} got'.format(expected, got))

def need_login_error():
    return error('You need to log in')

def dont_exist_error(**kwargs):
    return error('{} {} does not exists!'.format(*kwargs.items()[0]))

def message(*msg, delim=' '):
    return json.dumps({'status': 'ok', 'message': delim.join([str(m) for m in msg])})

def ok():
    return json.dumps({'status': 'ok'})

def fail():
    return json.dumps({'status': 'fail'})

