from PIL import Image
import os
from ExcelHandler import ExcelHandler
import brightnessAnalyzer as ba
import numpy as np
import matplotlib.pyplot as plt


class workWithFiles():

    def get_points_from_points_file(self, points_file):
        """
        Получает список точек из файла pointsN.txt.

        Возвращает:
        - points (list): Список координат точек.
        """
        points = []
        file_path = points_file
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

    def visualize_explored_area(self, border_width=10):
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





    def extract_number(self, filename):
        return int(filename.split('Image')[1].split('.')[0])

    def write_tuple_F3_data_to_file(self, tuple_data, filename):
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

    def write_tuple_F5_data_to_file(self, tuple_data, filename):
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

    def clear_files(self, filenames):
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

    def final_EXPORT_DATAF3F5_TO_EXEL(self, exel_file="CopyOfWorkTable.xlsx"):
        """
        Заполняет таблицу значениями из outputF3.txt и outputF5.txt
        :param exel_file:
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

        data = self.read_data_from_file("outputF3.txt")
        ex = ExcelHandler(exel_file)
        # X
        list_input = [data[i][0][0] for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 1, 4, 983)
        # Y
        list_input = [data[i][0][1] for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 2, 4, 983)
        # M3
        list_input = [int(data[i][1]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 3, 4, 983)
        # D3
        list_input = [int(data[i][2]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 4, 4, 983)
        data_addition = self.read_data_from_file("outputF5.txt")
        # M5
        list_input = [int(data_addition[i][1]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 5, 4, 983)
        # D5
        list_input = [int(data_addition[i][2]) for i in range(len(data))]  # Берем значения из первой координаты точки
        ex.fill_column(list_input, 6, 4, 983)

    def read_data_from_file(self, filename):
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
