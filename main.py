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


def create_analyzers(input_folder):
    """
    Создает объекты PixelBrightnessAnalyzer для каждого файла BMP в каталоге Input.

    Параметры:
    - input_folder (строка): Путь к каталогу с входными изображениями.
    """
    bmp_filenames = get_bmp_filenames(input_folder)
    for i, bmp_filename in enumerate(bmp_filenames, start=1):
        image_name = os.path.splitext(bmp_filename)[0]  # Получаем имя файла без расширения
        points_file = f"point{i}.txt"  # Генерируем имя файла для сохранения точек
        analyzer = ba.PixelBrightnessAnalyzer(input_folder, image_name + ".bmp", points_file)
        print(f"Создан объект PixelBrightnessAnalyzer для {bmp_filename}")


input_folder = "Input"
# create_analyzers(input_folder)






# Создаем объект
analyzer = ba.PixelBrightnessAnalyzer(input_folder)
points_for_lab = analyzer.track_max_dispersion_points(20)
print("Вывод точек")
for i in range(0, len(points_for_lab[0])):
    print(f"{points_for_lab[0][i]} {points_for_lab[1][i]} {points_for_lab[2][i]}")

