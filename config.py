from uuid import uuid4

class Config:
    DEBUG = True
    SECRET_KEY = uuid4().hex
    SESSION_PERMANENT = True
    SESSION_TYPE = 'filesystem'