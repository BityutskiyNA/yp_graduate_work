from src.app import create_app
from src.settings import app_settings

app = create_app()

if __name__ == "__main__":
    app.run(debug=app_settings.debug, host="0.0.0.0")
