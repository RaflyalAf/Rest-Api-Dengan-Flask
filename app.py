#import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)



api = Api(app)
CORS(app)

db = SQLAlchemy(app)

basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

class ModelDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.olumn(db.TEXT)

    def seve (self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
        
db.create_all()

identitas = {}

class ContohReource(Resource):
    def get(self):
        
        query = ModelDatabase.query.all()
        output = [{
            "nama":data.nama, 
            "umur":data.umur, 
            "alamat":data.alama}
                for data in query]

        response = {
                "code" : 200,
                "msg"  : "query data berhasil" ,
                "data" : output
            }

        return output, 200
    
    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]

        model = ModelDatabase(nama=dataNama, umur=dataUmur, alamat=dataAlamat)
        model.seve()

        response = {"msg" : "Data berhasil di masukan",
                    "code" : 200
        
        }
        return response, 200 
    
class Naruto(Resource):
    def put(self, id):
        query = ModelDatabase,query.get(id)
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]

        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat

        response = {
            "msg" : "edit data berhasil",
            "cede" : 200
        }
        return response
    
    def delete(self, id):
        queryData = ModelDatabase.query.get(id)
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg" : "delete data berhasil",
            "code" : 200
        }
        return response

api.add_resource(ContohReource, "/api", methods=["GET", "POST"])
api.add_resource(Naruto, "/api/<id>", methods=["PUT"])


if __name__ == "__main__":
    app.run(debug=True, port=5005)
