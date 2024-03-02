from PIL import Image
import os


class ImageCropper:
    def __init__(self, input_folder=os.path.join(os.getcwd(), "Input"), output_folder=os.path.join(os.getcwd(), "Input")):
        """
        Инициализирует объект ImageCropper.

        Параметры:
        - input_folder (строка): Путь к папке с входными изображениями. По умолчанию: папка "Input" в текущей директории.
        - output_folder (строка): Путь к папке, в которую будут сохранены обрезанные изображения. По умолчанию: папка "Output" в текущей директории.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder

    def crop_images(self):
        """
        Обрезает изображения в папке ввода и сохраняет их в папку вывода.

        Извлекает изображения из папки ввода, обрезает каждое изображение до размера 360x240 пикселей и сохраняет в формате BMP в папку вывода.
        """
        if not os.path.exists(self.input_folder):
            print(f"Папка {self.input_folder} не существует.")
            return
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        files = os.listdir(self.input_folder)
        for file in files:
            if file.endswith(".JPG"):
                img_path = os.path.join(self.input_folder, file)
                img = Image.open(img_path)

                width, height = img.size
                left = (width - 360) // 2
                top = (height - 240) // 2
                right = left + 360
                bottom = top + 240

                cropped_img = img.crop((left, top, right, bottom))

                # Сохраняем изображение в формате BMP
                output_path = os.path.join(self.output_folder, os.path.splitext(file)[0] + ".bmp")
                cropped_img.save(output_path)
                print(f"Изображение {file} успешно обрезано и сохранено в {self.output_folder}")

    def rename_output_images(self, name_of_image_for_out):
        """
        Переименовывает изображения в папке вывода.

        Переименовывает каждое изображение в папке вывода, добавляя к нему указанное имя и уникальный индекс.

        Параметры:
        - name_of_image_for_out (строка): Префикс, который будет добавлен к каждому новому имени изображения.
        """
        if not os.path.exists(self.output_folder):
            print(f"Папка {self.output_folder} не существует.")
            return

        files = os.listdir(self.output_folder)
        i = 1
        for file in files:
            if file.endswith(".bmp"):
                old_path = os.path.join(self.output_folder, file)
                new_name = f"{name_of_image_for_out}{i}.bmp"
                new_path = os.path.join(self.output_folder, new_name)
                os.rename(old_path, new_path)
                print(f"Файл {file} успешно переименован в {new_name}")
                i += 1
        self.move_jpg_to_deleted()

    def move_jpg_to_deleted(self):
        """
        Перемещает все JPG файлы из каталога ввода в каталог deleted.

        Перемещает все файлы с расширением ".JPG" из каталога ввода в каталог "deleted".
        """
        if not os.path.exists(self.input_folder):
            print(f"Папка {self.input_folder} не существует.")
            return

        deleted_folder = os.path.join(os.path.dirname(self.input_folder), "deleted")
        if not os.path.exists(deleted_folder):
            os.makedirs(deleted_folder)

        files = os.listdir(self.input_folder)
        for file in files:
            if file.endswith(".JPG"):
                old_path = os.path.join(self.input_folder, file)
                new_path = os.path.join(deleted_folder, file)
                os.rename(old_path, new_path)
                print(f"Файл {file} успешно перемещен в {deleted_folder}")