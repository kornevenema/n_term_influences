import sys
import os
import csv
import pandas as pd


def check_dir(argv):
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
    else:
        print('directories not found')
    return path_to_results


def create_csv(path_to_results):
    if os.path.isfile('all_results.csv'):
        print("file already exists, remove 'all_results.csv' to create new file with name 'all_results.csv'")
        exit(0)
    else:
        directories = ['havo_grades', 'vmbo_grades', 'vwo_grades']
        with open("all_results.csv", 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(['SCHOOLJAAR',
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
                for file in list_of_dir:
                    if directory == 'vmbo_grades':
                        with open(cur_dir + file, 'r', newline='') as csv_file:
                            data = csv.reader(csv_file, delimiter=';')
                            next(data)
                            for row in data:
                                degree = [row[8] + ' ' + row[9]]
                                if 'VMBO GL' in degree or 'VMBO TL' in degree:
                                    degree = ["VMBO GL en TL"]
                                new_row = row[0:8] + degree + row[10:]
                                writer.writerow(new_row)
                            print('good new_row')
                    else:
                        with open(cur_dir + file, 'r', newline='') as csv_file:
                            data = csv.reader(csv_file, delimiter=';')
                            row1 = next(data)
                            writer.writerows(data)
                            print('good')


def remove_non_n_term_exams():
    exceptions = ['LNO', 'bouw', 'ict',
                  'consumptief', 'administratie', 'elektrotechniek',
                  'handel', 'haven', 'horeca', 'tech', 'commercie',
                  'sport', 'rijn', 'ektro', 'produceren', 'zorg',
                  'media', 'dienst', 'ondernemen', 'groen']
    with open('all_results_filtered.csv', 'w', newline='') as result:
        writer = csv.writer(result, delimiter=";")
        with open('all_results.csv', 'r') as f:
            lines = csv.reader(f, delimiter=';')
            for line in lines:
                if str(line[20]) != ',0' \
                        and str(line[20]) != '0' \
                        and str(line[20]) != '0,0' \
                        and str(line[23]) != ',0' \
                        and not any(s in str(line[11]) for s in exceptions):
                    writer.writerow(line)
                else:
                    pass


def clear_course_name():
    with open('all_results_filtered2.csv', 'w', newline='') as result:
        writer = csv.writer(result, delimiter=";")
        with open('all_results_filtered.csv', 'r') as f:
            lines = csv.reader(f, delimiter=';')
            for line in lines:
                prev = [line[0], line[7], line[8]]
                course = str(line[11])
                after = [line[21], line[22]]
                course = course.replace('HAVO', '')
                course = course.replace('VWO', '')
                course = course.replace('GL en TL', '')
                course = course.replace('KB', '')
                course = course.replace('BB', '')
                course = course.replace('(bezem)', '')
                course = course.replace('bezem', '')
                course = course.replace('(pilot)', '')
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
                new_line = prev + [course] + after
                writer.writerow(new_line)


def main(argv):
    # path_to_results = check_dir(argv)
    # create_csv(path_to_results)
    remove_non_n_term_exams()
    clear_course_name()








    df = pd.read_csv(
        r"C:\Users\korne\PycharmProjects\n_term_influences\pre-processing data\exam results\all_results_filtered2.csv",
        sep=';')
    df2 = pd.read_csv(r"C:\Users\korne\PycharmProjects\n_term_influences\pre-processing data\n-term\n-terms_filtered.csv",
                      sep=';')
    set_of_courses1 = {item for item in df['VAKNAAM']}
    set_of_courses2 = {item for item in df2['COURSE_NAME']}
    new_set = set()
    for item in set_of_courses1:
        # item = item.replace('HAVO', '')
        # item = item.replace('VWO', '')
        # item = item.replace('GL en TL', '')
        # item = item.replace('KB', '')
        # item = item.replace('BB', '')
        # item = item.replace('(bezem)', '')
        # item = item.replace('bezem', '')
        # item = item.replace('(pilot)', '')
        # item = item.replace('&', 'en')
        new_set.add(item.strip())
    new_set = sorted(new_set)

    with open('test4.txt', 'w') as f:
        for item in new_set:
            print(item, file=f, end='\n')




if __name__ == "__main__":
    main(sys.argv)