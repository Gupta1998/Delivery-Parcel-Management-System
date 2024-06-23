class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@localhost/parcel_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
    SESSION_TYPE = 'filesystem'