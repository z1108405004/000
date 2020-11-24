from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import Users,User
#import jwt
import time
app = Flask(__name__)
api = Api(app)

api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')
@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ == "NotFound":
        status_code = 404
    elif type(error).__name__ == "TypeError":
        status_code = 500

    return jsonify({'msg':type(error).__name__}), status_code

# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     user_id = request.get_json()['user_id']
#     vaild_token = jwt.encode({"user_id":user_id,'timestamp':int(time.time())},
#     'password', algorithm='HS256').decode('utf-8')
#     print(vaild_token)
#     if token == vaild_token:
#         pass
#     else:
#         return {
#             'msg':'invaild token'
#         }

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True, host='0.0.0.0', port=5004)
