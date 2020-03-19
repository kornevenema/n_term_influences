import requests
from bs4 import BeautifulSoup
import csv
import os.path
import json


def get_links(file):
    with open(file, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_table(soup):
    list_of_table = []
    h1 = soup.h1.text
    words = h1.split()
    year = words[-1]
    degree = ""
    if "vmbo BB" in h1:
        degree = "vmbo BB"
    if "vmbo KB" in h1:
        degree = "vmbo KB"
    if "vmbo GL en TL" in h1:
        degree = "vmbo GL en TL"
    if "havo" in h1.lower():
        degree = "havo"
    if "vwo" in h1.lower():
        degree = "vwo"

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


if __name__ == "__main__":
    main()
