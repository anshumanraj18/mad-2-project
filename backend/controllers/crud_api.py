from flask_restful import Resource
from flask import request , jsonify, make_response
from flask_security import utils, auth_token_required , roles_required

from controllers.user_datastore import user_datastore
from controllers.database import db
from controllers.models import *

#CRUD APIs for categories

class DepartmentCrudAPI(Resource):
    def get(self, department_id=None):
        if department_id:
            department = Department.query.get(department_id)
            if not department:
                result = {"message": "Department not found"}
                return make_response(jsonify(result), 404)
            
            response = {
                "id": department.id,
                "name": department.name,
                "description": department.description
            }
            return make_response(jsonify(response), 200)
        
        else:
            departments = Department.query.all()
            response = []
            for department in departments:
                response.append({
                    "id": department.id,
                    "name": department.name,
                    "description": department.description
                })
            return make_response(jsonify(response), 200)
        
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()

        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)

        name = data.get("name", None)
        description = data.get("description", None)

        if Department.query.filter_by(name=name).first():
            result = {"message": "Department with this name already exists"}
            return make_response(jsonify(result), 400)
        
        if not name:
            result = {"message": "Department name is required"}
            return make_response(jsonify(result), 400)
        
        new_department = Department(name=name, description=description)
        db.session.add(new_department)
        db.session.commit()

        response = {
            'message': 'New Department created successfully',
            'data': {
                "id": new_department.id,
                "name": new_department.name,
                "description": new_department.description
            }
        }
        return make_response(jsonify(response), 201)
    
    @auth_token_required
    @roles_required('admin')
    def put(self, department_id):
        
        department = Department.query.get(department_id)
        if not department:
            result = {"message": "Department not found"}
            return make_response(jsonify(result), 404)
        
        data = request.get_json()
        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)
        
        name = data.get("name")
        description = data.get("description")

        if name:
            existing_department = Department.query.filter_by(name=name).first()
            if existing_department and existing_department.id != department_id:
                result = {"message": "Department with this name already exists"}
                return make_response(jsonify(result), 400)
            
            department.name = name

        if description:
            department.description = description     

        db.session.commit()
        response = {
            "id": department.id,
            "name": department.name,
            "description": department.description
        }
        return make_response(jsonify(response), 200)
    
    @auth_token_required
    @roles_required('admin')
    def delete(self, department_id):
        department = Department.query.get(department_id)
        if not department:
            result = {"message": "Department not found"}
            return make_response(jsonify(result), 404)
        
        db.session.delete(department)
        db.session.commit()

        result = {"message": "Department deleted successfully"}
        return make_response(jsonify(result), 200)

class DoctorCrudAPI(Resource):
    def get(self, doctor_id=None):
            if doctor_id:
                doctor = Doctor.query.get(doctor_id)
                if not doctor:
                    result = {"message": "Doctor not found"}
                    return make_response(jsonify(result), 404)
                
                response = {
                    "id": doctor.id,
                    "user_id": doctor.user_id,
                    "department_id": doctor.department_id,
                    "specialization": doctor.specialization,
                    "availability": doctor.availability
                }
                return make_response(jsonify(response), 200)
            
            else:
                doctors = Doctor.query.all()
                response = []
                for doctor in doctors:
                    response.append({
                        "id": doctor.id,
                        "user_id": doctor.user_id,
                        "department_id": doctor.department_id,
                        "specialization": doctor.specialization,
                        "availability": doctor.availability
                    })
                return make_response(jsonify(response), 200)
        
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
            
        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)
            
        user_id = data.get("user_id")
        department_id = data.get("department_id")
        specialization = data.get("specialization")
        availability = data.get("availability")
            
        if not all([user_id, department_id, specialization]):
            result = {"message": "user_id, department_id, and specialization are required"}
            return make_response(jsonify(result), 400)
            
        new_doctor = Doctor(user_id=user_id, department_id=department_id, specialization=specialization, availability=availability)
        db.session.add(new_doctor)
        db.session.commit()
            
        response = {
            'message': 'New Doctor created successfully',
            'data': {
                "id": new_doctor.id,
                "user_id": new_doctor.user_id,
                "department_id": new_doctor.department_id,
                "specialization": new_doctor.specialization,
                "availability": new_doctor.availability
            }
        }
        return make_response(jsonify(response), 201)
        
    @auth_token_required
    @roles_required('admin')
    def put(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            result = {"message": "Doctor not found"}
            return make_response(jsonify(result), 404)
            
        data = request.get_json()
        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)
            
        if "specialization" in data:
            doctor.specialization = data["specialization"]
        if "availability" in data:
            doctor.availability = data["availability"]
        if "department_id" in data:
            doctor.department_id = data["department_id"]
            
        db.session.commit()
        response = {
            "id": doctor.id,
            "user_id": doctor.user_id,
            "department_id": doctor.department_id,
            "specialization": doctor.specialization,
            "availability": doctor.availability
        }
        return make_response(jsonify(response), 200)
        
    @auth_token_required
    @roles_required('admin')
    def delete(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            result = {"message": "Doctor not found"}
            return make_response(jsonify(result), 404)
            
        db.session.delete(doctor)
        db.session.commit()
            
        result = {"message": "Doctor deleted successfully"}
        return make_response(jsonify(result), 200)
    
    
class PatientCrudAPI(Resource):
    def get(self, patient_id=None):
        if patient_id:
            patient = Patient.query.get(patient_id)
            if not patient:
                result = {"message": "Patient not found"}
                return make_response(jsonify(result), 404)
            
            response = {
                "id": patient.id,
                "user_id": patient.user_id,
                "age": patient.age,
                "phone": patient.phone
            }
            return make_response(jsonify(response), 200)
        
        else:
            patients = Patient.query.all()
            response = []
            for patient in patients:
                response.append({
                    "id": patient.id,
                    "user_id": patient.user_id,
                    "age": patient.age,
                    "phone": patient.phone
                })
            return make_response(jsonify(response), 200)
        
    @auth_token_required
    def post(self):
        data = request.get_json()
        
        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)
        
        user_id = data.get("user_id")
        age = data.get("age")
        phone = data.get("phone")
        
        if not user_id:
            result = {"message": "user_id is required"}
            return make_response(jsonify(result), 400)
        
        new_patient = Patient(user_id=user_id, age=age, phone=phone)
        db.session.add(new_patient)
        db.session.commit()
        
        response = {
            'message': 'New Patient created successfully',
            'data': {
                "id": new_patient.id,
                "user_id": new_patient.user_id,
                "age": new_patient.age,
                "phone": new_patient.phone
            }
        }
        return make_response(jsonify(response), 201)
        
    @auth_token_required
    def put(self, patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            result = {"message": "Patient not found"}
            return make_response(jsonify(result), 404)
        
        data = request.get_json()
        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)
        
        if "age" in data:
            patient.age = data["age"]
        if "phone" in data:
            patient.phone = data["phone"]
        
        db.session.commit()
        response = {
            "id": patient.id,
            "user_id": patient.user_id,
            "age": patient.age,
            "phone": patient.phone
        }
        return make_response(jsonify(response), 200)
        
    @auth_token_required
    def delete(self, patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            result = {"message": "Patient not found"}
            return make_response(jsonify(result), 404)
            
        db.session.delete(patient)
        db.session.commit()
            
        result = {"message": "Patient deleted successfully"}
        return make_response(jsonify(result), 200)   
    

class AppointmentCrudAPI(Resource):
    def get(self, appointment_id=None):
        if appointment_id:
            appointment = Appointment.query.get(appointment_id)
            if not appointment:
                result = {"message": "Appointment not found"}
                return make_response(jsonify(result), 404)
            
            response = {
                "id": appointment.id,
                "doctor_id": appointment.doctor_id,
                "patient_id": appointment.patient_id,
                "appointment_time": appointment.appointment_time.isoformat()
            }
            return make_response(jsonify(response), 200)
        
        else:
            appointments = Appointment.query.all()
            response = []
            for appointment in appointments:
                response.append({
                    "id": appointment.id,
                    "doctor_id": appointment.doctor_id,
                    "patient_id": appointment.patient_id,
                    "appointment_time": appointment.appointment_time.isoformat()
                })
            return make_response(jsonify(response), 200)
    
    def post(self):
        data = request.get_json()
        
        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)
        
        doctor_id = data.get("doctor_id")
        patient_id = data.get("patient_id")
        appointment_time = data.get("appointment_time")
        
        if not all([doctor_id, patient_id, appointment_time]):
            result = {"message": "doctor_id, patient_id, and appointment_time are required"}
            return make_response(jsonify(result), 400)
        
        new_appointment = Appointment(doctor_id=doctor_id, patient_id=patient_id, appointment_time=appointment_time)
        db.session.add(new_appointment)
        db.session.commit()
        
        response = {
            'message': 'New Appointment created successfully',
            'data': {
                "id": new_appointment.id,
                "doctor_id": new_appointment.doctor_id,
                "patient_id": new_appointment.patient_id,
                "appointment_time": new_appointment.appointment_time.isoformat()
            }
        }
        return make_response(jsonify(response), 201)
    
    def put(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            result = {"message": "Appointment not found"}
            return make_response(jsonify(result), 404)
        
        data = request.get_json()
        if not data:
            result = {"message": "No input data provided"}
            return make_response(jsonify(result), 400)
        
        if "doctor_id" in data:
            appointment.doctor_id = data["doctor_id"]
        if "patient_id" in data:
            appointment.patient_id = data["patient_id"]
        if "appointment_time" in data:
            appointment.appointment_time = data["appointment_time"]
        
        db.session.commit()
        response = {
            "id": appointment.id,
            "doctor_id": appointment.doctor_id,
            "patient_id": appointment.patient_id,
            "appointment_time": appointment.appointment_time.isoformat()
        }
        return make_response(jsonify(response), 200)