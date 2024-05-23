from flask import Flask
app = Flask(__name__)
    

    # Configuracion de la aplicacion (opcional)
    # Rutas
from .views import page

def create_app(config):
    app.config.from_object(config)

    app.register_blueprint(page)
    
    return app