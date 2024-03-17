from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


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
        """
        Получает яркость пикселя изображения по его координатам.

        Аргументы:
        - x (int): Координата x пикселя.
        - y (int): Координата y пикселя.
        - image_name (str): Имя изображения.

        Возвращает:
        - brightness (int): Яркость пикселя (значение от 0 до 255).
        """
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

    def get_background_dispersion(self, border_width = 80):
        """
        Находит максимальную дисперсию для точек фона в области шириной 10 пикселей сверху изображения.

        Возвращает:
        float: Максимальная дисперсия для точек фона.
        """
        # Определяем размеры изображения
        width, height = self.image.size

        background_dispersion_list = []

        # Проходим по области верхнего края изображения
        for x in tqdm(range(0, width - 1), desc="Processing rows"):
            for y in range(border_width):
                # print(f"[ {x}; {y} ]")
                # Для каждой точки в области верхнего края получаем яркость окружающих пикселей
                surrounding_brightness = self.get_surrounding_pixel_brightness(x, y, self.image_name)

                # Вычисляем дисперсию яркостей окружающих пикселей
                dispersion = self.dispersion_by_brightness_list(surrounding_brightness)

                # Добавляем дисперсию в список
                background_dispersion_list.append(dispersion)

        # Находим максимальную дисперсию
        max_dispersion = max(background_dispersion_list)
        # self.visualize_explored_area(border_width)
        return max_dispersion

    def visualize_explored_area(self, border_width = 10):
        """
        Визуализирует область, которая была исследована для поиска максимальной дисперсии.

        Возвращает:
        None
        """
        # Создаем изображение для визуализации
        explored_area = np.zeros_like(self.image)

        # Определяем размеры изображения
        width, height = self.image.size

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

    def save_explored_area(self, border_width=10, output_file="BackgroungArea.jpg"):
        """
        Сохраняет исследованную область в новом файле с сохранением яркости и цвета каждого пикселя.

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


        # Проходим по области верхнего края изображения
        for x in range(0, width):
            for y in range(border_width):
                # Получаем яркость и цвет пикселя из оригинального изображения
                brightness = self.get_pixel_brightness(x, y, self.image_name)
                color = self.image.getpixel((x, y))
                # Устанавливаем яркость и цвет пикселя в исследованной области
                explored_area.putpixel((x, y), color)

        # Сохраняем изображение
        explored_area.save(output_file)
        with Image.open(output_file) as img:
            # Показываем изображение в консоли
            img.show()

    def track_max_dispersion_points(self, dispersion_background, step_size=6, border_width=40):
        """
        Отслеживает максимальные точки дисперсии на изображении.

        Аргументы:
        - dispersion_background (float): Значение дисперсии фона.
        - step_size (int): Размер шага при перемещении по вертикали.

        Возвращает:
        - max_dispersion_points (list): Список точек с максимальной дисперсией.
        - brightness_list (list): Список яркостей пикселей для каждой найденной точки.
        - dispersion_list (list): Список дисперсий для каждой найденной точки.
        - brightness_list_5x5 (list): Список яркостей пикселей (для 5x5 окрестности) для каждой найденной точки.
        - dispersion_list_5x5 (list): Список дисперсий (для 5x5 окрестности) для каждой найденной точки.
        """
        step_size = step_size
        max_dispersion_points = []  # Список для хранения точек с максимальной дисперсией
        brightness_list = []
        dispersion_list = []

        # F5
        brightness_list_5x5 = []
        dispersion_list_5x5 = []

        # Определяем размеры изображения
        width = 178
        height = 238
        border = border_width
        # Проходим по каждой вертикальной полосе изображения
        for y in tqdm(range(border, height - border, step_size), desc="Processing rows from left to right"):
            max_dispersion = 0  # Максимальная дисперсия в текущей полосе
            max_dispersion_point = None  # Точка с максимальной дисперсией в текущей полосе

            # Начинаем с верхней части изображения и двигаемся вниз с шагом step_size
            for x in range(border, width):
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

        ###################################################################################
        first_point_x_left = max_dispersion_points[0][0]  # x-координата первой точки
        last_point_x_left = max_dispersion_points[-1][0]  # x-координата последней точки
        first_point_y_left = max_dispersion_points[0][1]  # y-координата первой точки
        last_point_y_left = max_dispersion_points[-1][1]  # y-координата последней точки
        # Они нужны, чтобы потом сверху вниз и снизу вверх пойти
        ####################################################################################
        # Добавляем точки справа налево
        right_side_cort = self.track_max_dispersion_points_From_Right_To_Left(dispersion_background, step_size)
        #####################################################################################
        first_point_x_right = right_side_cort[0][0][0]  # x-координата первой точки
        last_point_x_right = right_side_cort[0][-1][0]  # x-координата последней точки
        # Они нужны, чтобы потом сверху вниз и снизу вверх пойти
        #####################################################################################
        top_border = first_point_x_right - first_point_x_left
        bottom_border = last_point_x_right - last_point_x_left
        ######################################################################################
        # Добавляем остальные
        vertical_points = self.track_max_dispersion_points_From_Top_To_Bottom_And_Bottom_To_Top(
            dispersion_background, step_size, top_border, bottom_border,
            first_point_x_left, last_point_x_left, first_point_y_left, last_point_y_left)
        ######################################################################################)
        max_dispersion_points += right_side_cort[0]
        brightness_list += right_side_cort[1]
        dispersion_list += right_side_cort[2]
        brightness_list_5x5 += right_side_cort[3]
        dispersion_list_5x5 += right_side_cort[4]

        max_dispersion_points += vertical_points[0]
        brightness_list += vertical_points[1]
        dispersion_list += vertical_points[2]
        brightness_list_5x5 += vertical_points[3]
        dispersion_list_5x5 += vertical_points[4]

        # записываем в выходной файл координаты точек
        self.write_coordinates_to_file(max_dispersion_points)
        clear_console()
        return max_dispersion_points, brightness_list, dispersion_list, brightness_list_5x5, dispersion_list_5x5

    def track_max_dispersion_points_From_Right_To_Left(self, dispersion_background, step_size=6):
        """
        Отслеживает максимальные точки дисперсии на изображении, двигаясь справа налево.

        Аргументы:
        - dispersion_background (float): Значение дисперсии фона.
        - step_size (int): Размер шага при перемещении по вертикали.

        Возвращает:
        - max_dispersion_points (list): Список точек с максимальной дисперсией.
        - brightness_list (list): Список яркостей пикселей для каждой найденной точки.
        - dispersion_list (list): Список дисперсий для каждой найденной точки.
        - brightness_list_5x5 (list): Список яркостей пикселей (для 5x5 окрестности) для каждой найденной точки.
        - dispersion_list_5x5 (list): Список дисперсий (для 5x5 окрестности) для каждой найденной точки.
        """
        max_dispersion_points = []
        brightness_list = []
        dispersion_list = []
        brightness_list_5x5 = []
        dispersion_list_5x5 = []
        # Определяем размеры изображения
        width = 178
        height = 238
        border = 40
        # Проходим по каждой вертикальной полосе изображения
        for y in tqdm(range(border, height - border, step_size), desc="Processing rows from right to left"):
            max_dispersion = 0  # Максимальная дисперсия в текущей полосе
            max_dispersion_point = None  # Точка с максимальной дисперсией в текущей полосе

            # Начинаем с верхней части изображения и двигаемся вниз с шагом step_size
            for x in range(359 - border, 180, -1):
                # Проверяем, находятся ли координаты в пределах изображения
                if 180 <= x < 358 and 0 <= y < height:
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

        return max_dispersion_points, brightness_list, dispersion_list, brightness_list_5x5, dispersion_list_5x5

    def track_max_dispersion_points_From_Top_To_Bottom_And_Bottom_To_Top(self, dispersion_background, step_size,
                                                                         top_border, bottom_border,
                                                                         top_start, bottom_start,
                                                                         first_point_y_left, last_point_y_left):
        """
        Отслеживает максимальные точки дисперсии на изображении, двигаясь сверху вниз и снизу вверх по определенным полосам.

        Аргументы:
        - dispersion_background (float): Значение дисперсии фона.
        - step_size (int): Размер шага при перемещении по вертикали.
        - top_border (int): Верхняя граница для движения сверху вниз.
        - bottom_border (int): Нижняя граница для движения снизу вверх.

        Возвращает:
        - max_dispersion_points (list): Список точек с максимальной дисперсией.
        - brightness_list (list): Список яркостей пикселей для каждой найденной точки.
        - dispersion_list (list): Список дисперсий для каждой найденной точки.
        - brightness_list_5x5 (list): Список яркостей пикселей (для 5x5 окрестности) для каждой найденной точки.
        - dispersion_list_5x5 (list): Список дисперсий (для 5x5 окрестности) для каждой найденной точки.
        """

        ###############################
        max_dispersion_points = []
        brightness_list = []
        dispersion_list = []
        brightness_list_5x5 = []
        dispersion_list_5x5 = []
        ###############################

        # Определяем размеры изображения
        y_start = first_point_y_left
        y_end = last_point_y_left
        height = 238
        # Проходим по каждой вертикальной полосе изображения сверху вниз
        for x in range(top_start, top_start + top_border + 1, step_size):            # Проходим по каждой горизонтальной полосе изображения слева направо
            max_dispersion = 0  # Максимальная дисперсия в текущей полосе
            # print(f"Максимум дисперсии : {max_dispersion}")
            max_dispersion_point = None  # Точка с максимальной дисперсией в текущей полосе
            # print(f"Максимум дисперсии : {max_dispersion_point}")
            for y in range(0, y_start + 1):
                # Вычисляем дисперсию яркостей окружающих пикселей
                dispersion = self.dispersion_by_brightness_list(self.get_surrounding_pixel_brightness(x, y, self.image_name))
                if dispersion > dispersion_background:
                    if dispersion > max_dispersion:
                        max_dispersion = dispersion
                        max_dispersion_point = (x, y)
                    else:
                        pointX = x
                        pointY = y
                        max_dispersion_point = (x, y)
                        max_dispersion_points.append(max_dispersion_point)
                        brightness_list.append(self.analyze_pixel_and_surroundings(pointX, pointY, self.image_name))
                        brightness_list_5x5.append(self.analyze_pixel_and_surroundings_25(pointX, pointY, self.image_name))
                        # Получаем яркость окружающих пикселей для измененной текущей точки
                        surrounding_brightness = self.get_surrounding_pixel_brightness(pointX, pointY, self.image_name)
                        surrounding_brightness_5x5 = self.get_surrounding_pixel_brightness_25(pointX, pointY,
                                                                                              self.image_name)
                        # Вычисляем дисперсию яркостей окружающих пикселей
                        dispersion = self.dispersion_by_brightness_list(surrounding_brightness)
                        dispersion_list.append(dispersion)
                        dispersion_5x5 = self.dispersion_by_brightness_list(surrounding_brightness_5x5)
                        dispersion_list_5x5.append(dispersion_5x5)
                        break

        # Проходим по каждой вертикальной полосе изображения снизу вверх
        for x in range(bottom_start, bottom_start + bottom_border + 1, step_size):  # Проходим по каждой горизонтальной полосе изображения слева направо
            max_dispersion = 0  # Максимальная дисперсия в текущей полосе
            # print(f"Максимум дисперсии : {max_dispersion}")
            max_dispersion_point = None  # Точка с максимальной дисперсией в текущей полосе
            # print(f"Максимум дисперсии : {max_dispersion_point}")
            for y in range(height, y_end + 1, -1):
                # Вычисляем дисперсию яркостей окружающих пикселей
                dispersion = self.dispersion_by_brightness_list(
                    self.get_surrounding_pixel_brightness(x, y, self.image_name))
                if dispersion > dispersion_background:
                    print(f"{x} {y}")
                    print(f"Дисперсия : {dispersion}")
                    if dispersion > max_dispersion:
                        max_dispersion = dispersion
                        max_dispersion_point = (x, y)
                        print(f"Максимальная дисперсия {max_dispersion_point}")
                    else:
                        pointX = x
                        pointY = y
                        max_dispersion_point = (x, y)
                        max_dispersion_points.append(max_dispersion_point)
                        brightness_list.append(
                            self.analyze_pixel_and_surroundings(pointX, pointY, self.image_name))
                        brightness_list_5x5.append(
                            self.analyze_pixel_and_surroundings_25(pointX, pointY, self.image_name))
                        # Получаем яркость окружающих пикселей для измененной текущей точки
                        surrounding_brightness = self.get_surrounding_pixel_brightness(pointX, pointY,
                                                                                       self.image_name)
                        surrounding_brightness_5x5 = self.get_surrounding_pixel_brightness_25(pointX, pointY,
                                                                                              self.image_name)
                        # Вычисляем дисперсию яркостей окружающих пикселей
                        dispersion = self.dispersion_by_brightness_list(surrounding_brightness)
                        dispersion_list.append(dispersion)
                        dispersion_5x5 = self.dispersion_by_brightness_list(surrounding_brightness_5x5)
                        dispersion_list_5x5.append(dispersion_5x5)
                        break

        # self.write_coordinates_to_file(max_dispersion_points) # Убрать потом
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



def clear_console():
    """
    Очищает консольный вывод в зависимости от операционной системы.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
