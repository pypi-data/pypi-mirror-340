import os
import click
from waitress import serve
from .config import DEBUG
from . import app

@click.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug/--no-debug', default=None, help='Enable debug mode')
def main(host, port, debug):
    """Firefly Database Viewer - A web interface for viewing Firefly databases"""
    if debug is None:
        debug = DEBUG
    
    if debug:
        click.echo(f"Starting Firefly Database Viewer in DEBUG mode on http://{host}:{port}")
        click.echo("Press CTRL+C to quit")
        app.run(host=host, port=port, debug=True)
    else:
        click.echo(f"Starting Firefly Database Viewer in PRODUCTION mode on http://{host}:{port}")
        click.echo("Using Waitress production server")
        click.echo("Press CTRL+C to quit")
        serve(app, host=host, port=port, threads=4)

if __name__ == '__main__':
    main()