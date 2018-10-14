def f(text, name, type, opts=None, value=''):
    if opts is None:
        opts = []
    return {'text': text, 'name': name, 'type': type, 'opts': opts, 'value': value}


def m(text, name, fields):
    return {'text': text, 'name': name, 'fields': fields}


books_fields = [
    f('Авторы', 'authors', 'text'),
    f('Название', 'bookName', 'text'),
    f('Дисциплина', 'discipline', 'text'),
    f('Год выпуска', 'yeardate', 'year'),
    f('Издательство', 'organization', 'text'),
    f('Шифр', 'cipher', 'text')
]

discipline_fields = [
    f('Дисциплина', 'disc', 'text'),
    f('Характер измененений', 'characterUpdate', 'text'),
    f('Тип', 'type', 'text'),
    f('Отметка о выполнении', 'completeMark', 'text')
]

scienceWork_fields = [
    f('Дата начала', 'startDate', 'date'),
    f('Организация', 'organization', 'text'),
    f('Название научной работы', 'workName', 'text'),
    f('Дата окончания', 'finishDate', 'date'),
    f('Роль', 'role', 'text'),
    f('Шифр', 'cipher', 'text')
]

conf_fields = [
    f('Название события', 'event_name', 'text'),
    f('Уровень', 'level', 'text'),
    f('Дата проведения', 'date', 'date'),
    f('Место проведения', 'place', 'text'),
    f('Тип', 'typeConf', 'text',
      opts=['Конкурс', 'Выставка', 'Конференция', 'Семинар'])
]

publ_fields = [
    f('Тип', 'publicationType', 'text',
      opts=['Методическое указание', 'Книга', 'Статья в журнале', 'Сборник']),
    f('Вид повторение', 'reiteration', 'text',
      opts=['Одноразовый', 'Повторяющийся']),
    f('Название', 'name', 'text'),
    f('Единицы объема', 'unitVolume', 'text'),
    f('Название издательства', 'publishHouseName', 'text'),
    f('Номер издания', 'number', 'text'),
    f('Объем', 'volume', 'text'),
    f('Тираж', 'edition', 'text'),
    f('Место издания', 'place', 'text'),
    f('Редактор', 'editor', 'text'),
    f('Дата', 'date', 'text'),
    f('ISBN', 'isbn', 'text'),
    f('Вид', 'type', 'text')
]

kval_fields = [
    f('Название', 'courseName', 'text'),
    f('Дисциплина', 'discipline', 'text'),
    f('Спикеры', 'authors', 'text'),
    f('Дата начала', 'startDate', 'date'),
    f('Дата окончания', 'finishDate', 'date'),
    f('Организация', 'organization', 'text')
]

other_fields = [
    f('Дата начала', 'startDate', 'date'),
    f('Дата окончания', 'finishDate', 'date'),
    f('Вид_работы', 'kindOfWork', 'text')
]

models = [  # TODO Convertation from models or applying real ones (?)
    m('Подготовка учебников', 'books', books_fields),
    m('Постановка и модернизация дисциплин', 'discipline', discipline_fields),
    m('Научная работа', 'scienceWork', scienceWork_fields),
    m('Участие в конференциях и выставках', 'conf', conf_fields),
    m('Список публикаций', 'publ', publ_fields),
    m('Повышение квалификации', 'kval', kval_fields),
    m('Другие виды работ', 'other', other_fields)
]

