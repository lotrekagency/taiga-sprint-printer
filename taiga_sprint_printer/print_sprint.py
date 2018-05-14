import jinja2
import inquirer
import math
import os
import sys

from datetime import date
from taiga import TaigaAPI
from taiga.exceptions import TaigaException
from weasyprint import HTML

from .configuration import Configuration
from .messages import success_message, warning_message, error_message, progress_message


def _get_current_dir():
    return os.path.split(__file__)[0]


def _ask_credentials():
    questions = [
        inquirer.Text('host', message="Your taiga api host"),
        inquirer.Text('user', message="Your taiga username"),
        inquirer.Password('password', message="Your taiga password"),    
    ]
    answers = inquirer.prompt(questions)
    return answers['host'], answers['user'], answers['password']


def _ask_password(current_user):
    questions = [
        inquirer.Password('password', message="Taiga password for {0}".format(current_user)),    
    ]
    answers = inquirer.prompt(questions)
    return answers['password']


def _ask_project(current_project):
    findproject = [
        inquirer.Text('project', message="Taiga project", default=current_project ),
    ]
    answers = inquirer.prompt(findproject)
    return answers['project']


def _ask_sprint(milestones_list):
    selectsprint = [
        inquirer.List(
            'sprint', 
            message="Select the sprint you want to print", 
            choices=milestones_list 
        ),
    ]
    answers = inquirer.prompt(selectsprint)
    return answers['sprint']


def print_sprint():

    configuration = Configuration()

    host = configuration.get_config('taiga', 'host')
    user = configuration.get_config('taiga', 'user')

    templates_path = os.path.join(_get_current_dir(), 'templates')
    
    if host and user:
        password = _ask_password(user)
    else:
        host, user, password = _ask_credentials()

    try:
        api = TaigaAPI(
            host=host
        )
        api.auth(
            username=user,
            password=password
        )
        configuration.set_config('taiga', 'host', host)
        configuration.set_config('taiga', 'user', user)
    except TaigaException as ex:
        print(error_message(str(ex)))
        return 1

    project_slug = _ask_project(
        configuration.get_config('taiga', 'project')
    )
    
    try:
        project = api.projects.get_by_slug(project_slug)
        milestones = api.milestones.list(project__name=project)
        milestones_list = []
        configuration.set_config('taiga', 'project', project_slug)
    except TaigaException as ex:
        print(error_message(str(ex)))
        return 1

    for el in milestones:
        milestones_list.append(el.name)

    selected_sprint = _ask_sprint(milestones_list)

    try:
        print (progress_message(1, 5, '📅  Fetching the sprint'))
        sprint = api.milestones.list(project=project.id).filter(name=selected_sprint)
        print (progress_message(2, 5, '📗  Fetching stories'))
        stories = api.user_stories.list(project__name=project, milestone=sprint[0].id)
        tasks = []
        us_tasks_completed = 0
        for i, story in enumerate(stories):
            end_charcater = '\r'
            if (i + 1) == len(stories):
                end_charcater = '\n'
            us_tasks_completed = math.ceil(((i + 1) / len(stories)) * 100)
            print (progress_message(
                3, 5, '📄  Fetching tasks for stories {0}%'.format(us_tasks_completed)
            ), end=end_charcater)
            sys.stdout.flush()
            tasks.extend(story.list_tasks())
    except TaigaException as ex:
        print(error_message(str(ex)))
        return 1

    print (progress_message(4, 5, '🎨  Start rendering the template'))

    sourceHtml = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=templates_path)
    ).get_template('sprinttmp.html').render(
        date=date.today().strftime('%d, %b %Y'),
        stories=stories,
        tasks=tasks,
        config=configuration.get_config()
    )

    print (progress_message(5, 5, '👷🏻  Generating the pdf'))
    
    with open("test.pdf", "w+b") as f:
        pdf = HTML(string=sourceHtml).write_pdf(f)

    print (success_message('Done! The pdf is ready to be printed 🖨'))
