import xml.etree.cElementTree as etree
from glob import glob
import os


def parseXml(xmls):
    for xml in xmls:
        tree = etree.parse(xml)
        root = tree.getroot()
        xmlData = root.findall("*/text[@font='1']")
        for text in xmlData:
            print(text)



def getYearFolder():
    years = ['2016', '2015', '2014', '2013']
    for year in years:
        yearDir = '%s/%s/**/*.pdf.xml' % (os.getcwd(), year)
        parseXml(glob(yearDir))
