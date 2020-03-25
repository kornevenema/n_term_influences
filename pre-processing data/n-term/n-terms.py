import requests
import csv
import json
from bs4 import BeautifulSoup


def create_csv(config):
    """
    creates a csv file with all the n-terms of all high school exams
    in the Netherlands from the years 2012 to 2019.
    :param config:
    :return:
    """
    list_of_links = []
    for degree in config['degrees']:
        with open('links_to_n-terms/' + degree + '.txt', "r") as f:
            list_of_links += [line.strip() for line in f.readlines()]

    with open('n-terms.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['YEAR', 'DEGREE', 'NUMBER', 'COURSE_NAME', 'LENGTH_SCORE_SCALE', 'N-TERM'])

        for link in list_of_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            h1 = soup.find('h1').text
            year = h1.split()[-1]
            if int(year) in config['years']:
                list_of_table = []
                degree = ""
                if "vmbo bb" in h1.lower():
                    degree = "VMBO BB"
                elif "vmbo kb" in h1.lower():
                    degree = "VMBO KB"
                elif "vmbo gl en tl" in h1.lower():
                    degree = "VMBO GL en TL"
                elif "havo" in h1.lower():
                    degree = "HAVO"
                elif "vwo" in h1.lower():
                    degree = "VWO"
                for tr in soup.findAll("tr"):
                    row = [year, degree]
                    for td in tr.findAll("td"):
                        row.append(td.text)
                    list_of_table.append(row)
                list_of_table.pop(0)
                writer.writerows(list_of_table)
    print("'n-terms.csv' created")


def filter_n_terms():
    """
    filters all the n-terms from the file 'n-terms.csv'.
    This includes exams that are practical and thus use no n-term. (0 given)
    It also renames the course_name so that it matches the course_name from the results.
    It also removes unnecessary columns.
    :return:
    """
    lines = csv.reader(open('n-terms.csv', 'r'), delimiter=';')
    next(lines)
    exceptions = ['CBT', 'CPE', 'bezem', 'oud', 'ExamenTester', 'pilot']

    with open('n-terms_filtered.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['YEAR', 'DEGREE', 'COURSE_NAME', 'LENGTH_SCORE_SCALE', 'N-TERM'])
        for line in lines:
            course = str(line[3])
            n_term = str(line[5])
            if not any(s in course for s in exceptions):
                if "HAVO kunst" in course:
                    course = 'kunst'
                elif 'VWO kunst' in course:
                    course = 'kunst'
                course = course.replace(' (nieuwe examenprogramma)', '')
                course = course.replace(' (nieuwe examnprogramma)', '')
                course = course.replace(' en staatsinrichting', '')
                course = course.replace(' met audio-cd', '')
                course = course.replace('&', 'en')
                course = course.replace('BB', '')
                course = course.replace('KB', '')
                course = course.replace('GL en TL', '')
                course = course.replace('HAVO', '')
                course = course.replace('VWO', '')
                course = course.replace('CSE', '')
                course = course.replace('Latijnse taal en cultuur', 'Latijn')
                course = course.replace('Griekse taal en cultuur', 'Grieks')
                course = course.strip()
                n_term = float(n_term.replace(',', '.'))
                new_line = [int(line[0]), str(line[1]), course, int(line[4]), n_term]
                writer.writerow(new_line)
    print("'n-terms_filtered.csv' created")


def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    create_csv(config)
    filter_n_terms()


if __name__ == "__main__":
    main()
