import jinja2
import math
import os
import sys

from datetime import date
from taiga import TaigaAPI
from taiga.exceptions import TaigaException
from weasyprint import HTML

from .configuration import Configuration
from .messages import success_message, error_message, progress_message

from .prompts import ask_credentials, ask_password, \
    ask_project, ask_sprint, ask_file_destination
from .utils import get_current_dir


def print_sprint(new=False):

    configuration = Configuration()

    host = configuration.get_config('taiga', 'host')
    user = configuration.get_config('taiga', 'user')

    templates_path = os.path.join(get_current_dir(), 'templates')

    if not new and host and user:
        password = ask_password(user)
    elif new:
        host, user, password = ask_credentials(host, user)
    else:
        host, user, password = ask_credentials()

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

    project_slug = ask_project(
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
        milestones_list.append('{0}: {1}'.format(el.id, el.name))

    selected_sprint = ask_sprint(milestones_list)

    file_destination = ask_file_destination()

    path_destination = os.path.dirname(file_destination)
    if path_destination:
        os.makedirs(os.path.dirname(file_destination), exist_ok=True)

    try:
        print(progress_message(1, 5, '📅  Fetching the sprint'))
        sprint = milestones.filter(id=int(selected_sprint.split(': ')[0]))
        print(progress_message(2, 5, '📗  Fetching stories'))
        stories = api.user_stories.list(
            project__name=project,
            milestone=sprint[0].id
        )
        tasks = []
        us_tasks_completed = 0
        for i, story in enumerate(stories):
            end_charcater = '\r'
            if (i + 1) == len(stories):
                end_charcater = '\n'
            us_tasks_completed = math.ceil(((i + 1) / len(stories)) * 100)
            print(progress_message(
                3, 5,
                '📄  Fetching tasks for stories {0}%'.format(us_tasks_completed)
            ), end=end_charcater)
            sys.stdout.flush()
            tasks.extend(story.list_tasks())
    except TaigaException as ex:
        print(error_message(str(ex)))
        return 1

    print(progress_message(4, 5, '🎨  Start rendering the template'))

    sourceHtml = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=templates_path)
    ).get_template('sprinttmp.html').render(
        date=date.today().strftime('%d, %b %Y'),
        stories=stories,
        tasks=tasks,
        config=configuration.get_config()
    )

    print(progress_message(5, 5, '👷🏻  Generating the pdf'))

    with open(file_destination, "w+b") as f:
        HTML(string=sourceHtml).write_pdf(f)

    print(success_message('Done! The pdf is ready to be printed 🖨'))

    return 0
