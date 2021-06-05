from flask import Flask
from main import main_process

app = Flask(__name__)

@app.route('/startPCleaner/', methods=['GET'])
def index():
    main_process()
    return "Starting"


# @app.route('/duplicatePhotos/', methods=['GET'])
# def index():
#     return "Hello"


if __name__ == '__main__':
    app.run(debug=True)
