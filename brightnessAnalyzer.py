from PIL import Image
import os


class PixelBrightnessAnalyzer:
    def __init__(self, input_folder):
        self.input_folder = input_folder

    def get_pixel_brightness(self, x, y, image_name):
        img_path = os.path.join(self.input_folder, image_name)
        img = Image.open(img_path)
        pixel = img.getpixel((x, y))
        # Яркость пикселя для черно-белого изображения равна значению пикселя
        brightness = pixel
        return brightness

    def get_surrounding_pixel_brightness(self, x, y, image_name):
        """
        Получает яркость 9 соседних пикселей вокруг заданной точки.

        Аргументы:
        x (int): Координата x центрального пикселя.
        y (int): Координата y центрального пикселя.
        image_name (str): Имя файла изображения.

        Возвращает:
        list: Список со значениями яркости 9 соседних пикселей вокруг центрального пикселя.
        """
        surrounding_pixels_brightness = []

        # Координаты всех 9 пикселей (включая изначальную точку)
        neighbors_coordinates = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        ]

        # Получаем яркость каждого соседнего пикселя
        for coord_x, coord_y in neighbors_coordinates:
            brightness = self.get_pixel_brightness(coord_x, coord_y, image_name)
            surrounding_pixels_brightness.append(brightness)
        return surrounding_pixels_brightness

    def analyze_pixel_and_surroundings(self, x, y, image_name):
        """
        Анализирует среднюю яркость для заданной точки и ее 8 соседей.

        Аргументы:
        x (int): Координата x заданной точки.
        y (int): Координата y заданной точки.
        image_name (str): Имя файла изображения.

        Возвращает:
        float: Средняя яркость заданной точки и ее 8 соседей.
        """
        # Получаем значения яркости заданной точки и ее 8 соседей
        surrounding_brightness = self.get_surrounding_pixel_brightness(x, y, image_name)

        # Средняя яркость
        mean_brightness = sum(surrounding_brightness) / len(surrounding_brightness)

        return mean_brightness

    def dispersion_by_brightness_list(self, values):
        """
        Вычисляет дисперсию списка значений.

        Аргументы:
        values (list): Список числовых значений.

        Возвращает:
        float: Дисперсия списка значений.

        Примечания:
        Если в списке меньше двух элементов, возвращает 0.
        """
        n = len(values)
        if n < 2:
            return 0

        mean = sum(values) / n
        dispersion = sum((x - mean) ** 2 for x in values) / (n - 1)

        return dispersion

    def get_points_from_file(self, file_name):
        """
        Получает координаты точек из текстового файла.

        Аргументы:
        file_name (str): Имя текстового файла с координатами точек.

        Возвращает:
        list: Список точек в формате (x, y).
        """
        points = []

        # Полный путь к текстовому файлу
        file_path = os.path.join(self.input_folder, file_name)

        # Чтение координат из файла
        with open(file_path, 'r') as file:
            for line in file:
                # Разделение строки на координаты x и y
                coordinates = list(map(int, line.split()))
                x, y = coordinates if len(coordinates) == 2 else (
                coordinates[0], 0)  # Если только одна координата, то y=0
                points.append((x, y))

        return points

    def analyze_point(self, x, y, image_name):
        """
        Анализирует яркость и дисперсию для заданной точки.

        Аргументы:
        x (int): Координата x заданной точки.
        y (int): Координата y заданной точки.
        image_name (str): Имя файла изображения.

        Вывод:
        None
        """
        # Получаем яркость точки
        brightness = self.get_pixel_brightness(x, y, image_name)

        # Анализируем среднюю яркость для точки и ее соседей
        surrounding_brightness = self.get_surrounding_pixel_brightness(x, y, image_name)
        variance = self.dispersion_by_brightness_list(surrounding_brightness)

        # Выводим информацию
        print(f"Координаты точки: ({x}, {y}) Яркость: {brightness} Дисперсия: {variance}")

    def analyze_points_from_file(self, file_name, image_name):
        """
        Анализирует яркость и дисперсию для всех точек, полученных из текстового файла.

        Аргументы:
        file_name (str): Имя текстового файла с координатами точек.
        image_name (str): Имя файла изображения.

        Вывод:
        None
        """
        # Получаем список точек из текстового файла
        points = self.get_points_from_file(file_name)

        # Проходим по каждой точке и анализируем ее
        for point in points:
            x, y = point
            self.analyze_point(x, y, image_name)




