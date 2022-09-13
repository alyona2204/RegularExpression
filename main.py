import csv
import operator
import itertools
import os
import re

def dict(file_name):
    dict = []
    with open(file_name, encoding="utf8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        keys = contacts_list[0]
        values = contacts_list[1:]
        for k, v in enumerate(values):
            dict.append({})
            for key, value in zip(keys, v):
                dict[k].update({key: value})
        return dict

def fio(in_file):
    dict_file = dict(in_file)
    for element in dict_file:
        name_split = element['lastname'].split(' ')
        if len(name_split) > 1:
            element['lastname'] = name_split[0]
            element['firstname'] = name_split[1]
            if len(name_split) > 2:
                element['surname'] = name_split[2]
        name_split = element['firstname'].split(' ')
        if len(name_split) > 1:
            element['firstname'] = name_split[0]
            element['surname'] = name_split[1]
    return dict_file

def phone_numbers(in_file, out_file):
    with open(in_file, encoding="utf8") as f:
        text = f.read()
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
        phone = re.sub(pattern, r'+7(\2)\3-\4-\5\6\7\8', text)
        with open(out_file, 'w+', encoding="utf8") as f:
            text = f.write(phone)

def for_name_element(person_name):
    list = ['firstname', 'lastname']
    group = operator.itemgetter(*list)
    person_name.sort(key=group)
    grouped_person = itertools.groupby(person_name, group)
    list_element = []
    for (firstname, lastname), element in grouped_person:
        list_element.append({'lastname': lastname, 'firstname': firstname})
        for el in element:
            element_of_list = list_element[-1]
            for key, value in el.items():
                if key not in element_of_list or element_of_list[key] == '':
                    element_of_list[key] = value
    return list_element

def in_file(file_name, dict):
    keys = list(dict[0].keys())
    with open(file_name, "w", encoding="utf8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(keys)
        for element in dict:
            datawriter.writerow(element.values())

def end():
    phone_numbers(in_file="phonebook_raw.csv", out_file="phone.csv")
    fio_name = fio(in_file="phone.csv")
    os.remove("phone.csv")
    names = for_name_element(fio_name)
    in_file("phonebook.csv", names)

if __name__ == '__main__':
    end()