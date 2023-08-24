import csv
from itertools import zip_longest
import re

def good_format_for_numbers(csv_file):

    csv_content = ''
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        csv_content = file.read()

    pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(?(доб.)?\s*(\d+)?\)?"
    pattern_replace = r"+7(\2)\3-\4-\5 \6\7"

    result = re.sub(pattern, pattern_replace, csv_content)

    def strip_phone(match):
        return match.group().strip()

    stripped_result = re.sub(r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2} (доб.\d+)?', strip_phone, result)

    with open('phonebook_raw_with_correct_numbers.csv', 'w', newline='', encoding='utf-8') as file:
        file.write(stripped_result)

def correct_location_of_names(contact_list):
    updated_contacts_list = contact_list[:1]

    for contact in contacts_list[1:]:
        lastname = ''
        firstname = ''
        surname = ''

        if len(contact[0].split(' ')) == 3:
            lastname = contact[0].split(' ')[0]
            firstname = contact[0].split(' ')[1]
            surname = contact[0].split(' ')[2]
        elif len(contact[0].split(' ')) == 1 and len(contact[1].split(' ')) == 2:
            lastname = contact[0]
            firstname = contact[1].split(' ')[0]
            surname = contact[1].split(' ')[1]
        elif len(contact[0].split(' ')) == 2:
            lastname = contact[0].split(' ')[0]
            firstname = contact[0].split(' ')[1]
            surname = ''
        else:
            lastname = contact[0]
            firstname = contact[1]
            surname = contact[2]

        updated_contact = [lastname, firstname, surname] + contact[3:]
        updated_contacts_list.append(updated_contact)

    return updated_contacts_list


def merge_extra_rows(contacts_list):
    updated_contacts_list = contacts_list[:1]
    isextra = False
    for contact_1 in contacts_list[1:]:
        for sub_list in updated_contacts_list:
            if (contact_1[0] == sub_list[0]) and (contact_1[1] == sub_list[1]):
                isextra = True
                break
        if not isextra:
            updated_contacts_list.append(contact_1)
        isextra = False
        contacts_list.pop(0)
        for contact_2 in contacts_list[1:]:
            if (contact_1[0] == contact_2[0]) and (contact_1[1] == contact_2[1]):
                updated_contacts_list[-1] = [x or y for x, y in zip_longest(updated_contacts_list[-1], contact_2, fillvalue='')]
    return updated_contacts_list



if __name__ == '__main__':

    good_format_for_numbers('phonebook_raw.csv')

    with open("phonebook_raw_with_correct_numbers.csv", encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    corrected_contact_list = merge_extra_rows(correct_location_of_names(contacts_list))

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')

        datawriter.writerows(corrected_contact_list)