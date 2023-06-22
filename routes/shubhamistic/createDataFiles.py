import os


def createJsonFiles():
    # create the json data files
    json_directory = "assets/shubhamistic/json"
    projects_file = os.path.join(json_directory, 'projects.json')
    experience_file = os.path.join(json_directory, 'experience.json')
    skills_file = os.path.join(json_directory, 'skills.json')
    achievements_file = os.path.join(json_directory, 'achievements.json')

    if not os.path.exists(projects_file):
        with open(projects_file, 'w') as f:
            pass
    if not os.path.exists(experience_file):
        with open(experience_file, 'w') as f:
            pass
    if not os.path.exists(skills_file):
        with open(skills_file, 'w') as f:
            pass
    if not os.path.exists(achievements_file):
        with open(achievements_file, 'w') as f:
            pass
