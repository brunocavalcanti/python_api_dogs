from flask import request, Blueprint
from app.service.dog import DogService
dog_blp = Blueprint('dogs', __name__, url_prefix='/dogs')
dog_service = DogService()


@dog_blp.route('/register', methods=['POST'])
def save():
    return dog_service.save(request)


@dog_blp.route('/filter', methods=["GET"])
def get_by_name():
    return dog_service.get_by_name(request)


@dog_blp.route('/update', methods=["PUT"])
def update_by_name():
    return dog_service.update_by_name(request)


@dog_blp.route('/list', methods=["GET"])
def get_all():
    return dog_service.get_all()

@dog_blp.route('/report', methods=['POST'])
def generate_report():
    return dog_service.generate_report(request)

def configure():
    return dog_blp
