# teacherPlan
ИС Кафедры: индивидуальные планы преподавателей

Требуется разработать компоненты информационной системы кафедры, обеспечивающие управление индифидуальными планами преподавателей

*  Планирование учебной нагрузки
*  Переподготовка и повышение квалификации
*  Участие в мероприятиях, конференциях,
*  Руководство НИР
*  Генерация отчетов
*  и другие параметры индивидуального плана


Инструкция по запуску:
Установить mongoDB в C:\Program Files\MongoDB
Установить Robo 3t
Создать папки data\db в каталоге C:\
Запустить mongod.exe из C:\Program Files\MongoDB
Запустить mongo.exe из C:\Program Files\MongoDB
Запустить Robo 3t
В mongo.exe прописать: db.createUser( { user: "SiteUserAdmin", pwd: "password", roles: [ { role: "UserAdminAnyDatabase", db: "Admin" } ] } )
В Robo 3t законнектиться к серверу. Настройки аутентификации: Database = admin, User Name = SiteUserName, password = password
В Robo 3t щелкнуть на Admin правой кнопкой мышкой. Выбрать Create Database. Создать moevm.
В mongo.exe прописать: db.createUser( { user: "python", pwd: "python", roles: [ { role: "readWrite", db: "moevm" } ] } )
Закрыть mongo, mongod, robo 3t
создать ярлык для mongod с параметром --auth
Взять путь для manage.py в проекте, и для него в cmd-консоли прописать: путь\manage.py createsuperuser
В появившемся окне ввести следующие данные: username: admin, email: , password: admin, again password: admin
Запустить проект по адресу: http://127.0.0.1:8000/admin и ввести логин и пароль из пред. шага
Создать в новом окне юзера
Готово



