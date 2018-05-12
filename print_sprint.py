from taiga import TaigaAPI
from weasyprint import HTML
from datetime import date
import jinja2
import inquirer


def convertHtmlToPdf():

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
        inquirer.List('sprint', message="Select your sprint", choices=milestonesList ),
    ]

    selectsprintAnswer = inquirer.prompt(selectsprint)
    sprint = selectsprintAnswer['sprint']

    tasks = api.tasks.list()
    sprint = api.milestones.list(project=project.id).filter(name=sprint)
    stories = api.user_stories.list(project__name=project,milestone=sprint[0].id)

    sourceHtml = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath='')).get_template(
        'template.html').render(date=date.today().strftime('%d, %b %Y'),
                                    stories=stories,tasks=tasks)
    
    outputFilename = "test.pdf"
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pdf = HTML(string=sourceHtml).write_pdf(resultFile)

    # close output file
    resultFile.close()


# Main program
if __name__ == "__main__":
    convertHtmlToPdf()