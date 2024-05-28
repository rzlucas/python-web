from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap = Bootstrap()
    

    # Configuracion de la aplicacion (opcional)
    # Rutas
from .views import page

def create_app(config):
    app.config.from_object(config)

    Bootstrap.init_app(app)

    app.register_blueprint(page)

 
    
    return app