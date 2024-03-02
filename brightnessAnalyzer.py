from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt


class PixelBrightnessAnalyzer:
    def __init__(self, input_folder, image_name="Image1.bmp", points_file="points1.txt", output_folder="Output"):
        self.points_file = points_file
        self.image_name = image_name
        self.input_folder = input_folder
        self.image = Image.open(os.path.join(input_folder, image_name))
        self.output_folder = output_folder

    def get_points_from_points_file(self):
        """
        Получает список точек из файла pointsN.txt.

        Возвращает:
        - points (list): Список координат точек.
        """
        points = []
        file_path = self.points_file
        # Открываем файл pointsN.txt
        with open(file_path, "r") as file:
            # Читаем строки из файла
            lines = file.readlines()
            # Начиная со второй строки, обрабатываем каждую строку
            for line in lines[1:]:
                # Разбиваем строку на координаты x и y
                x, y = map(int, line.strip().split())
                points.append((x, y))

        return points

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

    def get_surrounding_pixel_brightness_25(self, x, y, image_name):
        """
        Получает яркость 25 соседних пикселей вокруг заданной точки.

        Аргументы:
        x (int): Координата x центрального пикселя.
        y (int): Координата y центрального пикселя.
        image_name (str): Имя файла изображения.

        Возвращает:
        list: Список со значениями яркости 25 соседних пикселей вокруг центрального пикселя.
        """
        surrounding_pixels_brightness = []

        # Координаты всех 25 пикселей (включая изначальную точку)
        neighbors_coordinates = [
            (x - 2, y - 2), (x - 1, y - 2), (x, y - 2), (x + 1, y - 2), (x + 2, y - 2),
            (x - 2, y - 1), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 2, y - 1),
            (x - 2, y), (x - 1, y), (x, y), (x + 1, y), (x + 2, y),
            (x - 2, y + 1), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1),
            (x - 2, y + 2), (x - 1, y + 2), (x, y + 2), (x + 1, y + 2), (x + 2, y + 2)
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

    def analyze_pixel_and_surroundings_25(self, x, y, image_name):
        """
        Анализирует среднюю яркость для заданной точки и ее 25 соседей.

        Аргументы:
        x (int): Координата x заданной точки.
        y (int): Координата y заданной точки.
        image_name (str): Имя файла изображения.

        Возвращает:
        float: Средняя яркость заданной точки и ее 25 соседей.
        """
        # Получаем значения яркости заданной точки и ее 25 соседей
        surrounding_brightness = self.get_surrounding_pixel_brightness_25(x, y, image_name)

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
        brightness, dispersion
        """
        # Получаем яркость точки
        brightness = self.get_pixel_brightness(x, y, image_name)

        # Анализируем среднюю яркость для точки и ее соседей
        surrounding_brightness = self.get_surrounding_pixel_brightness(x, y, image_name)
        dispersion = self.dispersion_by_brightness_list(surrounding_brightness)

        # Выводим информацию
        print(f"Координаты точки: ({x}, {y}) Яркость: {brightness} Дисперсия: {dispersion}")
        return brightness, dispersion

    def analyze_points_from_file(self, file_name, image_name):
        """
        Анализирует яркость и дисперсию для всех точек, полученных из текстового файла.

        Аргументы:
        file_name (str): Имя текстового файла с координатами точек.
        image_name (str): Имя файла изображения.

        Вывод:
        brightList, dispList
        """
        # Получаем список точек из текстового файла
        points = self.get_points_from_file(file_name)
        brightList = []
        dispList = []
        # Проходим по каждой точке и анализируем ее
        for point in points:
            x, y = point
            currBright, currDisp = self.analyze_point(x, y, image_name)
            brightList.append(currBright)
            dispList.append(currDisp)

        return brightList, dispList

    def get_background_dispersion(self):
        """
        Находит максимальную дисперсию для точек фона в области шириной 10 пикселей вверху изображения.

        Возвращает:
        float: Максимальная дисперсия для точек фона.
        """
        # Определяем размеры изображения
        width, height = self.image.size

        # Ширина области по краю, которую мы исследуем (например, 10 пикселей)
        border_width = 10

        # Создаем список для хранения дисперсий фона
        background_dispersion_list = []

        # Проходим по области верхнего края изображения
        for x in range(border_width, width - border_width):
            for y in range(border_width):
                print(f"[ {x}; {y} ]")
                # Для каждой точки в области верхнего края получаем яркость окружающих пикселей
                surrounding_brightness = self.get_surrounding_pixel_brightness(x, y, self.image_name)

                # Вычисляем дисперсию яркостей окружающих пикселей
                dispersion = self.dispersion_by_brightness_list(surrounding_brightness)

                # Добавляем дисперсию в список
                background_dispersion_list.append(dispersion)

        # Находим максимальную дисперсию
        max_dispersion = max(background_dispersion_list)

        return max_dispersion

    def visualize_explored_area(self):
        """
        Визуализирует область, которая была исследована для поиска максимальной дисперсии.

        Возвращает:
        None
        """
        # Создаем изображение для визуализации
        explored_area = np.zeros_like(self.image)

        # Определяем размеры изображения
        width, height = self.image.size

        # Ширина области по краю, которую мы исследуем (например, 10 пикселей)
        border_width = 10

        # Проходим по области верхнего края изображения
        for x in range(border_width, width - border_width):
            for y in range(border_width):
                # Метим точку на изображении как исследованную
                explored_area[y, x] = 255  # Белый цвет

        # Визуализируем исследованную область
        plt.imshow(explored_area, cmap='gray')
        plt.title('Explored Area')
        plt.axis('off')
        plt.show()

    def save_explored_area(self, output_file):
        """
        Сохраняет исследованную область в новом файле .bmp с сохранением яркости и цвета каждого пикселя.

        Аргументы:
        output_file (str): Имя выходного файла.

        Возвращает:
        None
        """
        # Создаем копию изображения для визуализации
        explored_area = Image.new("RGB", self.image.size)

        # Определяем размеры изображения
        width, height = self.image.size

        # Ширина области по краю, которую мы исследуем (например, 10 пикселей)
        border_width = 10

        # Проходим по области верхнего края изображения
        for x in range(border_width, width - border_width):
            for y in range(border_width):
                # Получаем яркость и цвет пикселя из оригинального изображения
                brightness = self.get_pixel_brightness(x, y, self.image_name)
                color = self.image.getpixel((x, y))
                # Устанавливаем яркость и цвет пикселя в исследованной области
                explored_area.putpixel((x, y), color)

        # Сохраняем изображение в файле .bmp
        explored_area.save(output_file)

    def track_max_dispersion_points(self, dispersion_background, step_size=6):
        """
        Отслеживает максимальные точки дисперсии на изображении.

        Аргументы:
        dispersion_background (float): Значение дисперсии фона.
        step_size (int): Размер шага при перемещении по вертикали.

        Возвращает:
        list: Список точек с максимальной дисперсией.
        """
        step_size = step_size
        max_dispersion_points = []  # Список для хранения точек с максимальной дисперсией
        brightness_list = []
        dispersion_list = []

        # F5
        brightness_list_5x5 = []
        dispersion_list_5x5 = []

        # Определяем размеры изображения
        width = 179
        height = 239
        # Проходим по каждой вертикальной полосе изображения
        for y in range(0, height, step_size):
            max_dispersion = 0  # Максимальная дисперсия в текущей полосе
            max_dispersion_point = None  # Точка с максимальной дисперсией в текущей полосе

            # Начинаем с верхней части изображения и двигаемся вниз с шагом step_size
            for x in range(width):
                # Проверяем, находятся ли координаты в пределах изображения
                if 0 <= x < width and 0 <= y < height:
                    # Получаем яркость окружающих пикселей для текущей точки
                    surrounding_brightness = self.get_surrounding_pixel_brightness(x, y, self.image_name)
                    # Вычисляем дисперсию яркостей окружающих пикселей
                    dispersion = self.dispersion_by_brightness_list(surrounding_brightness)
                    # print(f"[ {x};{y} ] {dispersion}")
                    # Если текущая дисперсия больше дисперсии фона, начинаем отслеживать максимум
                    if dispersion > dispersion_background:
                        if dispersion > max_dispersion:
                            max_dispersion = dispersion
                            max_dispersion_point = (x, y)

                        # Пропускаем остальные точки данного уровня
                        break

            # Если найден максимум на текущем уровне, добавляем его в список
            if max_dispersion_point is not None:
                pointX = max_dispersion_point[0]
                pointY = max_dispersion_point[1]
                # Для возможности сместить точку влево, вправо или вниз
                next_point = (pointX, pointY)
                max_dispersion_points.append(next_point)

                brightness_list.append(self.analyze_pixel_and_surroundings(pointX, pointY, self.image_name))
                brightness_list_5x5.append(self.analyze_pixel_and_surroundings_25(pointX, pointY, self.image_name))
                # Получаем яркость окружающих пикселей для измененной текущей точки
                surrounding_brightness = self.get_surrounding_pixel_brightness(pointX, pointY, self.image_name)
                surrounding_brightness_5x5 = self.get_surrounding_pixel_brightness_25(pointX, pointY, self.image_name)
                # Вычисляем дисперсию яркостей окружающих пикселей
                dispersion = self.dispersion_by_brightness_list(surrounding_brightness)
                dispersion_list.append(dispersion)
                dispersion_5x5 = self.dispersion_by_brightness_list(surrounding_brightness_5x5)
                dispersion_list_5x5.append(dispersion_5x5)
                print(f"[ {pointX};{pointY} ] {self.analyze_pixel_and_surroundings(pointX, pointY, self.image_name)} {dispersion} "
                      f"| F5 | {self.analyze_pixel_and_surroundings_25(pointX, pointY, self.image_name)} {dispersion_5x5}")  # Выводим координаты точки

        right_side_cort = self.track_max_dispersion_points_From_Right_To_Left(dispersion_background, step_size)
        max_dispersion_points += right_side_cort[0]
        brightness_list += right_side_cort[1]
        dispersion_list += right_side_cort[2]
        brightness_list_5x5 += right_side_cort[3]
        dispersion_list_5x5 += right_side_cort[4]

        # записываем в выходной файл координаты точек
        self.write_coordinates_to_file(max_dispersion_points)
        return max_dispersion_points, brightness_list, dispersion_list, brightness_list_5x5, dispersion_list_5x5

    def track_max_dispersion_points_From_Right_To_Left(self, dispersion_background, step_size=6):
        max_dispersion_points = []
        brightness_list = []
        dispersion_list = []
        brightness_list_5x5 = []
        dispersion_list_5x5 = []
        # Определяем размеры изображения
        width = 179
        height = 239
        # Проходим по каждой вертикальной полосе изображения
        for y in range(0, height, step_size):
            max_dispersion = 0  # Максимальная дисперсия в текущей полосе
            max_dispersion_point = None  # Точка с максимальной дисперсией в текущей полосе

            # Начинаем с верхней части изображения и двигаемся вниз с шагом step_size
            for x in range(359, 180, -1):
                # Проверяем, находятся ли координаты в пределах изображения
                if 180 <= x < 359 and 0 <= y < height:
                    # Получаем яркость окружающих пикселей для текущей точки
                    surrounding_brightness = self.get_surrounding_pixel_brightness(x, y, self.image_name)

                    # Вычисляем дисперсию яркостей окружающих пикселей
                    dispersion = self.dispersion_by_brightness_list(surrounding_brightness)
                    # print(f"[ {x};{y} ] {dispersion}")
                    # Если текущая дисперсия больше дисперсии фона, начинаем отслеживать максимум
                    if dispersion > dispersion_background:
                        if dispersion > max_dispersion:
                            max_dispersion = dispersion
                            max_dispersion_point = (x, y)

                        # Пропускаем остальные точки данного уровня
                        break

            # Если найден максимум на текущем уровне, добавляем его в список
            if max_dispersion_point is not None:
                pointX = max_dispersion_point[0]
                pointY = max_dispersion_point[1]
                # Для возможности сместить точку влево, вправо или вниз
                next_point = (pointX, pointY)
                max_dispersion_points.append(next_point)

                brightness_list.append(self.analyze_pixel_and_surroundings(pointX, pointY, self.image_name))
                brightness_list_5x5.append(self.analyze_pixel_and_surroundings_25(pointX, pointY, self.image_name))
                # Получаем яркость окружающих пикселей для измененной текущей точки
                surrounding_brightness = self.get_surrounding_pixel_brightness(pointX, pointY, self.image_name)
                surrounding_brightness_5x5 = self.get_surrounding_pixel_brightness_25(pointX, pointY, self.image_name)
                # Вычисляем дисперсию яркостей окружающих пикселей
                dispersion = self.dispersion_by_brightness_list(surrounding_brightness)
                dispersion_list.append(dispersion)
                dispersion_5x5 = self.dispersion_by_brightness_list(surrounding_brightness_5x5)
                dispersion_list_5x5.append(dispersion_5x5)
                print(
                    f"[ {pointX};{pointY} ] {self.analyze_pixel_and_surroundings(pointX, pointY, self.image_name)} {dispersion} "
                    f"| F5 | {self.analyze_pixel_and_surroundings_25(pointX, pointY, self.image_name)} {dispersion_5x5}")  # Выводим координаты точки

        return max_dispersion_points, brightness_list, dispersion_list, brightness_list_5x5, dispersion_list_5x5

    def fill_lists(self, point_list):
        """
        Заполняет списки яркости и дисперсии для указанных точек и их 5x5 окрестностей.

        Аргументы:
        - point_list (list): Список координат точек [(x1, y1), (x2, y2), ...].
        - image_name (str): Имя файла изображения.

        Возвращает:
        - point_list (list): Список координат точек.
        - brightness_list (list): Список значений яркости для каждой точки.
        - dispersion_list (list): Список значений дисперсии для каждой точки.
        - brightness_list_5x5 (list): Список значений яркости для каждой 5x5 окрестности.
        - dispersion_list_5x5 (list): Список значений дисперсии для каждой 5x5 окрестности.
        """
        brightness_list = []
        dispersion_list = []
        brightness_list_5x5 = []
        dispersion_list_5x5 = []

        for point in point_list:
            pointX, pointY = point
            # Получаем яркость и дисперсию для текущей точки
            brightness_list.append(self.analyze_pixel_and_surroundings(pointX, pointY, self.image_name))
            brightness_list_5x5.append(self.analyze_pixel_and_surroundings_25(pointX, pointY, self.image_name))
            # Получаем яркость окружающих пикселей для измененной текущей точки
            surrounding_brightness = self.get_surrounding_pixel_brightness(pointX, pointY, self.image_name)
            surrounding_brightness_5x5 = self.get_surrounding_pixel_brightness_25(pointX, pointY, self.image_name)
            # Вычисляем дисперсию яркостей окружающих пикселей
            dispersion = self.dispersion_by_brightness_list(surrounding_brightness)
            dispersion_list.append(dispersion)
            dispersion_5x5 = self.dispersion_by_brightness_list(surrounding_brightness_5x5)
            dispersion_list_5x5.append(dispersion_5x5)

        return point_list, brightness_list, dispersion_list, brightness_list_5x5, dispersion_list_5x5

    def write_coordinates_to_file(self, coordinates):
        """
        Записывает координаты точек в файл.

        Аргументы:
        coordinates (list): Список координат точек.

        Возвращает:
        None
        """
        total_points = len(coordinates)
        file_path = os.path.join(self.output_folder, self.points_file)
        file_path = os.path.join(os.getcwd(), file_path)
        # Создаем папку Output, если ее еще нет
        os.makedirs(os.path.join(os.getcwd(), self.output_folder), exist_ok=True)

        print(f"Данные запишем в файл {file_path}")
        with open(file_path, "w") as file:
            file.write(f"{str(total_points).zfill(4)}\n")
            for coord in coordinates:
                x_str = str(coord[0]).zfill(4)  # Добавляем нули спереди до 4 цифр
                y_str = str(coord[1]).zfill(4)  # Добавляем нули спереди до 4 цифр
                file.write(f"{x_str} {y_str}\n")