from flask import Flask

from authentication.authentication import authentication_blueprint
from database import mongo, bcrypt, app_session
from general.general import general_blueprint
from portfoliodetails.portfolio import portfolio_blueprint

app = Flask(__name__)

# Dev configuration
# app.config.from_object("config.DevelopmentConfig")

# Prod configuration
app.config.from_object("config.ProductionConfig")

# initializing mongo, bcrypt and session
mongo.init_app(app)
bcrypt.init_app(app)
app_session.init_app(app)

# registering blueprints
app.register_blueprint(authentication_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(portfolio_blueprint)

if __name__ == "__main__":
    app.run()
