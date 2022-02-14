class Config:
    dialect = 'postgresql'
    username = 'oypoardysbypop'
    password = '8bf53d8f8de04adf1175ba1c4504c1d36eb483728ed320e5c0b27dff5ac7ba6a'
    host = 'ec2-54-78-36-245.eu-west-1.compute.amazonaws.com'
    db_name = 'dftdt7n2jm2hre'

    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zxc-shadowfiend'
