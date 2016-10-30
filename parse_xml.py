import xml.etree.cElementTree as eTree
from glob import glob
import os
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
    # print('obj: {0}, xml: {1}'.format(flightLine, xml))
    # print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(flightLine[0], flightLine[1], flightLine[2], flightLine[3], flightLine[4], flightLine[5], flightLine[6]))
    flight = Flight(autoridade=flightLine[0],
                    origem=flightLine[1],
                    data_decolagem=parseDateTime(flightLine[2]),
                    destino=flightLine[3],
                    data_pouso=parseDateTime(flightLine[4]),
                    motivo=flightLine[5],
                    previsao_passageiros=flightLine[6])
    flight.save()


def parseXml(xmls):
    for xml in xmls:
        tree = eTree.parse(xml)
        root = tree.getroot()
        xmlData = root.findall("*/text[@font='1']")
        print('parsing xml[{0}]'.format(xml))
        parseXmlLines(xmlData, xml)


def isInvalidLine(tagText):
    return len(tagText) == 0 or "Página" in tagText


# alguns xmls tem a data e origem/destino na mesma tag.
def isTextMerged(lineCounter, allText):
    dateLength = 18
    return (lineCounter == 3 or lineCounter == 5) and len(allText) > dateLength


def parseXmlLines(xmlData, xml):
    flight = []
    lineCounter = 0
    for textTag in xmlData:
        if textTag.text is not None:
            allText = "".join(textTag.itertext()).strip()
            if isInvalidLine(allText):
                continue

            lineCounter += 1

            if isTextMerged(lineCounter, allText):
                flight.append(allText[:18])
                flight.append(allText[18:])
                lineCounter += 1
            else:
                flight.append(allText)

            if lineCounter == 7:  # 7 informacoes sao uma linha
                lineCounter = 0
                saveLineToDB(flight, xml)
                del flight[:]


# 2013 tem formato diferente, e AERONAVE usa font[1]
# olhar /2014/Janeiro/20140122_174018.pdf.xml
def getYearFolder():
    years = ['2016', '2015']
    for year in years:
        yearDir = '%s/%s/**/*.pdf.xml' % (os.getcwd(), year)
        parseXml(glob(yearDir))


def checkForError(root, xml):  # ver a necessidade
    counterForShareFlight = 0
    if counterForShareFlight == 0:
        zeroFont = root.findall("*/text[@font='0']")
        for textTag in zeroFont:
            allText = "".join(textTag.itertext())
            if "AERONAVE" in allText:
                print("error? [ {0} ]".format(xml))


getYearFolder()
