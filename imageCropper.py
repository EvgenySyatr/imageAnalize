from PIL import Image
import os


class ImageCropper:
    def __init__(self):
        # Пути к папкам Input и Output
        self.input_folder = os.path.join(os.getcwd(), "Input")
        self.output_folder = os.path.join(os.getcwd(), "Output")

    def crop_images(self):
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
