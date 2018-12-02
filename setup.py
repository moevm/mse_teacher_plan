from setuptools import setup

setup(
    name='mse_teacher_plan',
    version='',
    packages=['app', 'app.api', 'app.models'],
    install_requires=['Flask', 'pymongo', 'flask_mongoengine', 'flask_debugtoolbar',
                      'flask_login', 'mongoengine', 'faker', 'pdfkit', 'Flask-WTF', 'six', 'Blinker',
                      'WTForms', 'text-unidecode', 'python-dateutil'],
    url='',
    license='',
    author='thexc',
    author_email='',
    description=''
)
