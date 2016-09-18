import json
import os
import wget
from datetime import datetime
from ph2 import ParseHub
ph = ParseHub('')

def getProjectData():
	currentYear = datetime.now().year
	projects = ph.projects
	print(projects)

	for i in range(0,4):
		flightYear = (currentYear - i)
		filename = 'voo_%d.json' % flightYear
		print(filename)
		if not os.path.isfile(filename):
				projectData = projects[i].last_ready_run.get_data()
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
	monthFolder = '%s/%s' % (flightYear,monthName)
	createDir(monthFolder)
	print('\nparsing %s(%s)' % (monthName,flightYear))
	
	for day in monthDays:
		pdfUrl = day["url"]
		pdfUrlSplit = pdfUrl.split('/')
		pdfName = pdfUrlSplit[len(pdfUrlSplit)-1]
		localPdfFile = '%s/%s' % (monthFolder, pdfName)

		if not os.path.isfile(localPdfFile):
			print('\ndownloading %s-%s[%s]' % (monthName, day["name"], pdfUrl))
			wget.download(pdfUrl, monthFolder)

def createDir(name):
	if not os.path.exists(str(name)):
		os.makedirs(str(name))

getProjectData()
