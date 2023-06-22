from flask import Blueprint, request, abort, send_file
from os import path
from routes.shubhamistic.getProjects import projects
from routes.shubhamistic.createDataFiles import createJsonFiles


# Create a blueprint for /shubhamistic/ route
shubhamistic_routes = Blueprint('shubhamistic', __name__)

# create json data files
createJsonFiles()


# Route for /shubhamistic/
@shubhamistic_routes.route('/')
def admin():
    return {
        "message": "Welcome to shubhamistic!",
        "routes": [
            "/projects GET",
            "/experience GET",
            "/skills GET",
            "/achievements GET",
            "/contact POST"
        ]
    }


@shubhamistic_routes.route('/projects', methods=['GET'])
def getProjects():
    return projects


@shubhamistic_routes.route('/experience', methods=['GET'])
def getExperience():
    return {
        "message": "shubhamistic/experience/"
    }


@shubhamistic_routes.route('/skills', methods=['GET'])
def getSkills():
    return {
        "message": "shubhamistic/skills/"
    }


@shubhamistic_routes.route('/achievements', methods=['GET'])
def getAchievements():
    return {
        "message": "shubhamistic/achievements/"
    }


@shubhamistic_routes.route('/contact', methods=['POST'])
def contact():
    data = dict(request.args)

    return {
        "message": "Request Successful!",
        "data": data
    }


@shubhamistic_routes.route('/assets/<file>')
def returnQRFile(file):
    file_path = f"./assets/shubhamistic/images/{file}"
    if path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    else:
        abort(404, 'Error: Requested file not found!')
