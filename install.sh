#!/usr/bin/env bash
if (( $EUID != 0 )); then
    echo "Please run me as root"
    exit
fi

SEPR="|===================|"

function bigEcho {
    echo ${SEPR} ${1} ${SEPR}
}

echo "Running as root"
bigEcho "Checking installed packages"

function checkGlobal {
    echo -n Checking ${1}...
    if ! which ${1} > /dev/null; then
        echo false
        echo !!! ${1} not found
        read -r -p "Install? [y/n]" response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
            sudo apt-get install ${1}
            if [[ ${1} == "wkhtmltopdf" ]]; then
                bigEcho "Executing wkhtmltopdf installer"
                sudo bash ./wkhtmltox.sh
            fi
            if ${1} | grep mongo; then
                sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
                echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
                sudo apt-get update
                sudo apt-get install -y mongodb-org
            fi
        else
            exit
        fi
    fi
    echo " true"
}

function checkNpm {
    echo -n Checking ${1}...
    if ! npm list --global=true ${1} > /dev/null; then
        echo " false"
        echo !!! ${1} not found
        read -r -p "Install? [y/n]" response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
            sudo npm i -g ${1}
        else
            exit
        fi
    fi
    echo true
}

function checkPip {
    echo -n Checking ${1}...
    if ! ${PIP} list --format=columns | grep ${1} > /dev/null; then
        echo " false"
        echo !!! ${1} not found
        read -r -p "Install? [y/n]" response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
            sudo ${PIP} i ${1}
        else
            exit
        fi
    fi
    echo " true"
}

function checkPython {
    local RES=true
    if ! which ${1} > /dev/null; then
        RES=false
    elif [[ $(${1} --version | grep '[0-9]' -o | head -1) != "3" ]]; then
        RES=false
    fi
    echo ${RES}
}

bigEcho "Python"
PYTHON="python"
PIP="pip"

PYTHONCHECK=$(checkPython ${PYTHON})
echo Checking ${PYTHON}: ${PYTHONCHECK}
if ! ${PYTHONCHECK}; then
    PYTHON="python3"
    PIP="pip3"
    PYTHONCHECK=$(checkPython ${PYTHON})
    echo Checking ${PYTHON}: ${PYTHONCHECK}
    if ! ${PYTHONCHECK}; then
        echo "Please install the correct version of python";
        echo "Try sudo apt-get install ${PYTHON}"
        exit;
    fi
fi

bigEcho "Global packets"

checkGlobal ${PIP}
checkGlobal "mongo"
checkGlobal "mongod"
checkGlobal "mongoimport"
checkGlobal "nodejs"
checkGlobal "npm"
checkGlobal "wkhtmltopdf"

bigEcho "Npm packets"
checkNpm "bower"

bigEcho "Python packets"
checkPip "virtualenv"

bigEcho "Bower dependencies"
if ! ls app/static | grep "bower_components"; then
    bower install
fi

echo "Look like all packets installed."
bigEcho "Creating virtual environment"
if ! ls | grep "venv"; then
    echo "Looks like enviroment is not created yet"
    virtualenv venv
fi
echo "Switching to virtualenv"
source ./venv/bin/activate
PYTHON="python"
PIP="pip"

bigEcho "Starting database"
if ! ps -e | grep "mongod" > /dev/null; then
    sudo systemctl start mongod
    sleep 4
else
    echo "MongoDB Server is running"
fi
if ! mongo moevm_flask --eval 'db.getUsers()' | grep python > /dev/null; then
    echo 'Creating user...'
    mongo moevm_flask --eval 'db.createUser( { user: "python", pwd: "python", roles: [ { role: "readWrite", db: "moevm" } ] } )'
fi
if ! mongo moevm_flask --eval 'db.Models.find()' | grep _id > /dev/null; then
    echo 'Importing models...'
    mongoimport --db moevm_flask --collection Models --file models.json
fi
if ! mongo moevm_flask --eval 'db.Reports.find()' | grep _id > /dev/null; then
    echo 'Importing reports'
    mongoimport --db moevm_flask --collection Reports --file reports.json
fi

bigEcho "Running python install"
${PYTHON} setup.py install

bigEcho "Checking if all installed ok"
checkPip Flask
checkPip pymongo
checkPip flask-mongoengine
checkPip Flask-Login
checkPip mongoengine
checkPip Faker
checkPip pdfkit
checkPip Flask-WTF
checkPip Flask-DebugToolbar
checkPip six
checkPip blinker
checkPip WTForms
checkPip text-unidecode
checkPip python-dateutil

echo 'Look like everything is fine!'