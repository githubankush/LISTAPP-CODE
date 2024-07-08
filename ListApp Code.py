def split_alphanumeric(word):
    letters = ''.join(filter(str.isalpha, word))
    numbers = ''.join(filter(str.isdigit, word))

    if word:
        first_type = "letter" if word[0].isalpha() else "number"
    else:
        first_type = "unknown"

    return letters, numbers, first_type


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
        if i == 0 and any(char.isdigit() for char in word):
            pack_name.append(word)
            i += 1
            continue
        if any(char.isdigit() for char in word):
            break
        if word.isdigit():
            break
        elif word in pack_types:
            pack_type = word
            i += 1
        elif word in power_types:
            power_type = word
            i += 1
        else:
            pack_name.append(word)
            i += 1

    if i < len(words):
        next_word = words[i]
        if next_word.isdigit():
            if pack_type == '' and power_type == '':
                power = next_word
                i += 1
            else:
                pack_size = next_word
        elif any(char.isdigit() for char in next_word):
            letters, numbers, first_type = split_alphanumeric(next_word)
            if first_type == "number":
                power = numbers
                if letters in power_types:
                    power_type = letters
                elif letters in pack_types:
                    pack_type = letters
                i += 1
            elif first_type != "number":
                if letters in power_types:
                    power_type = letters
                    i += 1
                elif letters in pack_types:
                    pack_type = letters
                    pack_size = numbers
                    i += 1
                else:
                    next_word.replace(" ", "")
                    pack_name.append(next_word)
                    i += 1

        elif i < len(words):
            next_word = words[i]
            if next_word in power_types:
                power_type = next_word
                i += 1

            elif next_word in pack_types:
                pack_type = next_word
                i += 1

    # another case
    if i < len(words):
        if power != '':
            next_word = words[i]
            if any(char.isdigit() for char in next_word):
                letters, numbers, first_type = split_alphanumeric(next_word)
                if first_type == "number":
                    pack_size = numbers
                    if letters in pack_types:
                        pack_type = letters
                        i += 1
                elif first_type != "number":
                    if letters in pack_types:
                        pack_type = letters
                        pack_size = numbers
                        i += 1

    for word in words[i:]:
        if any(pt in word for pt in power_types):
            power_type = word

        elif any(pt in word for pt in pack_types):
            pack_type = word
        elif any(char.isdigit() for char in word):
            if pack_type == '':
                power = word
            elif power_type != '':
                pack_size = ''.join(filter(str.isdigit, word))
        else:
            pack_name.append(word)

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
    "ARVAST A75 CAPSULE",
    "ALTRACIROL 100ML",
    "ALZIL 10MG TAB",
    "AMANTEX 100MG TAB",
    "ALBIUM 10MG TABLET",
    "AMTAS M 25MG",
    "AMTAS TAB10",
    "AMTAS HT 10 TAB",
    "ANDRE PLUS 10ML",
    "ZYLENO FORTE CAPSULE",
    "ZAXPAM 15MG TAB",
    "AXEPTA 40 MG",
    "ZUBITIN TAB 30",
    "ZCILNY 10 TAB",
    "ZEN 200 MG TABLET",
    "ZENOXA 450 10T",
    "ZENOXA TAB 450",
    "ZENOXA 300 10T",
    "ZENOXA OD 150MG TAB",
    "ZENOXA OD 300 MG TABLET",
    "ABAXIS 2.5 TAB",
    "3 D PLUS TAB 10 TAB",
    "3D FLAM 25 MG INJECTION",
    "3D FLAM INJ 3ML",
    "ZORYL10 MG",
    "ZOREP 2MG TAB",
    "ZONALTA 8MG TAB TAB",
    "ZINSYP 60ML",
    "ZITASPOR CAP",
    "ZLEVERA 250",
    "ZLIPICURE 10 TAB",
    "ZLIPICURE TG TAB",
    "ZLIPITAS 10 TAB",
    "ZMORR F SOLUTION 60ML",
    "ZODOX",
    "ZODOX 10 VIAL INJ",
    "ZODOX 10MG INJECTION",
    "ZODOX 50 MG",
    "ZODOX 50 VIAL INJ",
    "ZODOX 50MG INJECTION",
    "ZOLASTA",
    "ZOLASTA",
    "ZOLASTA 4 MG INJECTION",
    "ZOLASTA 4GM VAIL",
    "ZOLASTA 4MG INJ 10ML INJ",
    "ZOLASTA INJ VAIL",
    "ZOLASTA SINGLE",
    "ZOLAX .25 TAB",
    "ZOLAX .5 TAB",
    "ZOLAX 0.25 10TAB",
    "ZOLAX 0.25 MG TABLET",
    "ZOLAX 0.25 MG TABLET SR",
    "ZOLAX 0.25 TAB",
    "ZOLAX 0.25MG TAB",
    "ZOLAX 0.5 10TAB",
    "ZOLAX 0.5 MG TABLET",
    "ZOLAX 0.5 MG TABLET SR",
    "ZOLAX 0.5MG TAB",
    "ZOLAX 025",
    "ZOLAX 05",
    "ZOLAX 1 MG TABLET",
    "ZOLAX 1 MG TABLET SR",
    "ZOLAX 1 TAB",
    "ZOLAX 1.5 MG TABLET",
    "ZOLAX SR .1 TABLET",
]


print("| {:<25} | {:<6} | {:<10} | {:<9} | {:<10} |".format(
    "pack_name", "power", "power_type", "pack_size", "pack_type"))
print("|---------------------------|--------|------------|-----------|------------|")


for s in strings:
    medicine_info = process_info(s)
    print("| {:<25} | {:<6} | {:<10} | {:<9} | {:<10} |".format(
        medicine_info['pack_name'], medicine_info['power'], medicine_info['power_type'],
        medicine_info['pack_size'], medicine_info['pack_type']))

