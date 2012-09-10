from mongokit import Document, Connection, CustomType
import hashlib
import uuid
import re
import datetime

def email_validator(value):
   email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)',re.IGNORECASE)
   return bool(email.match(value))

class Password(CustomType):
    mongo_type = basestring
    python_type = basestring # optional, just for more validation
    init_type = None # optional, fill the first empty value

    def to_bson(self, value):
        """convert type to a mongodb type"""
        return hashlib.new("md5",value).hexdigest()

    def to_python(self, value):
        """convert type to a python object"""
        return value

__all__ = ['UserBase', 'UserEMail', 'UserUsername']

class UserBase(object):
    """Base class for all users"""


    def check_password(self, pw):
        """check password"""
        hash = hashlib.new("md5",pw).hexdigest()
        return hash == self.password

    def create_pw(self):
        """create a password"""
        pw = unicode(uuid.uuid4())[:8]
        self.password = pw
        return pw

    def get_id(self):
        """return the userid we want to use in sessions etc."""
        return self._id

    @property
    def is_active(self):
        """overwrite this if you want a different use case"""
        return True

    def create_validation_code(self):
        """create a new validation code"""
        code = self.validationcode = unicode(uuid.uuid4())
        self.validationcode_sent = datetime.datetime.now()
        return code

    def get_token(self):
        """return a token to be used for remembering the user. Per default it's the hashed
        userid:password tuple. So if the password changes this token is not valid anymore
        and the user needs to login again
        """
        return hashlib.new("md5","%s:%s" %(self.get_id(), self.password)).hexdigest()

    

class UserEMail(Document, UserBase):
    """a user identified by email address and password"""

    name = "UserEMail" # should be the same name as the class
    use_dot_notation = True

    structure = {
        'fullname'                      : basestring,
        'email'                         : basestring,
        'password'                      : Password(),
        'date_creation'                 : datetime.datetime,
        'active'                        : bool,
        'activation_time'               : datetime.datetime,
        'last_login'                    : datetime.datetime,
        'last_ip'                       : basestring,
        'activation_code'               : basestring,
        'password_code'                 : basestring,
        'activation_code_expires'       : datetime.datetime,
        'password_code_expires'         : datetime.datetime,
        'fullname'                      : basestring,
    }
    
    validators = {
        'email': email_validator,
    }

    required_fields = ['email', 'password', 'date_creation']
    
    default_values = {
        'date_creation'                 : datetime.datetime.utcnow,
        "last_ip"                       : "",
        "last_login"                    : None,
        "activation_time"               : None,
        "activation_code_expires"       : None,
        "activation_code"               : None,
        "password_code"                 : None,
        "password_code_expires"         : None,
        "active"                        : False,
    }
    
    def get_id(self):
        """return the userid we want to use in sessions etc."""
        return self.email
    
    
class UserUsername(Document, UserBase):
    """a user identified by a username and password"""

    name = "UserUsername" # should be the same name as the class
    use_dot_notation = True

    structure = {
        'email'                         : basestring,
        'username'                      : basestring,
        'password'                      : Password(),
        'date_creation'                 : datetime.datetime,
        'active'                        : bool,
        'activation_time'               : datetime.datetime,
        'last_login'                    : datetime.datetime,
        'last_ip'                       : basestring,
        'activation_code'               : basestring,
        'password_code'                 : basestring,
        'activation_code_expires'       : datetime.datetime,
        'password_code_expires'         : datetime.datetime,
        'fullname'                      : basestring,
    }
    
    required_fields = ['email', 'username', 'password', 'date_creation']

    validators = {
        'email': email_validator,
    }
    
    default_values = {
        'date_creation'                 : datetime.datetime.utcnow,
        "last_ip"                       : "",
        "last_login"                    : None,
        "activation_time"               : None,
        "activation_code_expires"       : None,
        "activation_code"               : None,
        "password_code"                 : None,
        "password_code_expires"         : None,
        "active"                        : False,
    }

    def get_id(self):
        """return the userid we want to use in sessions etc."""
        return self.username

