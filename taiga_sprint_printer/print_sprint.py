import jinja2
import inquirer

from datetime import date
from taiga import TaigaAPI
from weasyprint import HTML


def print_sprint():

    sourceHtml = ''
    outputFilename = ''
    
    questions = [
        inquirer.Text('host', message="Your taiga api host"),
        inquirer.Text('user', message="Your taiga username"),
        inquirer.Password('password', message="Your taiga password"),    
    ]

    answers = inquirer.prompt(questions)

    api = TaigaAPI(
        host=answers['host']
    )

    api.auth(
        username=answers['user'],
        password=answers['password']
    )

    findproject = [
        inquirer.Text('project', message="taiga project" ),
    ]

    findprojectAnswers = inquirer.prompt(findproject)
    prjslug = findprojectAnswers['project']
    
    project = api.projects.get_by_slug(prjslug)

    milestones = api.milestones.list(project__name=project)
    milestonesList = []

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

    tasks = api.tasks.list()
    sprint = api.milestones.list(project=project.id).filter(name=sprint)
    stories = api.user_stories.list(project__name=project, milestone=sprint[0].id)

    sourceHtml = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath='')
    ).get_template('templates/template.html').render(
        date=date.today().strftime('%d, %b %Y'),
        stories=stories,
        tasks=tasks
    )
    
    outputFilename = "test.pdf"

    resultFile = open(outputFilename, "w+b")
    pdf = HTML(string=sourceHtml).write_pdf(resultFile)
    resultFile.close()
