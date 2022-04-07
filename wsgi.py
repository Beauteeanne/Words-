# import app from main.py
from . import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    # or
    # app.run()
    # or
    # app.run('0.0.0.0:8080')