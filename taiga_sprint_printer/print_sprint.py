import jinja2
import inquirer
import os

from datetime import date
from taiga import TaigaAPI
from taiga.exceptions import TaigaException
from weasyprint import HTML

from .configuration import Configuration
from .messages import success_message, warning_message, error_message, progress_message


def get_current_dir():
    return os.path.split(__file__)[0]


def print_sprint():

    configuration = Configuration()

    templates_path = os.path.join(get_current_dir(), 'templates')
    
    questions = [
        inquirer.Text('host', message="Your taiga api host"),
        inquirer.Text('user', message="Your taiga username"),
        inquirer.Password('password', message="Your taiga password"),    
    ]

    answers = inquirer.prompt(questions)

    try:
        api = TaigaAPI(
            host=answers['host']
        )

        api.auth(
            username=answers['user'],
            password=answers['password']
        )
        # Store username and host
    except TaigaException as ex:
        print(error_message(str(ex)))
        return 1

    findproject = [
        inquirer.Text('project', message="taiga project" ),
    ]

    findprojectAnswers = inquirer.prompt(findproject)
    prjslug = findprojectAnswers['project']
    
    try:
        project = api.projects.get_by_slug(prjslug)

        milestones = api.milestones.list(project__name=project)
        milestonesList = []
    except TaigaException as ex:
        print(error_message(str(ex)))
        return 1

    for el in milestones:
        milestonesList.append(el.name)

    selectsprint = [
        inquirer.List(
            'sprint', 
            message="Select the sprint you want to print", 
            choices=milestonesList 
        ),
    ]

    selectsprintAnswer = inquirer.prompt(selectsprint)
    sprint = selectsprintAnswer['sprint']

    try:
        print (progress_message(0, 4, '📅  Fetching the sprint'))
        sprint = api.milestones.list(project=project.id).filter(name=sprint)
        print (progress_message(1, 4, '📗  Fetching stories'))
        stories = api.user_stories.list(project__name=project, milestone=sprint[0].id)
        print (progress_message(2, 4, '📄  Fetching tasks'))
        tasks = api.tasks.list()
    except TaigaException as ex:
        print(error_message(str(ex)))
        return 1

    print (progress_message(3, 4, '🎨  Start rendering the template'))

    sourceHtml = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=templates_path)
    ).get_template('sprinttmp.html').render(
        date=date.today().strftime('%d, %b %Y'),
        stories=stories,
        tasks=tasks,
        config=configuration.get_config()
    )

    print (progress_message(4, 4, '👷🏻  Generating the pdf'))
    
    with open("test.pdf", "w+b") as f:
        pdf = HTML(string=sourceHtml).write_pdf(f)

    print (success_message('Done! The pdf is ready to be printed'))