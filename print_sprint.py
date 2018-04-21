from taiga import TaigaAPI
from xhtml2pdf import pisa
from datetime import date
import jinja2
import inquirer

sourceHtml=''
outputFilename=''

# Utility function
def convertHtmlToPdf():
    questions = [
        inquirer.Text('host', message="your taiga api host"),
        inquirer.Text('project', message="taiga project"),
        inquirer.Text('sprint', message="your sprint name"),
        inquirer.Text('user', message="your taiga username"),
        inquirer.Text('password', message="your taiga password"),
    ]

    answers = inquirer.prompt(questions)
    api = TaigaAPI(
        host=answers['host']
    )

    api.auth(
        username=answers['user'],
        password=answers['password']
    )

   
    prjslug = answers['project']
    sprint = answers['sprint']
    project = api.projects.get_by_slug(prjslug)


    tasks = api.tasks.list()
    milestoneid = api.milestones.list(project=project.id).filter(name=sprint)
    stories = api.user_stories.list(project=project.id,milestone=milestoneid[0].id)


    sourceHtml = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath='')).get_template(
        'template.html').render(date=date.today().strftime('%d, %b %Y'),
                                    stories=stories,tasks=tasks)
    
    outputFilename = "test.pdf"
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convertHtmlToPdf()