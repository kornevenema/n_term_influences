import sys
import os
import csv
import urllib.request
import json


def create_dir(config):
    """
    create all the needed directories and download all the data.
    :param config:
    :return:
    """
    if not os.path.exists('results'):
        os.makedirs('results')
        if any('VMBO' in degree for degree in config['degrees']):
            os.makedirs('results\\vmbo_grades')
            with open('links_to_results/vmbo.txt', "r") as f:
                list_of_links = [line.strip() for line in f.readlines()]
                for link, year in zip(list_of_links, config['years']):
                    if str(year-1) + "-" + str(year) in str(link):
                        urllib.request.urlretrieve(link, "results\\vmbo_grades\\vmbo" + str(year) + ".csv")
            print('created vmbo data')

        if any('HAVO' in degree for degree in config['degrees']):
            os.makedirs('results\\havo_grades')
            with open('links_to_results/havo.txt', "r") as f:
                list_of_links = [line.strip() for line in f.readlines()]
                for link, year in zip(list_of_links, config['years']):
                    if str(year - 1) + "-" + str(year) in str(link):
                        urllib.request.urlretrieve(link, "results\\havo_grades\\havo" + str(year) + ".csv")
            print('created havo data')

        if any('VWO' in degree for degree in config['degrees']):
            os.makedirs('results\\vwo_grades')
            with open('links_to_results/vwo.txt', "r") as f:
                list_of_links = [line.strip() for line in f.readlines()]
                for link, year in zip(list_of_links, config['years']):
                    if str(year - 1) + "-" + str(year) in str(link):
                        urllib.request.urlretrieve(link, "results\\vwo_grades\\vwo" + str(year) + ".csv")
            print('created vwo data')
    else:
        print('directory "results" already exist, remove to create new directory.')



def check_dir(argv):
    """
    check if the given directory contains the directories containing all the links needed.
    if no path given (if len(argv)==1) assume it is in the current directory.

    :param argv:
    :return:
    """
    if len(argv) == 2:
        path_to_results = argv[1] + "\\results"
    else:
        path_to_results = ".\\results"

    if os.path.isdir(path_to_results):
        if os.path.isdir(path_to_results + "\\havo_grades") \
                and os.path.isdir(path_to_results + "\\vwo_grades") \
                and os.path.isdir(path_to_results + "\\vmbo_grades"):
            print('all directories found')
        else:
            print('subdirectories not found')
            exit(0)
    else:
        print('directories not found')
        exit(0)

    return path_to_results


def create_csv(path_to_results):
    """
    creates a csv file with all the results of all high school students
    in the Netherlands from the years 2012 to 2019.
    :param path_to_results:
    :return:
    """
    directories = ['havo_grades', 'vmbo_grades', 'vwo_grades']
    with open("all_results.csv", 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            'SCHOOLJAAR',
            'BRIN NUMMER',
            'VESTIGINGSNUMMER',
            'INSTELLINGSNAAM VESTIGING',
            'GEMEENTENUMMER',
            'GEMEENTENAAM',
            'PLAATSNAAM',
            'PROVINCIE',
            'ONDERWIJSTYPE VO',
            'VAKCODE',
            'AFKORTING VAKNAAM',
            'VAKNAAM',
            'SCHOOLEXAMEN BEOORDELING',
            'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING',
            'AANTAL SCHOOLEXAMENS MET BEOORDELING MEETELLEND VOOR DIPLOMA',
            'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER',
            'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS',
            'AANTAL SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA',
            'GEM. CIJFER SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA',
            'TOTAAL AANTAL CENTRALE EXAMENS',
            'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS',
            'AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA',
            'GEM. CIJFER CENTRALE EXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA',
            'GEM. CIJFER CIJFERLIJST',
            'GEM. CIJFER REKENTOETS'])

        for directory in directories:
            cur_dir = path_to_results + '\\' + directory + '\\'
            list_of_dir = os.listdir(cur_dir)
            if directory == 'vmbo_grades':
                for file in list_of_dir:
                    with open(cur_dir + file, 'r', newline='') as csv_file:
                        data = csv.reader(csv_file, delimiter=';')
                        next(data)
                        for row in data:
                            degree = [row[8] + ' ' + row[9]]
                            if 'VMBO GL' in degree or 'VMBO TL' in degree:
                                degree = ["VMBO GL en TL"]
                            if 'VMBO BL' in degree:
                                degree = ["VMBO BB"]
                            if 'VMBO KL' in degree:
                                degree = ["VMBO KB"]
                            new_row = row[0:8] + degree + row[10:]
                            writer.writerow(new_row)
            else:
                for file in list_of_dir:
                    with open(cur_dir + file, 'r', newline='') as csv_file:
                        data = csv.reader(csv_file, delimiter=';')
                        next(data)
                        writer.writerows(data)
            print(directory, "appended to 'all_results.csv'")


def filter_results():
    """
    filters all the results from the file 'all_results.csv'.
    This includes courses that do not use n-terms.
    It also renames the course_name so that it matches the course_name from the n-terms.
    It also removes unnecessary columns.
    :return:
    """
    lines = csv.reader(open('all_results.csv', 'r'), delimiter=';')
    next(lines)
    exceptions = [
        'LNO', 'bouw', 'ict',
        'consumptief', 'administratie', 'elektrotechniek',
        'handel', 'haven', 'horeca', 'tech', 'commercie',
        'sport', 'rijn', 'ektro', 'produceren', 'zorg',
        'media', 'dienst', 'ondernemen', 'groen']
    with open('all_results_filtered.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['YEAR', 'DEGREE', 'COURSE_NAME', 'SCORE'])
        for line in lines:
            if not any(s in str(line[22]) for s in [',0', '0', '0,0']) \
                    and not any(s in str(line[11]) for s in exceptions) \
                    and str(line[23]) != ',0':
                prev = [int(line[0]) + 1, str(line[8])]
                course = str(line[11])
                score = str(line[22])
                score = float(score.replace(',', '.'))
                course = course.replace('HAVO', '')
                course = course.replace('VWO', '')
                course = course.replace('GL en TL', '')
                course = course.replace('KB', '')
                course = course.replace('BB', '')
                course = course.replace('&', 'en')
                course = course.replace('met kcv', '')
                course = course.replace('Latijnse taal en cultuur', 'Latijn')
                course = course.replace('Latijnse taal en literatuur', 'Latijn')
                course = course.replace('e taal en cultuur', '')
                course = course.replace('e taal en literatuur', '')
                course = course.replace(' en staatsinrichting', '')
                course = course.replace('e taal', '')
                course = course.replace('(oud)', '')
                course = course.replace('textiele vormgeving', 'xxxxxxxx')
                course = course.replace('tekenen', 'xxxxxxxx')
                course = course.replace('handvaardigheid', 'xxxxxxxx')
                course = course.replace('xxxxxxxx', 'tekenen, handvaardigheid, textiele vormgeving')
                course = course.replace('(algemeen)', '')
                course = course.replace('(beeldende vormgeving)', '')
                course = course.replace('(dans)', '')
                course = course.replace('(drama)', '')
                course = course.replace('(muziek)', '')
                course = course.replace('II', '2')
                course = course.replace('I', '1')
                if 'dans' in course:
                    course = 'dans'
                elif 'drama' in course:
                    course = 'drama'
                elif 'muziek' in course:
                    course = 'muziek'
                elif 'beeldende vakken' in course:
                    course = 'beeldende vakken'
                course = course.strip()
                new_line = prev + [course, score]
                writer.writerow(new_line)
    print("'all_results_filtered.csv' successfully created")


def add_more_results():
    with open('../n-term/n-terms_complete.csv', 'r') as csv_file:
        n_terms = csv.reader(csv_file, delimiter=';')
        n_terms = list(n_terms)
    lines = csv.reader(open('all_results_filtered.csv', 'r'), delimiter=';')
    next(lines)
    with open('all_results_complete.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['YEAR', 'DEGREE', 'COURSE_NAME', 'SCORE', 'SCORE_AVERAGE_N-TERM', 'SCORE_NO_N-TERM'])
        for line in lines:
            for n_term in n_terms[1:]:
                if n_term[0] == line[0] and n_term[1] == line[1] and n_term[2] == line[2]:
                    average_score = round(float(line[3]) + (float(n_term[4]) - float(n_term[3])), 1)
                    no_score = round(float(line[3]) + (float(n_term[5]) - float(n_term[3])), 1)
                    writer.writerow(line + [average_score, no_score])
                pass
        print("'all_results_complete.csv' successfully created")




def main(argv):
    with open('../../config.json', 'r') as f:
        config = json.load(f)
    create_dir(config)
    path = check_dir(argv)
    create_csv(path)
    filter_results()
    add_more_results()


if __name__ == "__main__":
    main(sys.argv)
