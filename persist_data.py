from peewee import *
from datetime import datetime

db = MySQLDatabase()


def parse_date_time(date):  # dd/mm/yyyy - HH:mm
    if '-' not in date:  # alguns pdf's nao tem - na data, resolvendo de forma simples por eqto
        return datetime.strptime(date, '%d/%m/%Y %H:%M')
    else:
        return datetime.strptime(date, '%d/%m/%Y - %H:%M')


class Flight(Model):
    autoridade = CharField()
    origem = CharField()
    data_decolagem = DateTimeField()
    destino = CharField()
    data_pouso = DateTimeField()
    motivo = CharField()
    previsao_passageiros = IntegerField()

    class Meta:
        database = db


def save_line_to_db(flight_line, xml):
    print('obj: {0}, xml: {1}'.format(flight_line, xml))
    print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(flight_line[0], flight_line[1], flight_line[2], flight_line[3], flight_line[4], flight_line[5], flight_line[6]))
    flight = Flight(autoridade=flight_line[0],
                    origem=flight_line[1],
                    data_decolagem=parse_date_time(flight_line[2]),
                    destino=flight_line[3],
                    data_pouso=parse_date_time(flight_line[4]),
                    motivo=flight_line[5],
                    previsao_passageiros=flight_line[6])
    # flight.save()


def close_db():
    pass
