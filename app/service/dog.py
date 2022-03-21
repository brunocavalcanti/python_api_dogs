import json
from mongoengine.errors import NotUniqueError
from app.database.dog_repository import DogRepository
from werkzeug.exceptions import BadRequest, NotFound
from flask import jsonify
from app.kafka.report.report_producer import ReportProducer
from reportlab.pdfgen import canvas


class DogSaveDto:
    def __init__(self, name=str, breed=str, features=list):
        self.name = name
        self.breed = breed
        self.features = features


class DogUpdateDto(DogSaveDto):
    pass


class DogService:
    def __init__(self):
        self.repository = DogRepository()
        self.report_producer = ReportProducer()

    def save(self, req):
        try:
            data = json.loads(req.data)
            dog = self.repository.save(DogSaveDto(name=data['name'],
                                                  breed=data['breed'],
                                                  features=data['features']))
            return jsonify(dog)
        except NotUniqueError:
            raise BadRequest(f"Already exists dog with name: {data['name']}")

    def get_dog_by_name_or_fail(self, name=str):
        dog = self.repository.get_by_name(name)
        if not dog:
            raise NotFound(f"Not found dog with name: {name}")
        return dog

    def get_by_name(self, req):
        name = req.args.get('name')
        dog = self.get_dog_by_name_or_fail(name)
        return jsonify(dog)

    def update_by_name(self, req):
        try:
            name = req.args.get('name')
            data = json.loads(req.data)
            dog = self.get_dog_by_name_or_fail(name)
            dog = self.repository.update_by_name(dog, DogSaveDto(name=data['name'],
                                                                 breed=data['breed'],
                                                                 features=data['features']))
            return jsonify(dog)
        except NotUniqueError:
            raise BadRequest(f"Already exists dog with name: {data['name']}")

    def get_all(self):
        dog_list = self.repository.get_all()
        return jsonify(dog_list)

    def generate_report(self, req):
        data = json.loads(req.data)
        self.report_producer.send(json.dumps(data))
        return jsonify({"message": "send report to generate"})

    def generate_report_pdf(self):
        dog_list = self.repository.get_all()
        pdf = canvas.Canvas('report.pdf')
        x = 720
        for dog in dog_list:
            x -= 20
            pdf.drawString(100, x, f"{dog.name} - {dog.breed}")
        pdf.setTitle('Relatório de Cachorros Cadastrados')
        pdf.drawString(100, 750, 'Relatório de Cachorros Cadastrados')
        pdf.save()
