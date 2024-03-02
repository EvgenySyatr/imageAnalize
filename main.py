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
        output_list.append(analyzer.track_max_dispersion_points(20, 50))
    return output_list


def write_array_to_file(array, filename):
    with open(filename, "w") as file:
        for item in array:
            file.write(str(item) + "\n")


def write_tuple_data_to_file(tuple_data, filename):
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
    with open(filename, "w") as file:
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



input_folder = "Input"

all_lab_points = create_analyzers(input_folder)

tuple_data = all_lab_points[0]  # Получаем кортеж из output_list
write_tuple_data_to_file(tuple_data, "output.txt")  # Передаем кортеж в функцию write_tuple_data_to_file






# Создаем объект
#analyzer = ba.PixelBrightnessAnalyzer(input_folder)
#points_for_lab = analyzer.track_max_dispersion_points(20)
#print("Вывод точек")
#for i in range(0, len(points_for_lab[0])):
 #   print(f"{points_for_lab[0][i]} {points_for_lab[1][i]} {points_for_lab[2][i]}")


