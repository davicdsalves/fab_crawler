import xml.etree.cElementTree as eTree
from glob import glob
import os
from persist_data import save_line_to_db, close_db
from date_parser import is_merged_date, parse_date


def parse_xml(xmls):
    for xml in xmls:
        tree = eTree.parse(xml)
        root = tree.getroot()
        xml_data = root.findall("*/text[@font='1']")
        print('parsing xml[{0}]'.format(xml))
        parse_xml_lines(xml_data, xml)


def is_invalid_line(tag_text):
    return len(tag_text) == 0 or "Página" in tag_text


# alguns xmls tem a data e origem/destino na mesma tag.
def is_text_merged(all_text):
    date_length = 18
    return len(all_text) > date_length and all_text.count('/') == 2


def is_double_line(previous_line_tag: eTree.Element, text_tag: eTree.Element):
    return previous_line_tag.attrib['left'] == text_tag.attrib['left']


def parse_xml_lines(xml_data, xml):
    flight = []
    previous_line_tag = xml_data[0]
    line_counter = 0
    for textTag in xml_data:
        if textTag.text is not None:
            all_text = "".join(textTag.itertext()).strip()
            if is_invalid_line(all_text):
                continue

            line_counter += 1

            if is_merged_date(all_text):
                splited_line = parse_date(all_text)
                flight.append(splited_line[0])
                flight.append(splited_line[1])
                line_counter += 1
            elif line_counter > 1 and is_double_line(previous_line_tag, textTag):
                double_line_text = flight[line_counter - 2] + all_text
                flight[line_counter - 2] = double_line_text
                line_counter -= 1
            else:
                flight.append(all_text)

            if line_counter == 7:  # 7 informacoes sao uma linha
                line_counter = 0
                save_line_to_db(flight, xml)
                del flight[:]

            previous_line_tag = textTag


# 2013 tem formato diferente, e AERONAVE usa font[1]
# olhar /2014/Janeiro/20140122_174018.pdf.xml
def get_year_folder():
    years = ['2016', '2015', '2014']
    for year in years:
        year_dir = '%s/%s/**/*.pdf.xml' % (os.getcwd(), year)
        parse_xml(glob(year_dir))
        close_db()


def check_for_error(root, xml):  # ver a necessidade
    counter_for_share_flight = 0
    if counter_for_share_flight == 0:
        zero_font = root.findall("*/text[@font='0']")
        for textTag in zero_font:
            all_text = "".join(textTag.itertext())
            if "AERONAVE" in all_text:
                print("error? [ {0} ]".format(xml))


get_year_folder()
