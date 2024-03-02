import imageCropper as ic
import blackWhiteConverter as bwc
import brightnessAnalyzer as ba
import os

"""
blackWhite converter после imageCropper!!!
"""

# Создаем экземпляр класса ImageCropper
cropper = ic.ImageCropper()
# Вызываем метод crop_images
# cropper.crop_images()
# cropper.rename_output_images("Image")

# bw = bwc.BlackAndWhiteConverter()
# bw.convert_to_black_and_white()

def get_bmp_filenames(input_folder):
    """
    Получает список имен всех файлов с расширением ".bmp" из каталога Input.

    Параметры:
    - input_folder (строка): Путь к каталогу с входными изображениями.

    Возвращает:
    - bmp_filenames (список строк): Список имен всех файлов с расширением ".bmp" в каталоге Input.
    """
    bmp_filenames = []
    if not os.path.exists(input_folder):
        print(f"Папка {input_folder} не существует.")
        return bmp_filenames

    files = os.listdir(input_folder)
    for file in files:
        if file.endswith(".bmp"):
            bmp_filenames.append(file)
    return bmp_filenames

def extract_number(filename):
    return int(filename.split('Image')[1].split('.')[0])

def create_analyzers(input_folder):
    """
    Создает объекты PixelBrightnessAnalyzer для каждого файла BMP в каталоге Input.

    Параметры:
    - input_folder (строка): Путь к каталогу с входными изображениями.
    """
    output_list = []
    bmp_filenames = get_bmp_filenames(input_folder)
    bmp_filenames = sorted(bmp_filenames, key=extract_number)  # Сортировка имен файлов
    for i, bmp_filename in enumerate(bmp_filenames, start=1):
        image_name = os.path.splitext(bmp_filename)[0]  # Получаем имя файла без расширения
        points_file = f"points{i}.txt"  # Генерируем имя файла для сохранения точек
        analyzer = ba.PixelBrightnessAnalyzer(input_folder, image_name + ".bmp", points_file, "Output")
        print(f"Создан объект PixelBrightnessAnalyzer для {bmp_filename}")
        output_list.append(analyzer.track_max_dispersion_points(20, 4))
    # В зависимости от количества входных файлов меняется количество элементов кортежа output_list
    return output_list


def write_array_to_file(array, filename):
    with open(filename, "w") as file:
        for item in array:
            file.write(str(item) + "\n")


def write_tuple_F3_data_to_file(tuple_data, filename):
    """
    Записывает данные из кортежа в файл.

    Аргументы:
    - tuple_data (tuple): Кортеж с данными.
    - filename (str): Имя файла для записи.

    Возвращает:
    None
    """
    tuple_data = tuple_data
    # Открываем файл для записи
    with open(filename, "a") as file:
        # Распаковываем кортеж
        points = tuple_data[0]
        brightness_list = tuple_data[1]
        dispersion_list = tuple_data[2]
        # Записываем данные в файл
        for i in range(len(points)):
            point = points[i]
            brightness = brightness_list[i]
            dispersion = dispersion_list[i]
            file.write(f"{point[0]} {point[1]} {brightness} {dispersion}\n")

def write_tuple_F5_data_to_file(tuple_data, filename):
    """
    Записывает данные из кортежа в файл.

    Аргументы:
    - tuple_data (tuple): Кортеж с данными.
    - filename (str): Имя файла для записи.

    Возвращает:
    None
    """
    tuple_data = tuple_data
    # Открываем файл для записи
    with open(filename, "a") as file:
        # Распаковываем кортеж
        points = tuple_data[0]
        brightness_list = tuple_data[3]
        dispersion_list = tuple_data[4]
        # Записываем данные в файл
        for i in range(len(points)):
            point = points[i]
            brightness = brightness_list[i]
            dispersion = dispersion_list[i]
            file.write(f"{point[0]} {point[1]} {brightness} {dispersion}\n")


def clear_files(*filenames):
    """
    Очищает содержимое указанных файлов.

    Аргументы:
    - filenames (строки): Имена файлов для очистки.

    Возвращает:
    None
    """
    for filename in filenames:
        with open(filename, "w") as file:
            file.truncate(0)


# input_folder = "Input"

# all_lab_points = create_analyzers(input_folder)

# tuple_data = all_lab_points[0]  # Получаем кортеж из output_list
# write_tuple_F3_data_to_file(tuple_data, "outputF3.txt")  # Передаем кортеж в функцию write_tuple_data_to_file

# write_tuple_F5_data_to_file(tuple_data, "outputF5.txt")  # Передаем кортеж в функцию write_tuple_data_to_file

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    input("Нажмите Enter для продолжения\n")
    clear_console()
    print("Меню:")
    print("1. Обрезать изображения")
    print("2. Преобразовать изображения в черно-белый формат")
    print("3. Отформатировать названия изображений")
    print("4. Выполнить анализ яркости изображений")
    print("5. Выход")

    choice = input("Введите номер действия: ")

    if choice == "1":
        cropper = ic.ImageCropper()
        cropper.crop_images()
        cropper.rename_output_images("Image")
    elif choice == "2":
        bw = bwc.BlackAndWhiteConverter()
        bw.convert_to_black_and_white()
    elif choice == "3":
        cropper = ic.ImageCropper()
        cropper.rename_output_images("Image")
    elif choice == "4":
        analyze_brightness_menu()
    elif choice == "5":
        print("До свидания!")
        exit()
    else:
        print("Некорректный выбор. Пожалуйста, выберите действие из списка.")

def analyze_brightness_menu():
    print("Выберите опцию для анализа яркости изображений:")
    print("1. Найти точки, сделать анализ дисперсии и яркости по F3 и F5")
    print("2. Очистить выходные файлы F3 F5")
    print("3. Вернуться в главное меню")

    choice = input("Введите номер действия: ")

    if choice == "1":
        input_folder = "Input"
        all_lab_points = create_analyzers(input_folder)
        for i in range(len(all_lab_points)):
            tuple_data = all_lab_points[i]  # Получаем кортеж из output_list
            write_tuple_F3_data_to_file(tuple_data, "outputF3.txt")  # Передаем кортеж в функцию write_tuple_data_to_file
            write_tuple_F5_data_to_file(tuple_data, "outputF5.txt")  # Передаем кортеж в функцию write_tuple_data_to_file
    elif choice == "2":
        clear_files("outputF3.txt", "outputF5.txt")
        pass
    elif choice == "3":
        return
    else:
        print("Некорректный выбор. Пожалуйста, выберите действие из списка.")


# Основной цикл программы
while True:
    main_menu()
