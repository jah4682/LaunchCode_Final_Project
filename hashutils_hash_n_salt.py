import hashlib
import random
import string

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

def make_pw_hash(password,salt=None):
    # make hash using hashlib sha256 function
    # hash is stored in database instead of password
    # str.encode returns bytes of password. This is necessary to avoid error. 
    # hexdigst returns a string instead of object.
    # salting: use salt function. concatinate password and salt. return string of hash and salt.
    # let user provide salt
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest() 
    return '{0},{1}'.format(hash,salt)

def check_pw_hash(password, hash):
    # get salt from database
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return True

    return False