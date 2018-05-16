from setuptools import setup, find_packages


package_data = ['templates/*.html']

setup(
    name='taiga-sprint-printer',
    packages=['taiga_sprint_printer'],
    package_dir={'taiga_sprint_printer': 'taiga_sprint_printer'},
    package_data={'taiga_sprint_printer': package_data},
    version='0.2.0',
    url='https://github.com/lotrekagency/taiga-sprint-printer',
    install_requires=[
        'python-taiga==0.9.0',
        'WeasyPrint==0.42.3',
        'Jinja2==2.10',
        'inquirer==2.2.0'
    ],
    description="A simple tool for printing your sprint from Taiga",
    long_description=open('README.rst', 'r').read(),
    license="MIT",
    author="Lotrek",
    author_email="dimmitutto@lotrek.it",
    keywords= "taiga sprint story agile planning task management",
    entry_points = {
        'console_scripts': [
            'sprint-printer = taiga_sprint_printer.main:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    zip_safe = False,
)
