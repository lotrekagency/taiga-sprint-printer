from .configuration import Configuration
from .prompts import ask_colors


def change_colors():
    configuration = Configuration()

    us_color = configuration.get_config('colors', 'userstory')
    task_color = configuration.get_config('colors', 'task')

    us_color, task_color = ask_colors(us_color, task_color)

    configuration.set_config('colors', 'userstory', us_color)
    configuration.set_config('colors', 'task', task_color)
