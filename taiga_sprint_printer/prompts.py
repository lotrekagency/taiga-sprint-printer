import inquirer

from .errors import CancelledByUserError


def check_answer(answers):
    if not answers:
        raise CancelledByUserError()


def ask_credentials(default_host, default_user):
    questions = [
        inquirer.Text(
            'host', message="Your taiga api host", default=default_host
        ),
        inquirer.Text(
            'user', message="Your taiga username", default=default_user
        ),
        inquirer.Password('password', message="Your taiga password"),
    ]
    answers = inquirer.prompt(questions)
    check_answer(answers)
    return answers['host'], answers['user'], answers['password']


def ask_password(current_user):
    questions = [
        inquirer.Password(
            'password',
            message="Taiga password for {0}".format(current_user)
        ),
    ]
    answers = inquirer.prompt(questions)
    check_answer(answers)
    return answers['password']


def ask_project(current_project):
    findproject = [
        inquirer.Text(
            'project',
            message="Taiga project slug", default=current_project
        ),
    ]
    answers = inquirer.prompt(findproject)
    check_answer(answers)
    return answers['project']


def ask_file_destination():
    findproject = [
        inquirer.Text(
            'file_destination',
            message="File destination",
        ),
    ]
    answers = inquirer.prompt(findproject)
    check_answer(answers)
    file_destination = answers['file_destination']
    if not file_destination.endswith('.pdf'):
        file_destination = file_destination + '.pdf'
    return file_destination


def ask_sprint(milestones_list):
    selectsprint = [
        inquirer.List(
            'sprint',
            message="Select the sprint you want to print",
            choices=milestones_list
        ),
    ]
    answers = inquirer.prompt(selectsprint)
    check_answer(answers)
    return answers['sprint']


def ask_colors(default_us_color, default_task_color):
    questions = [
        inquirer.Text(
            'us_color',
            message="Default color for user stories", default=default_us_color
        ),
        inquirer.Text(
            'task_color',
            message="Default color for tasks", default=default_task_color
        ),
    ]
    answers = inquirer.prompt(questions)
    check_answer(answers)
    return answers['us_color'], answers['task_color']
