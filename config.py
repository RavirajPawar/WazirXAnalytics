class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = "mongodb+srv://raviraj:randomPassword@cluster0.btv5a.mongodb.net/wazirx_analytics?retryWrites=true&w=majority"
    JWT_SECRET_KEY = "Let's_Keep_It_Secret"
    SECRET_KEY = "Flask_Secret_Key_1458752214542"
    secret_key = "Raviraj_Developed_This_For_Cryto_4537674234675354"
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = "mongodb+srv://raviraj:randomPassword@cluster0.btv5a.mongodb.net/wazirx_analytics?retryWrites=true&w=majority"
    JWT_SECRET_KEY = "Let's_Keep_It_Secret"
    SECRET_KEY = "Flask_Secret_Key"
    secret_key = "Raviraj_Developed_This_For_Cryto"
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False


class TestingConfig(Config):
    TESTING = True