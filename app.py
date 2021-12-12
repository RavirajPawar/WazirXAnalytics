from flask import Flask
from database import mongo, bcrypt
from general.general import general_blueprint
from portfoliodetails.portfolio import portfolio_blueprint
from authentication.authentication import authentication_blueprint


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wazirx_analytics"
mongo.init_app(app)
bcrypt.init_app(app)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(portfolio_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
