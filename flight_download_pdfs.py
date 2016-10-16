import json
import os
from urllib.error import HTTPError
import time
import wget
from datetime import datetime
from ph2 import ParseHub

ph = ParseHub(os.environ.get('PARSEHUB_KEY'))


def getProjectData():
    currentYear = datetime.now().year
    projects = ph.projects
    print(projects)

    for i in range(0, 4):
        flightYear = (currentYear - i)
        filename = 'voo_%d.json' % flightYear
        print('\nparsing %s' % filename)
        if not os.path.isfile(filename):
            projectLastRun = projects[i].last_run
            print('retrieve project run {0}'.format(projectLastRun))
            projectData = projectLastRun.get_data()
            with open(filename, 'w') as file:
                json.dump(projectData, file)

        parseProjectData(filename, flightYear)
    print('done downloading pdfs')


def parseProjectData(filename, flightYear):
    with open(filename) as projectData:
        data = json.load(projectData)
    createDir(flightYear)

    months = data["month"]
    for month in months:
        if 'days' in month:
            getMonthData(flightYear, month["name"], month["days"])


def getMonthData(flightYear, monthName, monthDays):
    monthFolder = '%s/%s' % (flightYear, monthName)
    createDir(monthFolder)
    print('parsing %s(%s)' % (monthName, flightYear))
    days = []

    for day in monthDays:
        days.append(day["name"])
        pdfUrl = day["url"]
        pdfUrlSplit = pdfUrl.split('/')
        pdfName = pdfUrlSplit[len(pdfUrlSplit) - 1]
        localPdfFile = '%s/%s' % (monthFolder, pdfName)

        if not os.path.isfile(localPdfFile):
            print('\ndownloading %s-%s[%s]' % (monthName, day["name"], pdfUrl))
            try:
                wget.download(pdfUrl, monthFolder)
            except HTTPError as e:
                if e.code == 404:
                    print('error downloading %s, sleep for 3 seconds.' % pdfUrl)
                    time.sleep(3)
                    wget.download(pdfUrl, monthFolder)
    print('month[%s], days[%s] done.' % (monthName, ', '.join(days)))


def createDir(name):
    if not os.path.exists(str(name)):
        os.makedirs(str(name))


getProjectData()
