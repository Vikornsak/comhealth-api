from app import app
from waitress import serve

if app.debug:
    app.run(debug=True, port=8080)
else:
    serve(app, host='0.0.0.0', port=8080, threads=1)

