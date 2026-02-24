import re
import argparse


NAME_PATTERN = r'^[А-ЯЁ][а-яё]+$'


def is_valid_name(value: str) -> bool:
    return re.fullmatch(NAME_PATTERN, value) is not None


def main():
    parser = argparse.ArgumentParser(description="Lab 1 Variant 21")
    parser.add_argument("filename", type=str, help="Input file name")
    args = parser.parse_args()

    result = []

    try:
        with open(args.filename, "r", encoding="utf-8") as file:
            surname = None
            name = None

            for line in file:
                line = line.strip()

                match_surname = re.match(r'^Фамилия:\s*(.+)$', line)
                if match_surname:
                    surname = match_surname.group(1)
                    continue

                match_name = re.match(r'^Имя:\s*(.+)$', line)
                if match_name:
                    name = match_name.group(1)

                if surname and name:
                    if is_valid_name(surname) and is_valid_name(name):
                        result.append(f"{surname} {name[0]}.")
                    surname = None
                    name = None

    except FileNotFoundError:
        print("Файл не найден")
        return

    result.sort()

    with open("lab1_var21_output.txt", "w", encoding="utf-8") as out:
        for item in result:
            out.write(item + "\n")

    print(f"Найдено корректных записей: {len(result)}")
    for item in result:
        print(item)


if __name__ == "__main__":
    main()