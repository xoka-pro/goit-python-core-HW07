import re
import shutil
import sys
from pathlib import Path

# === ГЛОБАЛЬНІ ЗМІННІ ===
target_folders = ['images', 'documents', 'audio', 'video', 'archives', ]

# списки файлів у кожній категорії


image_files = []
document_files = []
audio_files = []
video_files = []
archive_files  = []

known_ext = []  # перелік усіх відомих розширень
unknown_ext = []  # перелік НЕ відомих розширень
# === КІНЕЦЬ ГЛОБАЛЬНИХ ЗМІННИХ ===


def init(folder: Path) -> None:
    """ функція створює цільові директорії"""

    for element in target_folders:
        new_folder = folder / element
        new_folder.mkdir(exist_ok=True, parents=True)
    return None


def cleaner(folder: Path) -> None:
    """функція рекурсивно видаляє порожні директорії в робочій директорії виключаючі цільові"""
    for element in folder.iterdir():
        if element.is_dir():
            if element.name not in target_folders:
                cleaner(element)
                try:
                    element.rmdir()
                except:
                    print(f'Directory {element} is not empty. Can not remove')
                    continue
    return None


def normalize(filename) -> str:
    """  Функція normalize:

    +++ 1. Проводить транслітерацію кирилічного алфавіту на латинський.
    +++ 2. Замінює всі символи крім латинських літер, цифр на '_'.

    Вимоги до функції normalize:
    +++ приймає на вхід рядок та повертає рядок;
    +++ проводить транслітерацію кирилічних символів на латиницю;
    +++ замінює всі символи, крім літер латинського алфавіту та цифр, на символ '_';
    +++ транслітерація може не відповідати стандарту, але бути читабельною;
    +++ великі літери залишаються великими, а маленькі — маленькими після транслітерації.  """

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(cyr)] = lat
        TRANS[ord(cyr.upper())] = lat.upper()

    transcripted_filename = filename.translate(TRANS)

    normalized_filename = re.sub('[^A-Za-z0-9.]+', '_', transcripted_filename)

    return normalized_filename


def archive_handler() -> None:

    for file in Path(folder_to_sort / 'archives').iterdir():

        folder_for_file = Path(folder_to_sort / 'archives' / normalize(file.name.replace(file.suffix, '')))
        folder_for_file.mkdir(exist_ok=True, parents=True)

        try:
            shutil.unpack_archive(str(file.resolve()),
                               str(folder_for_file.resolve()))
        except shutil.ReadError:
            print(f'Це не архів {file}!')
            folder_for_file.rmdir()
            continue
    return None


def sort_folder(folder: Path) -> None:
    """
    функція:
    - переносе файли по директоріях за шаблонами
    - заповнює списки файлів
    - заповнює списки відомих та невідомих розширень
    """


    # визначаємо розширення за якими будемо сортувати файли
    image_ext = ['JPEG', 'PNG', 'JPG', 'SVG', ]
    document_ext = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', ]
    audio_ext = ['MP3', 'OGG', 'WAV', 'AMR', ]
    video_ext = ['AVI', 'MP4', 'MOV', 'MKV', ]
    archive_ext = ['ZIP', 'GZ', 'TAR', ]

    for element in folder.iterdir():
        if element.is_dir() and element not in target_folders:
            sort_folder(element)
        else:
            for file in folder.iterdir():
                if file.suffix[1:].upper() in image_ext:
                    image_folder = Path('images')
                    file.replace(folder_to_sort / image_folder / normalize(file.name))
                    known_ext.append(file.suffix)
                    image_files.append(normalize(file.name))

                elif file.suffix[1:].upper() in document_ext:
                    document_folder = Path('documents')
                    file.replace(folder_to_sort / document_folder / normalize(file.name))
                    known_ext.append(file.suffix)
                    document_files.append(normalize(file.name))

                elif file.suffix[1:].upper() in audio_ext:
                    audio_folder = Path('audio')
                    file.replace(folder_to_sort / audio_folder / normalize(file.name))
                    known_ext.append(file.suffix)
                    audio_files.append(normalize(file.name))

                elif file.suffix[1:].upper() in video_ext:
                    video_folder = Path('video')
                    file.replace(folder_to_sort / video_folder / normalize(file.name))
                    known_ext.append(file.suffix)
                    video_files.append(normalize(file.name))

                elif file.suffix[1:].upper() in archive_ext:
                    archive_folder = Path('archives')
                    file.replace(folder_to_sort / archive_folder / normalize(file.name))
                    known_ext.append(file.suffix)
                    archive_files.append(normalize(file.name))

                else:
                    normalize(file.name)
                    if not file.is_dir():
                        unknown_ext.append(file.suffix)
    return None


def general():

    if len(sys.argv) < 2:
        print(f'The path to folder is not specified. Check arguments.')
        exit()
    global folder_to_sort
    folder_to_sort = Path(sys.argv[1])
    if not Path(folder_to_sort).is_dir():
        print(f'Your argument is not folder. Check arguments.')
        exit()

    init(folder_to_sort)
    sort_folder(folder_to_sort)
    archive_handler()
    cleaner(folder_to_sort)

    global image_files
    global document_files
    global audio_files
    global video_files
    global archive_files
    global known_ext
    global unknown_ext

    known_ext = list(set(known_ext))
    print(f'Відомі розширення файлів: {known_ext}')
    unknown_ext = list(set(unknown_ext))
    unknown_ext.remove("")
    print(f'Невідомі розширення файлів: {unknown_ext}')
    image_files = list(set(image_files))
    print(f'Список файлів у категорії "зображення": {image_files}')
    document_files = list(set(document_files))
    print(f'Список файлів у категорії "документи": {document_files}')
    audio_files = list(set(audio_files))
    print(f'Список файлів у категорії "музика": {audio_files}')
    video_files = list(set(video_files))
    print(f'Список файлів у категорії "відео": {video_files}')
    archive_files = list(set(archive_files))
    print(f'Список файлів у категорії "архіви": {archive_files}')


if __name__ == '__main__':

    general()
