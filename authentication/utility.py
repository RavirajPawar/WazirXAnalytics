def register_user(mongo, email, password):
    """
    creates new user in database.
    Args:
        mongo: database connection object
        email: email string
        password: byte hashed password
    """
    try:
        mongo.db.user_auth.insert_one({"email": email, "password": password})
        return "User has been created."
    except:
        return "something went wrong."


def fetch_user(mongo, email):
    """
       checks email address present or not in collection.
       Args:
           mongo: database connection object
           email: email string
       Returns:
           user details dict from collection
    """
    try:
        return mongo.db.user_auth.find_one({"email": email})
    except:
        return "something went wrong."
