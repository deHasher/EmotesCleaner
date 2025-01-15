import os
import json
import re
import ctypes
import random
import string
from colorama import Fore, Back, init


def unlink(filepath):
    os.remove(filepath)


def clear_trash(current_dir, name, new_name, format_element):
    image = os.path.join(current_dir, f"{name}.{format_element}")
    if os.path.exists(image):
        with open(image, "rb") as img_f:
            content = img_f.read()
        unlink(image)
        with open(os.path.join(current_dir, f"{new_name}.{format_element}"), "wb") as img_f:
            img_f.write(content)


def main():
    format_emote = "json"
    format_image = "png"
    format_music = "nbs"
    format_skip = ["py", "exe", "emotecraft"]
    print(Fore.GREEN + "Приветствую!")
    print(Fore.CYAN + "Эта программа очистит папку .minecraft/emotes от лишнего мусора и упростит поиск по эмоциям.")
    print(Back.LIGHTRED_EX + "Программа обязательно должна находиться в папке " + Back.RED + "emotes/" + Back.LIGHTRED_EX + "!")
    author = input("Введите базовое имя автора всех " + Fore.GREEN + ".json" + Fore.WHITE + " эмоций или введите " + Fore.LIGHTRED_EX + "-" + Fore.WHITE + " чтобы не менять его: " + Fore.YELLOW).strip()
    i = 0
    current_dir = os.getcwd()

    for filename in os.listdir(current_dir):
        if filename in [".", ".."]:
            continue

        file = os.path.join(current_dir, filename)

        if os.path.isdir(file):
            continue

        name, ext = os.path.splitext(filename)
        ext = ext[1:].lower()

        if ext in format_skip or ext == format_image or ext == format_music:
            continue

        if ext != format_emote:
            unlink(file)
            continue

        i += 1

        try:
            with open(file, "rb") as f:
                content = f.read()
        except Exception:
            content = b""

        try:
            content = content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                content = content.decode("utf-8-sig")
            except UnicodeDecodeError:
                content = content.decode("utf-8", errors="ignore")

        content = re.sub(r"[\x00-\x1F\x7F]", "", content)

        if content.startswith("\ufeff"):
            content = content[1:]

        content = re.sub(r"[\x00-\x1F\x7F]", "", content)

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + f"Произошла ошибка при обработке json'a у эмоции {filename}: Некорректный JSON")
            continue

        if not data:
            print(Fore.LIGHTRED_EX + f"Произошла ошибка при обработке json'a у эмоции {filename}: JSON пустой")
            continue

        if author != "-":
            data["author"] = author

        animations = data.get("animations", {})
        name_field = data.get("name", "")

        if not name_field and not list(animations.keys()):
            print(Fore.LIGHTRED_EX + f"Произошла ошибка при получении названия у эмоции: {filename}")
            continue

        new_name = name_field if name_field else (list(animations.keys())[0] if animations else "")
        new_name = re.sub(r"[§&][0-9a-fA-FolmnkrOLMKR]", "", new_name)
        new_name = re.sub(r"[^a-zA-Zа-яА-ЯёЁ0-9\-_() ]", "", new_name)

        content = json.dumps(data, ensure_ascii=False, indent=4)
        new_json_path = os.path.join(current_dir, f"{new_name}.{format_emote}")

        unlink(file)

        with open(new_json_path, "w", encoding="utf-8") as f:
            f.write(content)

        format_image = "png"
        format_music = "nbs"

        clear_trash(current_dir, name, new_name, format_image)
        clear_trash(current_dir, name, new_name, format_music)

        ctypes.windll.kernel32.SetConsoleTitleW("".join(random.choices(string.ascii_letters + string.digits, k=32)))
        print(Fore.WHITE + f"Обработано: " + Fore.GREEN + str(i) + Fore.WHITE + " эмоций.")

    print(Fore.YELLOW + "Очистка от мусора...")

    for filename in os.listdir(current_dir):
        if filename in [".", ".."]:
            continue

        file = os.path.join(current_dir, filename)

        if os.path.isdir(file):
            continue

        name, ext = os.path.splitext(filename)
        ext = ext[1:].lower()

        if ext != format_image and ext != format_music:
            continue

        if not os.path.exists(os.path.join(current_dir, f"{name}.{format_emote}")):
            unlink(file)

    input(Fore.GREEN + "Готово! Мусор успешно удалён.")


if __name__ == "__main__":
    init(autoreset=True)
    main()
