from setuptools import setup, find_packages


package_data = ['templates/*.html']

setup(
    name='taiga_sprint_printer',
    version='0.0.0',
    url='https://github.com/lotrekagency/taiga-sprint-printer',
    package_data={'taiga_sprint_printer': package_data},
    install_requires=[
        'python-taiga==0.9.0',
        'WeasyPrint==0.42.3',
        'Jinja2==2.10',
        'inquirer==2.2.0'
    ],
    description="A simple tool for printing your sprint from Taiga",
    long_description=open('README.md', 'r').read(),
    license="MIT",
    author="Lotrek",
    author_email="dimmitutto@lotrek.it",
    packages=find_packages(),
    include_package_data=True,
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
    ]
)