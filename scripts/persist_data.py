from peewee import *

from date_parser import parse_date_time

db = MySQLDatabase()
flights_to_save = []


class RawData(Model):
    autoridade = CharField()
    origem = CharField()
    data_decolagem = DateTimeField()
    destino = CharField()
    data_pouso = DateTimeField()
    motivo = CharField()
    previsao_passageiros = IntegerField()

    class Meta:
        database = db
        db_table = "raw_data"


def create_db_model(flight_line, xml):
    # print('obj: {0}, xml: {1}'.format(flight_line, xml))
    # print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(flight_line[0], flight_line[1], flight_line[2], flight_line[3], flight_line[4], flight_line[5], flight_line[6]))

    if is_int(flight_line[6]):
        motivo = flight_line[5]
        previsao = flight_line[6]
    else:
        motivo = flight_line[6]
        previsao = flight_line[5]

    flight = RawData(autoridade=" ".join(flight_line[0].split()),
                     origem=flight_line[1],
                     data_decolagem=parse_date_time(flight_line[2]),
                     destino=flight_line[3],
                     data_pouso=parse_date_time(flight_line[4]),
                     motivo=motivo,
                     previsao_passageiros=previsao)
    flights_to_save.append(flight)


def is_int(text):
    try:
        # pdf's de 2013 tem padrao diferente, ultimas colunas sao previsao / motivo
        # ao inves de motivo / previsao
        int(text)
        return True
    except ValueError:
        return False


def close_db():
    pass


def bulk_insert():
    print("saving %d records to database" % len(flights_to_save))
    with db.atomic():  # entender pq Model.insert_many nao funciona
        for data_dict in flights_to_save:
            data_dict.save()
