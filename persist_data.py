from peewee import *
from datetime import datetime

db = MySQLDatabase()


def parseDateTime(date):  # dd/mm/yyyy - HH:mm
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


def saveLineToDB(flightLine, xml):
    print('obj: {0}, xml: {1}'.format(flightLine, xml))
    print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(flightLine[0], flightLine[1], flightLine[2], flightLine[3], flightLine[4], flightLine[5], flightLine[6]))
    flight = Flight(autoridade=flightLine[0],
                    origem=flightLine[1],
                    data_decolagem=parseDateTime(flightLine[2]),
                    destino=flightLine[3],
                    data_pouso=parseDateTime(flightLine[4]),
                    motivo=flightLine[5],
                    previsao_passageiros=flightLine[6])
    # flight.save()


def closeDb():
    pass
