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
create_analyzers(input_folder)






# Создаем объект
analyzer = ba.PixelBrightnessAnalyzer(input_folder)

# file_name = "image2.bmp"
#points = analyzer.get_surrounding_pixel_brightness(x, y, file_name) #Яркость по точке центральной
#disp = analyzer.calculate_brightness_variance(x, y, file_name) # дисперсия по точке центральной
#print(f"0008 0007 Средняя яркость: {analyzer.analyze_pixel_and_surroundings(8, 7, file_name)} Средняя дисперсия: {disp}")


# print(analyzer.get_pixel_brightness(27, 21, "Image2.bmp"))
# analyzer.analyze_points_from_file("points.txt", "Image1.bmp")
# print(analyzer.get_background_dispersion())
# analyzer.visualize_explored_area()
# analyzer.save_explored_area("gg.bmp")
# print(analyzer.track_max_dispersion_points(40))

# coordinates = analyzer.track_max_dispersion_points(20) # указываем максимальную дисперсию для фона

