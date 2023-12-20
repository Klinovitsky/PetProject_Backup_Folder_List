# --------------------------------------------------------------------------------------------------------------
# PetProject_Backup_Folder_List. 02
# Задача получить из файла CSV список папок для архивации и параметров архивации, пройти циклом по списку папок,
# архивировать, только не отмеченные знаком «#», передать параметры между функциями и в командную строку,
# создать архив, # затем перенести его на внешний накопитель с сопроводительным файлом,
# содержащим наименования папок в архиве.
# --------------------------------------------------------------------------------------------------------------

# import glob
import os
import datetime
import shutil
import csv


def get_folders_list():
    """
    Get folders from file and save them to a list.
    Reading data from reader Object in a for Loop (The reader object can be looped over only once)!
    File structure: first string 'Header' which is commented + strings with paths
    """
    file = open('backup_these_folders.csv', encoding='Utf-8')  # Default coding for windows is cp2151, but CSV is UTF-8
    reader = csv.reader(file)
    skip_line = '#'
    all_folders = []
    print('...... Reading CSV file')
    for row in reader:
        folders = list(row)  # Convert to list

        # if my_setting[0] == 'backup_from':
        #     path_from = my_setting[1]   # Get the second col, from [1]
        # print('Row #' + str(reader.line_num) + ' ' + str(folders))    # line_num - attribute of the reader object

        # Skip commented with '#' strings
        # row[0] because raw is a list, and we need to skip such chars "['']". Example: C:/_from3 instead ['C:/_from2']
        if skip_line in row[0]:
            # line_num - attribute of the reader object
            print('Row #' + str(reader.line_num) + ' ' + str(folders) +
                  '--- The string with character "#" - so, skip the line and do not archive it')
        else:
            print('Row #' + str(reader.line_num) + ' ' + str(folders))
            all_folders = all_folders + folders

    return all_folders

# Setting in file:
# Setting,Value
# backup_to,C:\_BAK\_2023_BACKUP_MY_UTIL
# path_to_7zip,C:\Program Files\7-Zip\7z.exe
# zip_options,a -tzip -mx5 -r0
# test_archive,yes
# copy_folders_after_archiving,yes
# copy_to,C:/_to


def take_settings_from_file():
    print('...... Reading settings from CSV file')
    file = open('my_backup_settings.csv', encoding='Utf-8')
    reader = csv.DictReader(file)
    dict_data = {}

    # Reading data from reader Object in a for Loop (The reader object can be looped over only once)!
    # And adding values to the dictionary
    for row in reader:
        # print(row['Setting'] + ', ' + row['Value'])
        # dict_data = row['Setting'], row['Value']
        print('Row #' + str(reader.line_num) + ' ' + row['Setting'] + ', ' + row['Value'])
        dict_data[row['Setting']] = row['Value']

    # Get values from dict
    backup_to_shl = dict_data['backup_to']
    path_to_7zip = dict_data['path_to_7zip']
    zip_options_shl = dict_data['zip_options']
    copy_folders_after_archiving_shl = dict_data['copy_folders_after_archiving']
    copy_to_shl = dict_data['copy_to']

    if dict_data['test_archive'] == 'yes':
        test_archive_shl = True
    else:
        test_archive_shl = False

    return backup_to_shl, path_to_7zip, zip_options_shl, test_archive_shl, copy_folders_after_archiving_shl, copy_to_shl


def write_to_csv(folders_archived):  # The reader object can be looped only once!
    """
    Save a list of archived folders
    """
    file_name = 'output.csv'
    output_file = open(file_name, 'w', newline='')  # newline is for Windows, to avoid double-spacing in CSV
    writer = csv.writer(output_file, delimiter='\t', lineterminator='\n')  # \t - tab \n\n - double-space
    writer.writerow(['Number', 'Path'])

    counter = 1
    for path in folders_archived:
        print('Folders in archive #' + str(counter) + ' ' + path)
        writer.writerow([counter, path])
        counter = counter + 1

    print('...... The file "' + output_file.name + '" is saved to the project folder: "' + os.getcwd() + '"')
    print('folders_archived', folders_archived)
    print(os.listdir(copy_to))  # get list of files in "copy_to" folder
    output_file.close()

    source = file_name
    shutil.move(source, copy_to)  # Move log file. dst can be a folder

    # Извращения с переименованием файла в целевой директории.
    # Задача сделать имя сопроводительного файла аналогичным имени архива.
    path = file_to_move
    # raw path = r"C:\_BAK\_2023_BACKUP_MY_UTIL/20231220_172254_bak.zip"
    file_to_rename = path[path.find('202'):]    # Cut everything before '202'
    file_to_rename_final = copy_to + '/' + file_to_rename + '.txt'
    file_to_move_final = copy_to + '/' + source
    os.rename(file_to_move_final, file_to_rename_final)
    print('....... Renaming the file:', file_to_move_final, file_to_rename_final)


def archive(folders, backup_to_sh, path_to_7zip_sh, zip_options, test_archive_sha):
    """
    Запуск архиватора с параметрами из файла настройки. Главные параметры ниже:
    :param folders:
    :param zip_options:
    """
    print('...... Check disk usage')

    result = shutil.disk_usage('C:/')
    gb = 10 ** 9
    print('Сырые данные по свободному месту:', result)
    print(f"Всего места: {result.total / gb:.2f}")
    print(f"Места использовано: {result.used / gb:.2f}")
    print(f"Места осталось: {result.free / gb:.2f}")

    # R от слова raw, т.е r – это сырые строки (необработанные строки).
    # Нужны для того, чтобы slash "\" не вызывал экранирование символов.
    # In Python, the "r" prefix before a string denotes that it is a raw string literal.
    # This means that any backslashes () in the string are not treated as escape characters.

    # Эксперименты с raw strings
    # path_to_7zip = str(path_to_7zip_1.encode('cp1251'))
    # print(path_to_7zip)
    # my_string = 'кот cat'.decode('utf-8')
    # path_to_7zip = r'"C:\Program Files\7-Zip\7z.exe"' # working string

    path_to_7zip = '"' + path_to_7zip_sh + '"'     # CMD takes only "", '' - don't work, r' - don't work too
    dt = datetime.datetime.now()                  # делаем каталог для копий по текущему времени
    current_date = dt.strftime('%Y%m%d_%H%M%S')   # Добавил секунды, чтобы не выдавало ошибку на уже существующий файл

    # Берем значения из функции get_folders_list(), затем в списке перебираем значения
    counter = 0
    for path in folders:
        print('File\\folder to archive #' + str(counter) + ' ' + path)
        counter = counter + 1
    print('...... Start of archiving. Please, wait')

    # backup_from = str.strip(folders[1])   # Удаляем пробел из строки заодно.

    target_path = backup_to_sh + '/' + current_date + "_bak"

    # Архивируем всё содержимое папок, что получили из функции get_folders_list()
    # ' ' - это добавлял т.к. без пробелов между опциями 7-зип выдавал ошибку
    # Для имён, содержащих пробелы, необходимо использовать двойные кавычки внутри строки.

    for item_to_archive in folders:
        item_to_archive_2 = '"' + str(item_to_archive) + '"'    # Список приезжает в одинарных кавычках, а нужны - ""

        # Выяснилось что нужно сделать экранирование двумя кавычками всей команды
        # 1) "C:\Program Files\7-Zip\7z" a -tzip -mx5 -r0 "c:\_from_test\file.zip" "C:\_BAK\_2023_BACKUP_MY_UTIL"
        # 2) ""C:\Program Files\7-Zip\7z" a -tzip -mx5 -r0 "c:\_from_test\file.zip" "C:\_BAK\_2023_BACKUP_MY_UTIL""
        # Если из CMD запускать строка 1 отрабатывает, но os.system запускает командой CMD /C и в этом случае строка 1
        # Выдает ошибку, а вот строка 2 - будет работать отлично!

        os.system('"' + path_to_7zip + ' ' + zip_options + ' ' + target_path + ' ' + item_to_archive_2 + '"' + '> nul')

        # Можно добавить это если нужен лог. Проверил, работает, отключил. В конце строки не забыть поставить ")"
        #                    + '>' + backup_to + '/' + current_date + '_bak' + '_log.txt'
        # Либо можно дописать сзади строки '> nul', чтобы не выводил в консоль ничего

        print('...... Archiving', item_to_archive_2, 'Target path/file:', target_path)

        # Создаю zip-архив с уровнем компрессии 5.
        # В архив попадет все содержимое всех каталогов.
        # Разделяю логику и настройки, выделил настройки в конфиг, стало очень удобно менять параметры.

        # KEYS:
        # Параметры: "А -tzip -ssw -mx5 -pPassword -r0". Буква стоит русская т.к. PEP ругался
        # -ssw	Включить, файл в архив, даже если он в данный момент используется.
        #       Для резервного копирования очень полезный ключ.
        # -mx5	Уровень компрессии. 0 - без компрессии, 9 - самая большая компрессия. Например, -mx5 (нормальная)
        # -r	Рекурсивное архивирование для папок. Задается числом от 0 (все каталоги) до количества уровней каталогов,
        #       которые нужно включить в архив.
        # -t	Тип архива. По умолчанию создаются файлы в формате 7z. Примеры, -tzip, -tgz

        # -p{Password} : set Password
        # -bb[0-3] : set output log level
        # -bt : show execution time statistics
        # -sni : store NT security information
        # -m{Parameters} : set compression Method
        # t : Test integrity of archive (7z t <archive-name>)
        # u : Update files to archive
        # Ключ -df удаляет скопированные каталоги после архивирования
        # https://www.dmosk.ru/miniinstruktions.php?mini=7zip-cmd - другие команды см. здесь

    if test_archive_sha is True:    # Test archive
        print('...... Testing')
        # Example: "C:\Program Files\7-Zip\7z.exe" t C:\_to\2023_12_09_1502_bak.zip
        zip_options_test = "t"
        os.system('"' + path_to_7zip + ' ' + zip_options_test + ' ' + target_path + '.zip' + '"' + '> nul')
        # > nul, means "No log, please"
        print('...... Test completed! Archive: ' + target_path + ' saved.')
    else:
        print('...... Archive testing was not performed because was disabled in settings')
        pass

    file_to_copy_temp = target_path
    return file_to_copy_temp


def copy_folders(file_to_move_shadow, copy_folders_after_archiving_shadow):

    if copy_folders_after_archiving_shadow == 'yes' or 'Yes':

        # скопируем все каталоги в созданный каталог, копируем дерево, запятая перед местом назначения обязательна
        source = file_to_move_shadow + '.zip'
        destination = copy_to

        try:
            shutil.move(source, destination)  # dst can be a folder
            print("...... Moved successfully.")

        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        except shutil.Error:
            print("Huston we have a problem. Error!")

        # List files and directories
        print("...... Files moved here:", destination, ". "
                                                       "The destination folder contains the following files:\n",
              os.listdir(destination))


if __name__ == '__main__':
    folders_to_archive = get_folders_list()
    parameters = take_settings_from_file()
    backup_to = parameters[0]
    path_to_7zip_1 = parameters[1]
    zip_options = parameters[2]
    test_archive = parameters[3]
    copy_folders_after_archiving = parameters[4]
    copy_to = parameters[5]  # Move file here after archiving

    file_to_move = archive(folders_to_archive, backup_to, path_to_7zip_1, zip_options, test_archive)

    move_zip_to = copy_to
    move_zip_from = backup_to

    copy_folders(file_to_move, copy_folders_after_archiving)

    write_to_csv(folders_to_archive)    # Pass a list of folders to the function
