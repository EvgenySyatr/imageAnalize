from PIL import Image
import os

class BlackAndWhiteConverter:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def convert_to_black_and_white(self):
        if not os.path.exists(self.input_folder):
            print(f"Папка {self.input_folder} не существует.")
            return
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        files = os.listdir(self.input_folder)
        for file in files:
            if file.endswith(".bmp"):
                img_path = os.path.join(self.input_folder, file)
                img = Image.open(img_path)

                # Преобразуем изображение в черно-белое
                bw_img = img.convert("L")

                # Сохраняем черно-белое изображение
                output_path = os.path.join(self.output_folder, file)
                bw_img.save(output_path)
                print(f"Изображение {file} успешно преобразовано в черно-белое и сохранено в {self.output_folder}")

