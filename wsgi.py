from app import app
from waitress import serve

if app.debug:
    app.run(debug=True, port=5001)
else:
    serve(app, host='0.0.0.0', port=5001, threads=1)

