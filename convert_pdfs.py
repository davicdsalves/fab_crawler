from glob import glob
import os
from subprocess import Popen, PIPE


def getYearFolder():
    years = ['2016', '2015', '2014', '2013']
    for year in years:
        yearDir = '%s/%s/**/*.pdf' % (os.getcwd(), year)
        convertPdfToHtml(glob(yearDir))


def convertPdfToHtml(pdfs):
    for pdfPath in pdfs:
        pdfPathSplit = pdfPath.split('/')
        pdfName = pdfPathSplit[len(pdfPathSplit) - 1]
        pdfPathFolder = pdfPath[0:pdfPath.rfind('/')]
        outputFile = "{0}/{1}".format(pdfPathFolder, pdfName)
        print('converting %s to html' % pdfName)
        command = ['pdftohtml', '-nomerge', '-xml', '-s', '-noframes', pdfPath, outputFile]
        with Popen(command, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='')


getYearFolder()
