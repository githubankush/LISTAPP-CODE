import re
def split_alphanumeric(word):
    letters = ''.join(filter(str.isalpha, word))
    numbers = ''.join(filter(str.isdigit, word))

    if word:
        first_type = "letter" if word[0].isalpha() else "number"
    else:
        first_type = "unknown"

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
    pack_types = ['TAB', 'TABLET', 'INJECTION', 'CAP', 'CAPSULE', 'T']

    pack_name = []
    power = ''
    power_type = ''
    pack_type = ''
    pack_size = ''

    i = 0
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


    while i < len(words):
        next_word = words[i]
        if is_number(next_word):
            if  power == '' and pack_type == '' and power_type == '':
                power = next_word
                i += 1
            else:
                pack_size = next_word
                i +=1
        elif any(char.isdigit() for char in next_word):
            letters, numbers, first_type = split_alphanumeric(next_word)
            if first_type == "number":
                #for pack size (1*10), (1X10)
                if re.match(r'\d+[Xx*]\d+', next_word):
                    pack_size = next_word
                    i += 1
                    continue
                #for pack size (60K)
                # if re.match(r'\d+[Kk]', next_word):
                #     pack_size = next_word
                #     i += 1
                #     continue
                if letters in power_types:
                    power_type = letters
                    power = numbers
                    i +=1
                elif letters in pack_types:
                    pack_type = letters
                    pack_size = numbers
                    i += 1
                else:
                    pack_name.append(next_word)
                    i  += 1
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

                elif not next_word.isdigit():
                    pack_name.append(next_word)
                    i += 1

                else:
                    # next_word.replace(" ", "")
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
            i +=1
            continue

        else:
            i += 1

    pack_name = ' '.join(pack_name).strip()

    info = {
        'pack_name': pack_name,
        'power': power,
        'power_type': power_type,
        'pack_size': pack_size,
        'pack_type': pack_type,
    }

    return info

strings = [
     "D GAIN (NANO)",
    "D GAIN 1K SOFTGEL",
    "D GAIN 15 20",
    "D GAIN 60 K 1X4 softgel CAP",
    "D GAIN 60K CAP",
    "D GAIN 60K SOFTGEL",
    "D GAIN CAPSULE",
    "D GAIN SACHET",
    "D GAIN SACHET 1GM",
    "D GAIN SYR",
    "BRIVAZEN 25",
    "BRIVAZEN 25 10TAB",
    "BRIVAZEN 25 MG",
    "BRIVAZEN 25 TAB",
    "BRIVAZEN 25 TAB",
    "BRIVAZEN 25 TAB 1*10",
    "BRIVAZEN 25MG TAB",
]

print("| {:<30} | {:<25} | {:<6} | {:<10} | {:<9} | {:<10} |".format(
    "Original strings", "pack_name", "power", "power_type", "pack_size", "pack_type"))
print("|--------------------------------|---------------------------|--------|------------|-----------|------------|")

for s in strings:
    medicine_info = process_info(s)
    print("| {:<30} | {:<25} | {:<6} | {:<10} | {:<9} | {:<10} |".format(
        s, medicine_info['pack_name'], medicine_info['power'], medicine_info['power_type'],
        medicine_info['pack_size'], medicine_info['pack_type']))

