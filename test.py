from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/employee'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypass123@localhost:3306/knowly'


db = SQLAlchemy(app)


class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())



class Test(Base):

    __tablename__ = 'ToDo'

    # User Name
    user    = db.Column(db.String(128),  nullable=False)
    hash_pwd    = db.Column(db.String(128),  nullable=True)




# db.create_all()
# p = Test()
# p.col1 = "abhishek1"
# p.col2 = "abc1"

# db.session.add(p)
# db.session.commit()

def hashit(password):
    hashed_pass = generate_password_hash(password)
    return hashed_pass

class userReg(Resource):

    # def get(self):
    #     all = Test.query.all()
    #     print(all)
    #     return {'hello': 'world'}

    def post(self):
        data = request.get_json()
        password = data['password']
        agent_id = data['agent_id']
        hash_pwd = hashit(password)
        user= Test()
        user.user = agent_id
        user.hash_pwd = hash_pwd
        db.session.add(user)
        db.session.commit()
        return {'status': 'account created', 'status_code': 200}


class userLogin(Resource):

    def post(self):
        data = request.get_json()
        password = data['password']
        agent_id = data['agent_id']
        hash_pwd = hashit(password)
        user= Test()
        user.user = agent_id
        user.hash_pwd = hash_pwd
        check=Test.query.filter_by(user=agent_id).first()
        print (check.user, check.hash_pwd)
        if(check.hash_pwd == user.hash_pwd):
            return {'status' : 'success','agent_id' : agent_id,'status_code' : 200 }
    
        return {'status' : 'failure','status_code' : 401 }

api.add_resource(userReg,'/app/agent')
# @app.route('/app/agent', methods=['POST'])
# def posting(agent_id, password):
#     hash_pwd = hashit(password)
#     user= Test(agent_id, hash_pwd)
#     db.session.add(user)
#     db.session.commit()
#     return {'status': 'account created', 'status_code': 200}
api.add_resource(userLogin,'/app/agent/auth')



if __name__=='__main__':
    app.run(debug=True)