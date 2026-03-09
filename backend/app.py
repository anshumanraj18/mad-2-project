from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

from controllers.database import db
from controllers.config import config
from controllers.user_datastore import user_datastore

from flask_restful import Api, Resource
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    security = Security(app, user_datastore, register_blueprint=False)

    api = Api(app , prefix="/api")

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_role = user_datastore.find_or_create_role(name='user', description='Regular User')

        if not user_datastore.find_user(email="admin@gmail.com"):
            user_datastore.create_user(
                email="admin@gmail.com",
                password="admin123",
                roles=[admin_role]
            )
        
        db.session.commit()
    
    return app, api

app,api = create_app()
CORS(app , origins="*")

@app.route('/')
def index():
    return {"message": "Welcome to the Hospital Management System API 1"}, 200

#class IndexAPI(Resource):
#    def get(self):
#       return {"message": "Welcome to the Hospital Management System API 2"}, 200

#api.add_resource(IndexAPI, '/api')

from controllers.authentication_apis import LoginAPI, LogoutAPI, RegisterAPI

api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')

from controllers.crud_api import DepartmentCrudAPI , DoctorCrudAPI , PatientCrudAPI , AppointmentCrudAPI
api.add_resource(DepartmentCrudAPI, '/departments', '/departments/<int:department_id>')
api.add_resource(DoctorCrudAPI, '/doctors', '/doctors/<int:doctor_id>')
api.add_resource(PatientCrudAPI, '/patients', '/patients/<int:patient_id>')
api.add_resource(AppointmentCrudAPI, '/appointments', '/appointments/<int:appointment_id>')

if __name__ == "__main__":
    app.run(debug=True)