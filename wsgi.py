from app import create_app
from app.apis import apis

app = create_app()

app.register_blueprint(apis, url_prefix='/apis')