from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql
import traceback
 
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource):
    def db_init(self):
        db = pymysql.connect('localhost','root','123456','api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self,id):
        db, cursor = self.db_init()
        sql = """SELECT * FROM api.users WHERE id ={}""".format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()

        return jsonify({'data':user})

    def patch(self,id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note'],
        }
        query = []
        for key, value in user.items():
            if value != None:
                query.append(key + "=" + "'{}'".format(value))
        query = ", ".join(query)
        sql = """
            UPDATE `api`.`users` SET {} WHERE  `id`={}
        """.format(query,id)

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'Success'
        except:
            traceback.print_exc()
            response['msg'] = 'Failed'
        db.commit()
        db.close()
        return jsonify(response)        

    def delete(self,id):
        db, cursor = self.db_init()
        #sql = """DELETE FROM api.users WHERE id ={}""".format(id)
        sql = """
            UPDATE `api`.`users` SET deleted = 1 WHERE  `id`={}
        """.format(id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'Success'
        except:
            traceback.print_exc()
            response['msg'] = 'Failed'
        db.commit()
        db.close()
        return jsonify(response)

class Users(Resource):
    def db_init(self):
        db = pymysql.connect('localhost','root','123456','api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        sql = 'SELECT * FROM api.users WHERE deleted = "0"'
        if arg['gender'] != None:
            sql += 'AND gender = {}'.format(arg['gender'])
        print(sql)
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()

        return make_response(jsonify({'data':users}),400)

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note'],
        }
        sql = """
            INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`) 
            VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'],user['gender'],user['birth'],user['note'])
     
        response = {}
        status_code = 200
        try:
            status_code = 200
            cursor.execute(sql)
            response['msg'] = 'Success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
        db.commit()
        db.close()
        return make_response(jsonify(response), status_code)
