import imageCropper as ic
import blackWhiteConverter as bwc
import brightnessAnalyzer as ba
import os
import re
# import exelTable as ex
from PIL import Image
from ExcelHandler import ExcelHandler
from tqdm import tqdm


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


def get_start_index():
    """
    Определяет стартовый индекс для создания объектов PixelBrightnessAnalyzer.

    Если в папке Output есть несколько файлов pointsN.txt, выбирается порядковый номер предпоследнего файла.
    Если файлов pointsN.txt нет или их только один, стартовый индекс устанавливается на 1.

    Возвращает:
    int: Стартовый индекс.
    """
    existing_points_files = [f for f in os.listdir('Output') if f.startswith('points') and f.endswith('.txt')]
    if len(existing_points_files) > 1:
        existing_points_files.sort(key=lambda x: int(x[6:-4]))
        start_index = int(existing_points_files[-2][6:-4])
    elif len(existing_points_files) == 1:
        start_index = 1
    else:
        start_index = 0
    return start_index


def create_analyzers(input_folder, background_dispersion=20, step_size=4):
    """
    Создает объекты PixelBrightnessAnalyzer для каждого файла BMP в каталоге Input.
    Если для какого то из объектов уже есть выходной файл, тогда начинаем со следующего
    Параметры:
    - input_folder (строка): Путь к каталогу с входными изображениями.
    """
    input_disp= input("Введите максимальную дисперсию фона\n     ")
    if(input_disp):
        background_dispersion = int(input_disp)

    output_list = []
    bmp_filenames = get_bmp_filenames(input_folder)
    bmp_filenames = sorted(bmp_filenames, key=extract_number)  # Сортировка имен файлов

    start_index = get_start_index()
    border_input = input("Введите ширину области, которая не будет исследована\n     ")
    # for i in range(start_index + 1, len(bmp_filenames)):
    for i in tqdm(range(start_index + 1, len(bmp_filenames) + 1), desc="Progress of Analise of Image"):
        bmp_filename = bmp_filenames[i - 1]
        image_name = os.path.splitext(bmp_filename)[0]  # Получаем имя файла без расширения
        points_file = f"points{i}.txt"  # Генерируем имя файла для сохранения точек
        analyzer = ba.PixelBrightnessAnalyzer(input_folder, image_name + ".bmp", points_file, "Output")
        print(f"Создан объект PixelBrightnessAnalyzer для {bmp_filename}")
        if(border_input):
            border_width = int(border_input)
        else:
            border_width = 40
        output_list.append(analyzer.track_max_dispersion_points(background_dispersion, step_size, border_width))
    # В зависимости от количества входных файлов меняется количество элементов кортежа output_list
    return output_list


def create_and_save_random_points(input_folder, width=40):
    """
    Создает объекты PixelBrightnessAnalyzer для каждого файла BMP в каталоге Input
    и вызывает метод select_random_points_and_save для каждого анализатора.

    Параметры:
    - input_folder (строка): Путь к каталогу с входными изображениями.
    - background_dispersion (int): Максимальная дисперсия фона.
    - step_size (int): Размер шага при перемещении по изображению.
    """
    output_list = []
    bmp_filenames = get_bmp_filenames(input_folder)
    bmp_filenames = sorted(bmp_filenames, key=extract_number)  # Сортировка имен файлов
    start_index = get_start_index()

    for i in tqdm(range(start_index + 1, len(bmp_filenames) + 1), desc="Прогресс анализа изображений"):
        bmp_filename = bmp_filenames[i - 1]

        image_name = os.path.splitext(bmp_filename)[0]  # Получаем имя файла без расширения
        points_file = f"points{i}.txt"  # Генерируем имя файла для сохранения точек
        analyzer = ba.PixelBrightnessAnalyzer(input_folder, image_name + ".bmp", points_file, "Output")
        print(f"Создан объект PixelBrightnessAnalyzer для {bmp_filename}")
        height = 238
        # Вызываем метод select_random_points_and_save для каждого анализатора
        analyzer.select_random_points_and_save(height, width)

    return output_list


def create_analyzers_from_points_files(output_folder):
    """
    Создает объекты PixelBrightnessAnalyzer для каждого файла pointsN.txt в каталоге Output.

    Параметры:
    - output_folder (строка): Путь к каталогу с файлами pointsN.txt.

    Возвращает:
    - analyzers (list): Список объектов PixelBrightnessAnalyzer.
    """
    analyzers = []

    # Получаем список всех файлов в каталоге Output
    files = os.listdir(output_folder)

    # Фильтруем только файлы pointsN.txt
    points_files = [file for file in files if file.startswith("points") and file.endswith(".txt")]

    # Сортируем файлы по числовому значению в имени
    points_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

    # Создаем объекты PixelBrightnessAnalyzer для каждого файла pointsN.txt
    for points_file in points_files:
        # Извлекаем номер из имени файла
        analyzer_number = int(points_file.split("points")[1].split(".")[0])

        # Получаем имя изображения и путь к нему
        image_name = f"Image{analyzer_number}.bmp"
        input_folder = "Input"  # Путь к каталогу с изображениями

        # Генерируем имя файла для сохранения точек
        points_file_path = os.path.join(output_folder, points_file)

        # Создаем объект PixelBrightnessAnalyzer
        analyzer = ba.PixelBrightnessAnalyzer(input_folder, image_name, points_file_path, output_folder)
        analyzers.append(analyzer)

    return analyzers


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


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    clear_console()
    print("Меню:")
    print("1. Обрезать изображения")
    print("2. Преобразовать изображения в черно-белый формат")
    print("3. Отформатировать названия изображений")
    print("4. Выполнить анализ яркости изображений")
    print("5. Импортировать Точки Границы из txt в exel")
    print("6. Импортировать Точки Фона из txt в exel")
    print("0. Выход")

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
        final_EXPORT_DATAF3F5_TO_EXEL(1)
    elif choice == "6":
        final_EXPORT_DATAF3F5_TO_EXEL(0)
    elif choice == "0":
        print("До свидания!")
        exit()
    else:
        print("Некорректный выбор. Пожалуйста, выберите действие из списка.")


def analyze_brightness_menu():
    print("Выберите опцию для анализа яркости изображений:")
    print("1. Найти максимальную дисперсию фона")
    print("2. Составить points файлы для входных изображений [Граница]")
    print("3. Очистить выходные файлы F3 F5")
    print("4. Заполнить F3 F5 файлы")
    print("5. Составить points файлы для входных изображений [Фон]")
    print("0. Вернуться в главное меню")

    choice = input("Введите номер действия: ")

    if choice == "1":
        border_width = int(input("Введите ширину исследуемой сверху области\n     "))
        analyze = ba.PixelBrightnessAnalyzer("Input")
        analyze.save_explored_area(border_width)
        print(f"Максимальная дисперсия фона : {analyze.get_background_dispersion(border_width)}")
        input("Для продолжения нажмите Enter...")
    elif choice == "2":
        input_folder = "Input"
        create_analyzers(input_folder)
    elif choice == "3":
        clear_files("outputF3.txt", "outputF5.txt")
        input("Для продолжения нажмите Enter...")
    elif choice == "4":
        analyzer_list = create_analyzers_from_points_files("Output")
        for analyzer in analyzer_list:
            points_list = analyzer.get_points_from_points_file(analyzer.points_file)
            tuple = analyzer.fill_lists(points_list)
            write_tuple_F3_data_to_file(tuple, "outputF3.txt")
            write_tuple_F5_data_to_file(tuple, "outputF5.txt")
        input("Для продолжения нажмите Enter...")
    elif choice == "5":
        input_folder = "Input"
        create_and_save_random_points(input_folder, 80) #второй параметр это ширина полоски
        input("Для продолжения нажмите Enter...")
    elif choice == "0":
        return
    else:
        print("Некорректный выбор. Пожалуйста, выберите действие из списка.")

def read_data_from_file(filename):
    """
    Считывает данные из файла и возвращает список кортежей значений.

    Аргументы:
    - filename (str): Имя файла для чтения.

    Возвращает:
    - data (list): Список кортежей значений.
    """
    data = []
    with open(filename, "r") as file:
        for line in file:
            # Разбиваем строку по пробелам и преобразуем значения в нужный формат
            values = line.strip().split()
            point = (float(values[0]), float(values[1]))
            brightness = float(values[2])
            dispersion = float(values[3])
            data.append((point, brightness, dispersion))
    return data


def final_EXPORT_DATAF3F5_TO_EXEL(contur_true, exel_file="CopyOfWorkTable.xlsx"):
    """
    Заполняет таблицу значениями из outputF3.txt и outputF5.txt
    contur_true - если 1 то граница, если 0 то фон
    :param exel_file: ,
    :return:
    """
    input_folder = "Input"
    output_folder = "Output"
    image_name = "Image1.bmp"
    points_file = "points1.txt"
    # Генерируем имя файла для сохранения точек
    points_file_path = os.path.join(output_folder, points_file)
    # Создаем объект PixelBrightnessAnalyzer
    analyzer = ba.PixelBrightnessAnalyzer(input_folder, image_name, points_file_path, output_folder)
    data = read_data_from_file("outputF3.txt")
    ex = ExcelHandler(exel_file)
    data_addition = read_data_from_file("outputF5.txt")

    # Заполняем точки границы
    if (contur_true == 1):
        # X
        list_input = [data[i][0][0] for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 1, 4, 489)
        # Y
        list_input = [data[i][0][1] for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 2, 4, 489)
        # M3
        list_input = [int(data[i][1]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 3, 4, 489)
        # D3
        list_input = [int(data[i][2]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 4, 4, 489)

        # M5
        list_input = [int(data_addition[i][1]) for i in
                      range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 5, 4, 489)
        # D5
        list_input = [int(data_addition[i][2]) for i in
                      range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 6, 4, 489)
        N = 489 - 4 + 1
        list_last_column = [1] * N
        ex.fill_column(list_last_column, 7, 4, 489)
    # Заполняем точки фона
    if (contur_true == 0):
        # X
        list_input = [data[i][0][0] for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 1, 490, 983)
        # Y
        list_input = [data[i][0][1] for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 2, 490, 983)
        # M3
        list_input = [int(data[i][1]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 3, 490, 983)
        # D3
        list_input = [int(data[i][2]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 4, 490, 983)

        # M5
        list_input = [int(data_addition[i][1]) for i in
                      range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 5, 490, 983)
        # D5
        list_input = [int(data_addition[i][2]) for i in
                      range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 6, 490, 983)
        N = 983 - 490 + 1
        list_last_column = [0] * N
        ex.fill_column(list_last_column, 7, 490, 983)
###################################################

# Основной цикл программы
while True:
    main_menu()
