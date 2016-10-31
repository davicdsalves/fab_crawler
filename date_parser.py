from datetime import datetime


def parse_date_time(date):  # dd/mm/yyyy - HH:mm
    if '-' not in date:  # alguns pdf's nao tem - na data, resolvendo de forma simples por eqto
        return datetime.strptime(date, '%d/%m/%Y %H:%M')
    else:
        return datetime.strptime(date, '%d/%m/%Y - %H:%M')


def is_merged_date(text):
    if not is_date(text):
        return text.count('/') == 2 and text.count(':') == 1
    return False


def is_date(text):
    try:
        parse_date_time(text)
        return True
    except ValueError:
        return False


def date_at_beginning(text):
    return text.index('/') == 2


# formatos possiveis de data
# 1) normal: 12/05/2014 - 15:00
# 2) 12/05/2014 - 15:00 Brasília
# 3) Brasília 12/05/2014 - 15:00
# metodo chamado caso encontre um texto que contenha data e Cidade
def parse_date(text: str):
    splited = []
    if date_at_beginning(text):
        colon_position = text.index(':')
        date_limit = colon_position + 3
        date = text[:date_limit].strip()
        city = text[date_limit:].strip()
        splited.append(date)
        splited.append(city)
    else:
        first_slash_position = text.index('/')
        date_limit = first_slash_position - 2
        city = text[:date_limit].strip()
        date = text[date_limit:].strip()
        splited.append(city)
        splited.append(date)
    return splited
