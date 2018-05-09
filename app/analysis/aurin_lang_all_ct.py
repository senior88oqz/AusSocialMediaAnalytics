import json
import sys
import csv


def main(argv):
    format_output = {}
    with open("data/lang_mel.csv", 'rb') as csvfile:
        count = 0
        temp_lang_dict = {}
        data = csv.reader(csvfile)
        list_data = list(data)
        for i in range(len(list_data[0])):
            if count < 10:
                temps = str(list_data[0][i]).split('_')
                if temps[len(temps) - 1] == "tot" and temps[len(temps) - 2] != 'oth':
                    temp_lang_dict[temps[len(temps) - 2].title()] = list_data[1][i]
                    count += 1
        format_output["Melbourne"] = temp_lang_dict

    with open("data/lang_syd.csv", 'rb') as csvfile:
        count = 0
        temp_lang_dict = {}
        data = csv.reader(csvfile)
        list_data = list(data)
        for i in range(len(list_data[0])):
            if count < 10:
                temps = str(list_data[0][i]).split('_')
                if temps[len(temps) - 1] == "tot" and temps[len(temps) - 2] != 'oth':
                    temp_lang_dict[temps[len(temps) - 2].title()] = list_data[1][i]
                    count += 1
        format_output["Sydney"] = temp_lang_dict

    with open("data/lang_brisbane.csv", 'rb') as csvfile:
        count = 0
        temp_lang_dict = {}
        data = csv.reader(csvfile)
        list_data = list(data)
        for i in range(len(list_data[0])):
            if count < 10:
                temps = str(list_data[0][i]).split('_')
                if temps[len(temps) - 1] == "tot" and temps[len(temps) - 2] != 'oth':
                    temp_lang_dict[temps[len(temps) - 2].title()] = list_data[1][i]
                    count += 1
        format_output["Brisbane"] = temp_lang_dict

    with open("data/lang_perth.csv", 'rb') as csvfile:
        count = 0
        temp_lang_dict = {}
        data = csv.reader(csvfile)
        list_data = list(data)
        for i in range(len(list_data[0])):
            if count < 10:
                temps = str(list_data[0][i]).split('_')
                if temps[len(temps) - 1] == "tot" and temps[len(temps) - 2] != 'oth':
                    temp_lang_dict[temps[len(temps) - 2].title()] = list_data[1][i]
                    count += 1
        format_output["Perth"] = temp_lang_dict

    with open("data/lang_adelaide.csv", 'rb') as csvfile:
        count = 0
        temp_lang_dict = {}
        data = csv.reader(csvfile)
        list_data = list(data)
        for i in range(len(list_data[0])):
            if count < 10:
                temps = str(list_data[0][i]).split('_')
                if temps[len(temps) - 1] == "tot" and temps[len(temps) - 2] != 'oth':
                    temp_lang_dict[temps[len(temps) - 2].title()] = list_data[1][i]
                    count += 1
        format_output["Adelaide"] = temp_lang_dict
    with open("result/aurin_lang_all_ct.json", 'w') as fp:
        json.dump(format_output, fp)

if __name__ == "__main__":
    main(sys.argv[1:])
