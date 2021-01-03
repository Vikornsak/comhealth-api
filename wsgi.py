from app import create_app
from app.apis import apis
from waitress import serve

app = create_app()

app.register_blueprint(apis, url_prefix='/apis')

serve(app, host='0.0.0.0', port=8080, threads=1)