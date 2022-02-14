class Config:
    dialect = 'postgresql'
    username = 'mrulfwmtmwplos'
    password = 'a67e9ca8e6e41a6d81c1df0a49bd9472618d91f098251b780a12776e86e83511'
    host = 'ec2-52-211-158-144.eu-west-1.compute.amazonaws.com'
    db_name = 'dbgsg3c5be3uat'

    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zxc-shadowfiend'
