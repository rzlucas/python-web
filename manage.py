from app import create_app
import click
from config import config

config_class = config['development']
app = create_app(config_class)

@click.group()
def cli():
    """Comandos de administración de la aplicación."""
    pass

@cli.command()
def runserver():
    """Inicia el servidor de desarrollo."""
    app.run(debug=True)

# Puedes agregar más comandos aquí, por ejemplo:
# @cli.command()
# def initdb():
#     """python manage.py runserver | Para inicializa la base de datos."""
#     # ... (tu código para inicializar la base de datos)

if __name__ == '__main__':
    cli()

@cli.command()
def stop():
    """CTRL+C Detiene el servidor."""
    # Aquí debes implementar la lógica para detener el servidor de forma segura.
    # Puedes usar una variable global para indicar que el servidor debe detenerse,
    # o enviar una señal de interrupción al proceso.
