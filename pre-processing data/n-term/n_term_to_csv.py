import requests
import csv
import os.path
import json
from bs4 import BeautifulSoup


def get_links(file):
    with open(file, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_table(soup):
    list_of_table = []
    h1 = soup.h1.text
    words = h1.split()
    year = words[-1]
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
    return list_of_table[1:]


def create_csv(file_name):
    if os.path.isfile(file_name):
        print("file already exists, remove '" + file_name + "' to create new file with name '" + file_name + "'")
        exit(0)
    else:
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(['YEAR', 'DEGREE', 'NUMBER', 'COURSE_NAME', 'LENGTH_SCORE_SCALE', 'N-TERM'])


def append_data_to_csv(file_name, data):
    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(data)


def create_filtered_csv():
    with open('n-terms_filtered.csv', 'w', newline='') as result:
        writer = csv.writer(result, delimiter=";")
        with open('n-terms.csv', 'r') as f:
            data = csv.reader(f, delimiter=';')
            for line in data:
                if 'CBT' in str(line[3]):
                    pass
                elif 'CPE' in str(line[3]):
                    pass
                elif 'bezem' in str(line[3]):
                    pass
                elif 'oud' in str(line[3]):
                    pass
                elif 'ExamenTester' in str(line[3]):
                    pass
                elif 'pilot' in str(line[3]):
                    pass
                else:
                    if "HAVO kunst" in str(line[3]):
                        line[3] = 'kunst'
                    elif 'VWO kunst' in str(line[3]):
                        line[3] = 'kunst'
                    line[3] = str(line[3].replace(' (nieuwe examenprogramma)', ''))
                    line[3] = str(line[3].replace(' (nieuwe examnprogramma)', ''))
                    line[3] = str(line[3].replace(' en staatsinrichting', ''))
                    line[3] = str(line[3].replace(' met audio-cd', ''))
                    line[3] = str(line[3].replace('&', 'en'))
                    line[3] = str(line[3].replace('BB', ''))
                    line[3] = str(line[3].replace('KB', ''))
                    line[3] = str(line[3].replace('GL en TL', ''))
                    line[3] = str(line[3].replace('HAVO', ''))
                    line[3] = str(line[3].replace('VWO', ''))
                    line[3] = str(line[3].replace('CSE', ''))
                    line[3] = str(line[3].replace('Latijnse taal en cultuur', 'Latijn'))
                    line[3] = str(line[3].replace('Griekse taal en cultuur', 'Grieks'))
                    line[3] = str(line[3].strip())
                    writer.writerow(line)


def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    create_csv("n-terms.csv")

    for file in config['degrees']:
        file = "links_to_n-terms/" + file + ".txt"
        list_of_links = get_links(file)

        for link in list_of_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            for h1 in soup.findAll('h1'):
                words = h1.text.split()
                year = words[-1]
                if int(year) in config['years']:
                    table = get_table(soup)
                    append_data_to_csv("n-terms.csv", table)

    create_filtered_csv()


if __name__ == "__main__":
    main()
