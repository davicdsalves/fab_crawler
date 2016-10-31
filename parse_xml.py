import xml.etree.cElementTree as eTree
from glob import glob
import os
from persist_data import saveLineToDB, closeDb


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
def isTextMerged(allText):
    dateLength = 18
    return len(allText) > dateLength and allText.count('/') > 1


def isDoubleLine(previousLineTag: eTree.Element, textTag: eTree.Element):
    return previousLineTag.attrib['left'] == textTag.attrib['left']


def parseXmlLines(xmlData, xml):
    flight = []
    previousLineTag = xmlData[0]
    lineCounter = 0
    for textTag in xmlData:
        if textTag.text is not None:
            allText = "".join(textTag.itertext()).strip()
            if isInvalidLine(allText):
                continue

            lineCounter += 1

            if isTextMerged(allText):
                flight.append(allText[:18])
                flight.append(allText[18:])
                lineCounter += 1
            elif lineCounter > 1 and isDoubleLine(previousLineTag, textTag):
                print(flight)
                print(lineCounter)
                doubleLineText = flight[lineCounter - 2] + allText
                flight[lineCounter - 2] = doubleLineText
                lineCounter -= 1
            else:
                flight.append(allText)

            if lineCounter == 7:  # 7 informacoes sao uma linha
                lineCounter = 0
                saveLineToDB(flight, xml)
                del flight[:]

            previousLineTag = textTag


# 2013 tem formato diferente, e AERONAVE usa font[1]
# olhar /2014/Janeiro/20140122_174018.pdf.xml
def getYearFolder():
    # years = ['2016', '2015', '2014']
    years = ['2014']
    for year in years:
        yearDir = '%s/%s/**/*.pdf.xml' % (os.getcwd(), year)
        parseXml(glob(yearDir))
        closeDb()


def checkForError(root, xml):  # ver a necessidade
    counterForShareFlight = 0
    if counterForShareFlight == 0:
        zeroFont = root.findall("*/text[@font='0']")
        for textTag in zeroFont:
            allText = "".join(textTag.itertext())
            if "AERONAVE" in allText:
                print("error? [ {0} ]".format(xml))


getYearFolder()
