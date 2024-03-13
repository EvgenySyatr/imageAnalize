import imageCropper as ic
import blackWhiteConverter as bwc
import brightnessAnalyzer as ba
import os
import re
# import exelTable as ex
from PIL import Image
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
    print("5. Импортировать Points из txt в exel")
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
    elif choice == "0":
        print("До свидания!")
        exit()
    else:
        print("Некорректный выбор. Пожалуйста, выберите действие из списка.")

def analyze_brightness_menu():
    print("Выберите опцию для анализа яркости изображений:")
    print("1. Составить points файлы для входных изображений")
    print("2. Очистить выходные файлы F3 F5")
    print("3. Заполнить F3 F5 файлы")
    print("4. Найти максимальную дисперсию фона")
    print("0. Вернуться в главное меню")

    choice = input("Введите номер действия: ")

    if choice == "1":
        input_folder = "Input"
        create_analyzers(input_folder)

    elif choice == "2":
        clear_files("outputF3.txt", "outputF5.txt")
        pass
    elif choice == "3":
        analyzer_list = create_analyzers_from_points_files("Output")
        for analyzer in analyzer_list:
            # point_list = []
            # analyzer.fill_lists(point_list)
            print(analyzer.points_file)
            points_list = analyzer.get_points_from_points_file()
            tuple = analyzer.fill_lists(points_list)
            write_tuple_F3_data_to_file(tuple, "outputF3.txt")
            write_tuple_F5_data_to_file(tuple, "outputF5.txt")
    elif choice == "4":
        # image_for_analize = "Image1.bmp"
        border_width = int(input("Введите ширину исследуемой сверху области\n     "))
        analyze = ba.PixelBrightnessAnalyzer("Input")
        analyze.save_explored_area(border_width)
        continue_input = input("Enter чтобы продолжить, любой ввод чтобы вернуться в меню\n")
        if (continue_input):
            return
        print(f"Максимальная дисперсия фона : {analyze.get_background_dispersion(border_width)}")
        input()
    elif choice == "0":
        return
    else:
        print("Некорректный выбор. Пожалуйста, выберите действие из списка.")

###################################################

# # Основной цикл программы
# while True:
#     main_menu()

###########################################################################
input_folder = "Input"
output_folder = "Output"
image_name = "Image1.bmp"
points_file = "points1.txt"
# Генерируем имя файла для сохранения точек
points_file_path = os.path.join(output_folder, points_file)
 # Создаем объект PixelBrightnessAnalyzer
analyzer = ba.PixelBrightnessAnalyzer(input_folder, image_name, points_file_path, output_folder)

