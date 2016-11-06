import json
import os
import time
from datetime import datetime
from urllib.error import HTTPError

import wget

from ph2 import ParseHub

ph = ParseHub(os.environ.get('PARSEHUB_KEY'))


def get_project_data():
    current_year = datetime.now().year
    projects = ph.projects
    print(projects)

    for i in range(0, 4):
        flight_year = (current_year - i)
        filename = 'voo_%d.json' % flight_year
        print('\nparsing %s' % filename)
        if not os.path.isfile(filename):
            project_last_run = projects[i].last_run
            print('retrieve project run {0}'.format(project_last_run))
            project_data = project_last_run.get_data()
            with open(filename, 'w') as file:
                json.dump(project_data, file)

        parse_project_data(filename, flight_year)
    print('done downloading pdfs')


def parse_project_data(filename, flight_year):
    with open(filename) as project_data:
        data = json.load(project_data)
    create_dir(flight_year)

    months = data["month"]
    for month in months:
        if 'days' in month:
            get_month_data(flight_year, month["name"], month["days"])


def get_month_data(flight_year, month_name, month_days):
    month_folder = '%s/%s' % (flight_year, month_name)
    create_dir(month_folder)
    print('parsing %s(%s)' % (month_name, flight_year))
    days = []

    for day in month_days:
        days.append(day["name"])
        pdf_url = day["url"]
        pdf_url_split = pdf_url.split('/')
        pdf_name = pdf_url_split[len(pdf_url_split) - 1]
        local_pdf_file = '%s/%s' % (month_folder, pdf_name)

        if not os.path.isfile(local_pdf_file):
            print('\ndownloading %s-%s[%s]' % (month_name, day["name"], pdf_url))
            try:
                wget.download(pdf_url, month_folder)
            except HTTPError as e:
                if e.code == 404:
                    print('error downloading %s, sleep for 3 seconds. will retry 1 more time.' % pdf_url)
                    time.sleep(3)
                    wget.download(pdf_url, month_folder)
    print('month[%s], days[%s] done.' % (month_name, ', '.join(days)))


def create_dir(name):
    if not os.path.exists(str(name)):
        os.makedirs(str(name))


get_project_data()
