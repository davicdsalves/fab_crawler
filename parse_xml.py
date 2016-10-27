import xml.etree.cElementTree as eTree
from glob import glob
import os


def parseXml(xmls):
    shareFlight = ["(1)", "(2)", "(3)", "(4)"]
    for xml in xmls:
        counterForShareFlight = 0 # se encontra voo compartilhado, esse valor no final tem q ser par
        tree = eTree.parse(xml)
        root = tree.getroot()
        xmlData = root.findall("*/text[@font='1']")
        for textTag in xmlData:
            if textTag.text is not None:
                allText = "".join(textTag.itertext())
                if any(x in allText for x in shareFlight):
                    counterForShareFlight += 1
                    # print(allText)
            else:
                print(xml)
        if counterForShareFlight == 0:
            zeroFont = root.findall("*/text[@font='0']")
            for textTag in zeroFont:
                allText = "".join(textTag.itertext())
                if "AERONAVE" in allText:
                    print("error? [ {0} ]".format(xml))


# 2013 tem formato diferente, e AERONAVE usa font[1]
# olhar /2014/Janeiro/20140122_174018.pdf.xml

def getYearFolder():
    years = ['2016', '2015', '2014']
    for year in years:
        yearDir = '%s/%s/**/*.pdf.xml' % (os.getcwd(), year)
        parseXml(glob(yearDir))


getYearFolder()
