import os
from flask import Flask

#Application factory function
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) #creates the Flask instance
    app.config.from_object(__name__)
    app.config.from_pyfile('../cashback/config.py')
    
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'cashback.sqlite'),
    )
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import db
    db.init_app(app)
    
    from .views import auth_route
    app.register_blueprint(auth_route.bp)
    
    from .views import purchase_route
    app.register_blueprint(purchase_route.bp)
    
    return app