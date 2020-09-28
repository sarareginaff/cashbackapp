import os
from flask import Flask

def create_app():
    """
        Create cashback flask app

        :Returns: 
            - app (flask instance): cashback flask app

        :author: sarareginaff       
        :creation: Sep/2020
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(__name__)
    app.config.from_pyfile('../cashback/config.py')
    
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'cashback.sqlite'),
    )
    
    # create instance folder exists if it does not exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init db
    from .db import db
    db.init_app(app)
    
    # include controllers
    from .controllers import auth_route
    app.register_blueprint(auth_route.bp)
    
    from .controllers import purchase_route
    app.register_blueprint(purchase_route.bp)
    
    return app