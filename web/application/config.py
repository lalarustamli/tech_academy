import os

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'secret_key'
    MONGODB_SETTINGS = {'db':'UTA_enrollment'}