import requests
from bs4 import BeautifulSoup
import csv
import os.path


def get_links(file):
    with open(file, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_table(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    list_of_table = []
    for tr in soup.findAll("tr"):
        row = []
        for td in tr.findAll("td"):
            row.append(td.string)
        list_of_table.append(row)
    for th in soup.findAll("th"):
        list_of_table[0].append(th.string)
    return list_of_table


def create_csv(file_name):
    if os.path.isfile(file_name):
        print("file already exists")
    else:
        file_name = file_name + ".csv"
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(['NUMBER', 'DEGREE', 'COURSE_NAME', 'LENGTH_SCORE_SCALE', 'N-TERM'])


def append_data_to_csv(file_name, data):
    with open(file_name, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for row in data:
            writer.writerow(row)


def main():
    list_of_links = get_links("links_n-term_vmbo.txt")
    # table = get_table(list_of_links[0])
    # print(table[0])
    create_csv("n-terms")


if __name__ == "__main__":
    main()