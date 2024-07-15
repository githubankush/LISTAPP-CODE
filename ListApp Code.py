import re
import mysql.connector
from mysql.connector import Error

def split_alphanumeric(word):
    letters = ''.join(filter(str.isalpha, word))
    numbers = ''.join(filter(str.isdigit, word))
    first_type = "letter" if word and word[0].isalpha() else "number" if word else "unknown"
    return letters, numbers, first_type

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def process_info(medicine_info):
    words = medicine_info.split()
    power_types = ['MG', 'GM', 'ML']
    pack_types = ['TAB', 'TABLET', 'INJECTION', 'CAP', 'CAPSULE',]

    pack_name = []
    power = ''
    power_type = ''
    pack_type = ''
    pack_size = ''
    other = ''

    i = 0

    # Loop for pack_name
    while i < len(words):
        word = words[i]
        if i == 0 and word.isdigit():
            pack_name.append(word)
            i += 1
            continue
        elif i == 0 and any(char.isdigit() for char in word):
            pack_name.append(word)
            i += 1
            continue
        elif any(char.isdigit() for char in word):
            break
        elif word.isdigit():
            break
        elif word in pack_types:
            pack_type = word
            i += 1
        elif word in power_types:
            power_type = word
            i += 1
        else:
            if pack_type == '' or pack_size == '' or power_type == '' or power == '':
                pack_name.append(word)
                i += 1

    # Loop for all other fields
    while i < len(words):
        next_word = words[i]
        if is_number(next_word):
            if power == '' and pack_type == '' and power_type == '':
                power = next_word
                i += 1
            else:
                pack_size += ' ' + next_word
                i += 1
        elif any(char.isdigit() for char in next_word):
            letters, numbers, first_type = split_alphanumeric(next_word)
            if first_type == "number":
                if re.match(r'\d+[Xx*]\d+', next_word):
                    pack_size = next_word
                    i += 1
                    continue
                if letters in power_types:
                    power_type = letters
                    power = numbers
                    i += 1
                elif letters in pack_types:
                    pack_type = letters
                    pack_size = numbers
                    i += 1
                else:
                    pack_name.append(next_word)
                    i += 1
                    continue
            elif first_type != "number":
                if letters in power_types:
                    power_type = letters
                    pack_size = numbers
                    i += 1
                elif letters in pack_types:
                    pack_type = letters
                    pack_size = numbers
                    i += 1
                # elif not next_word.isdigit():
                #     pack_name.append(next_word)
                #     i += 1
                else:
                    pack_name.append(next_word)
                    i += 1
                    continue

        elif next_word in power_types:
            power_type = next_word
            i += 1

        elif next_word in pack_types:
            pack_type = next_word
            i += 1

        elif power == '' and power_type == '' and pack_size == '' and pack_type == '':
            pack_name.append(next_word)
            i += 1
            continue

        else:
            other   += ' ' + next_word
            i += 1


    pack_name = ' '.join(pack_name).strip()

    info = {
        'pack_name': pack_name,
        'power': power,
        'power_type': power_type,
        'pack_size': pack_size,
        'pack_type': pack_type,
        'other': other,
    }

    return info
#mapping
def map_strings(string1, string2):
    info1 = process_info(string1)
    info2 = process_info(string2)

    if (info1['pack_name'] == info2['pack_name'] and
            info1['power'] == info2['power'] and
            info1['pack_type'] == info2['pack_type'] and info1['other'] == info2['other']):

        if info1['power_type'] and info2['power_type']:
            if info1['power_type'] != info2['power_type']:
                return (string1, string2, 'No')
        else:
            return (string1, string2, 'Yes')
    return (string1, string2, 'No')

# Test with example strings
# strings = [
#     "BRIVAZEN 25",
#     "BRIVAZEN 25 10TAB",
#     "BRIVAZEN 25 MG",
#     "BRIVAZEN 25 TAB",
#     "BRIVAZEN 25 TAB FORTE",
#     "BRIVAZEN 25 FORTE TAB",
#     "BRIVAZEN 25 15 TAB FORTE SR",
#     "BRIVAZEN 25 TAB 15 FORTE",
#     "BRIVAZEN 25 TAB FORTE 15",
#     "BRIVAZEN 25 TAB 1*10",
#     "BRIVAZEN 25MG TAB",
#     "CROCIN 150MG TAB 10 PR",
#     "AVVA 250 MG TABLET SR",
#     "CALINTA D3 TAB 15 S",
#     "CROCIN 150MG TAB",
#     "CROCIN 150MG TAB PR",
#     "EPOFIT 1000 TV PREFILLED SYRINGE 1X15 10 TABLET",
#    "CHYMOTAS FORT TA",
#     "CHYMOTAS FORTE 20 TAB",
#     "CHYMOTAS FORTE 20 TAB",
#     "CHYMOTAS FORTE 20T",
#     "CHYMOTAS FORTE B/L",
#     "CHYMOTAS FORTE TAB",
#     "CHYMOTAS FORTE TAB",
#     "CHYMOTAS FORTE TAB",
#     "CHYMOTAS FORTE TABLET",
#     "CHYTROZYM 20",
#     "CHYTROZYM 20 20T",
#     "CHYTROZYM TAB",
#     "CIFLOX 250 TAB",
#     "CIFLOX 250MG TABLET",
#     "CLONIL 75 MG TABLET SR",
#     "CLONIL 75 SR",
#     "CLONIL 75 SR",
#     "CLONIL 75 SR",
#     "CLONIL 75 SR 10T",
#     "CLONIL 75 SR 15T",
#     "CLONIL 75 SR TAB",
#     "CLONIL 75 SR TAB",
#     "CLONIL 75MG SR TAB",
#     "CLONIL SR 50 TABLET",
#     "CLONIL SR 75",
#     "CLONIL SR 75 TAB",
#     "CLONIL SR 75 TAB",
#     "CLONIL SR 75 TAB INTAS",
#     "CLONIL SR 75 TABLET",
#     "CLOZEMA 0.05% CREAM",
#     "CLOZEMA CREAM",
#     "CLOZEMA GM CREAM",
#     "CLOZEMA GM CREAM",
#     "CNAC EYE DROPS 10ML",
#     "CNE SOAP",
#     "CNO CREAM",
#     "COBAFAST FORTE CAP",
#     "COF Q TAB TAB",
# ]

# print("| {:<30} | {:<25} | {:<6} | {:<10} | {:<9} | {:<10} | {:<20}".format(
#     "Original strings", "pack_name", "power", "power_type", "pack_size", "pack_type", "other"))
# print("|--------------------------------|---------------------------|--------|------------|-----------|------------|---------------|")
# #
# for s in strings:
#     medicine_info = process_info(s)
#     print("| {:<30} | {:<25} | {:<6} | {:<10} | {:<9} | {:<10} | {:<20}".format(
#         s, medicine_info['pack_name'], medicine_info['power'], medicine_info['power_type'],
#         medicine_info['pack_size'], medicine_info['pack_type'],medicine_info['other']))

# status_list = [map_strings(strings[i], strings[j]) for i in range(len(strings)) for j in range(i + 1, len(strings))]
#
# print("\n| {:<30} | {:<30} | {:<6} |".format("Original Strings", "Mapped Strings", "Status"))
# print("|--------------------------------|--------------------------------|--------|")
#
# for status in status_list:
#     print("| {:<30} | {:<30} | {:<6} |".format(status[0], status[1], status[2]))

# Database connection and processing
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='listapp_db',
        port=3306
    )
    cur = connection.cursor()


    column_name = 'denotion'
    select_query = f"SELECT * FROM m16j_demo_poducts_1 WHERE {column_name} = ''"
    cur.execute(select_query)
    records = cur.fetchall()

    for record in records:
        product_id = record[0]
        product_name = record[1]

        info = process_info(product_name)
        pack_name = info['pack_name']

        search_query = f"""
            SELECT *
            FROM m16j_demo_poducts_1
            WHERE product_name LIKE %s
            AND product_id != %s
        """
        cur.execute(search_query, (f"%{pack_name}%", product_id))
        similar_records = cur.fetchall()
        # print(similar_records)

        exact_map = []
        for similar_record in similar_records:
        #similar_product_id = similar_record[0]
            similar_product_name = similar_record[1]
            # print( similar_product_name)
            result = map_strings(product_name,similar_product_name)
            if result[2] == 'Yes':
                # print(similar_record)
                # break
                exact_map.append(similar_record)

        for i in exact_map:
            print(product_name, " - ",i[1])

            # print(f"Product ID: {product_id}, Product Name: {product_name}")
            # print(f"Similar Product ID: {product_id}, Similar Product Name: {similar_product_name}")

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cur.close()
        connection.close()
