from mongoengine import *
from os import getenv
from loguru import logger

class UserData(Document):
    fname = StringField(required=True, min_length=1, max_length=200)
    lname = StringField(required=True, min_length=1, max_length=200)
    email = StringField(required=True, min_length=1, max_length=200)
    
    meta = {
        'allow_inheritance': True,
        'collection': getenv('MONGODB_COLLECTION', 'user')
    }

class User:
    def __init__(self):
        self.db_alias = 'default'
        
    def __enter__(self):
        # Establish MongoDB connection
        connect(alias=self.db_alias, host=getenv('MONGODB_CONNECT_STRING'))
        return self
        
    def __get_user(self, email: str) -> dict:
        response_json = {'status': 'error', 'description': '', 'user': {}}
        
        try:
            row = UserData.objects(email=email).first()
            if row:
                # Convert MongoEngine document to dict
                user = row.to_mongo().to_dict()
                response_json['user'] = user
                response_json['status'] = 'success'
                    
        except Exception as e:
            response_json['description'] = str(e)
            
        return response_json
    
    def _save_user(self, user: dict) -> dict:
        response_json = {'status': 'error', 'description': ''}
        
        try:
            fname, lname, email = user.get('fname', ''), user.get('lname', ''), user.get('email', '')
            values = (fname, lname, email)
            
            # logger.debug(values)
            
            if not all(values):
                response_json['description'] = 'Invalid form!'
                return response_json
            
            if self.__get_user(email).get('status') == 'success':
                response_json['description'] = 'User already exists!'
                return response_json
            
            # Save new user to the database
            new_user = UserData(fname=fname, lname=lname, email=email)
            new_user.save()
            
            response_json['description'] = 'Success! User saved!'
            response_json['status'] = 'success'
                    
        except Exception as e:
            response_json['description'] = str(e)
            
        return response_json
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Disconnect from MongoDB
        disconnect(alias=self.db_alias)
