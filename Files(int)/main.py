import win32api
import win32file
import shutil
import os
import zipfile


def get_type_disk(case):
    if   case == 0:
        return "Unknown"
    elif case == 1:
        return "No Root Directory"
    elif case == 2:
        return "Removable Disk"
    elif case == 3:
        return "Local Disk"
    elif case == 4:
        return "Network Drive"
    elif case == 5:
        return "Compact Disc"
    elif case == 6:
        return "RAM Disk"

def task1():
    print("Получение информации о дисках...\n")
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    print("Выберите диск:")
    for i,drive in enumerate(drives):
        print("   ", i,". ", drive, sep="")
    
    c = int(input("\nВыбранный диск: "))
    if (c < 0) or (c >= len(drives)):
        print("Неправильный номер диска!\n")
        return
    
    disk = drives[c]

    print()
    print("------------------------------")
    print("Название: ", disk)
    print("Тип: ", get_type_disk(win32file.GetDriveType(disk)))

    total, used, free = shutil.disk_usage(disk)
    print("Всего: %d ГБ" % (total // (2 ** 30)))
    print("Использовано: %d ГБ" % (used // (2 ** 30)))
    print("Свободно: %d ГБ" % (free // (2 ** 30)))
    t = win32api.GetVolumeInformation(disk)
    print("Метка:", t[0])
    print("------------------------------")
    print()

class FileWorker:
    def __init__(self):
        self.txt = []

    def get_list_files(self):
        self.txt = []
        for file in os.listdir():
            if file.endswith(".txt"):
                self.txt.append(file)
        print("Список файлов: ")
        for n in self.txt:
            print("   ", n)
    
    def create_file(self):
        name = input("Введите имя файла: ")
        my_file = open(name, "w+")
        my_file.close()
        print(f"Файл {name} создан.")
    
    def remove_file(self):
        name = input("Введите имя файла: ")
        os.remove(name)

    def enter_to_file(self):
        name = input("Введите имя файла: ")
        my_file = open(name, "w+")
        my_file.write(input("Введите строку для записи в файл: "))
        my_file.close()
        print("Строка успешн записана.")
    
    def get_from_file(self):
        name = input("Введите имя файла: ")
        my_file = open(name, "r+")
        print("Содержимое файла: ", my_file.read())
        my_file.close()
    
def task2():
    fw = FileWorker()
    menu = "\nМеню:\n   1. Показать список файлов\n   2. Создать файл\n   3. Удалить файл\n   4. Записать информацию в файл\n   5. Считать информацию из файла\n   0. Выход\n\n"
    while True:
        print(menu)
        c = input("Выберите пункт меню: ")
        if c == "1":
            fw.get_list_files()
        elif c == "2":
            fw.create_file()
        elif c == "3":
            fw.remove_file()
        elif c == "4":
            fw.enter_to_file()
        elif c == "5":
            fw.get_from_file()
        elif c == "0":
            break

def task3():
    import json
    data = {'int': 100, 'name': 'Pavel', 'array': ['msg 1', 'msg 2', 'msg 3']}
    outfile = open('data.json', 'w+')
    json.dump(data, outfile)
    outfile.close()
    outfile = open('data.json', 'r+')
    print(outfile.read())
    outfile.close()
    os.remove(outfile.name)

def task4():
    import xml.etree.ElementTree as ET

    p = ET.Element('parent')
    c = ET.SubElement(p, 'child_one')
    tree = ET.ElementTree(p)
    tree.write("data.xml")

    tree = ET.parse('data.xml')
    root = tree.getroot()
    element = root[0]
    ET.SubElement(element, 'child_two')
    tree.write("data.xml")

    ET.dump(tree)

    os.remove('data.xml')


class ZipWorker:
    def __init__(self):
        self.zip = []

    def get_list_files(self):
        self.zip = []
        for file in os.listdir():
            if file.endswith(".zip"):
                self.zip.append(file)
        print("Список файлов: ")
        for n in self.zip:
            print("   ", n)
    
    def create_zip(self):
        name_zip = input("Введите имя архива: ")
        name_file = input("Введите имя файла, который хотите добавить в архив: ")
        newzip = zipfile.ZipFile(name_zip, 'w',zipfile.ZIP_DEFLATED)
        newzip.write(name_file)
        newzip.close()
        print(f"Архив {name_zip} создан.")
    
    def remove_file(self):
        name = input("Введите имя файла: ")
        os.remove(name)
        print("Архив успешно удален.")

    def unpack_zip(self):
        name_zip = input("Введите имя архива: ")
        newzip = zipfile.ZipFile(name_zip, 'r',zipfile.ZIP_DEFLATED)
        newzip.extractall()
        print("Архив успешно распакован. Сожержимое: ")
        newzip.printdir()
        newzip.close()

def task5():
    fw = ZipWorker()
    menu = "\nМеню:\n   1. Показать список архивов\n   2. Создать архив с файлом\n   3. Удалить архив\n   4. Распаковать архив\n   0. Выход\n\n"
    while True:
        print(menu)
        c = input("Выберите пункт меню: ")
        if c == "1":
            fw.get_list_files()
        elif c == "2":
            fw.create_zip()
        elif c == "3":
            fw.remove_file()
        elif c == "4":
            fw.unpack_zip()
        elif c == "0":
            break 

if __name__ == "__main__":
    while True:
        print("Задания:")
        print("1. Задание №1\n2. Задание №2\n3. Задание №3\n4. Задание №4\n5. Задание №5\n0. Выход\n\n")
        c = input("Выберите задание: ")
        if c == "1":
            task1()
        elif c == "2":
            task2()
        elif c == "3":
            print()
            task3()
            print()
        elif c == "4":
            print()    
            task4()
            print()
        elif c == "5":
            task5()
        elif c == "0":
            break 
