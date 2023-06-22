import json


def getProjects():
    # Open the JSON file
    file = open('assets/shubhamistic/json/projects.json', 'r')

    # Load & return the JSON data
    return json.load(file)
