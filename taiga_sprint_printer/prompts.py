import inquirer


def ask_credentials():
    questions = [
        inquirer.Text('host', message="Your taiga api host"),
        inquirer.Text('user', message="Your taiga username"),
        inquirer.Password('password', message="Your taiga password"),
    ]
    answers = inquirer.prompt(questions)
    return answers['host'], answers['user'], answers['password']


def ask_password(current_user):
    questions = [
        inquirer.Password(
            'password',
            message="Taiga password for {0}".format(current_user)
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['password']


def ask_project(current_project):
    findproject = [
        inquirer.Text(
            'project',
            message="Taiga project slug", default=current_project
        ),
    ]
    answers = inquirer.prompt(findproject)
    return answers['project']


def ask_sprint(milestones_list):
    selectsprint = [
        inquirer.List(
            'sprint',
            message="Select the sprint you want to print",
            choices=milestones_list
        ),
    ]
    answers = inquirer.prompt(selectsprint)
    return answers['sprint']
