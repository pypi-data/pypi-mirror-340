# click_tracker_library/__init__.py

from flask import Flask
from .utils import init_csv, log_click
from .config import DefaultConfig

def create_app(config=None):
    """
    Factory function to create and configure the Flask app.
    :param config: Optional configuration object or dictionary.
    :return: Flask app instance.
    """
    app = Flask(__name__)

    # Load default configuration
    app.config.from_object(DefaultConfig)

    # Override with custom configuration if provided
    if config:
        app.config.update(config)

    # Initialize CSV file
    init_csv(app.config['CSV_FILE'])

    # Import and register routes
    from .app import track_click, view_clicks
    app.add_url_rule('/', 'track_click', track_click)
    app.add_url_rule('/admin/ips', 'view_clicks', view_clicks)

    return app