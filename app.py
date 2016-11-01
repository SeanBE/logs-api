from app.config import DevConfig
from app import create_app, config

if __name__ == '__main__':
    app = create_app(config.DevConfig)
    app.run(host='0.0.0.0')
