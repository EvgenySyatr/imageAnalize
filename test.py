import brightnessAnalyzer as ba
import os

bmp_filename = "Image1.bmp"
image_name = os.path.splitext(bmp_filename)[0]  # Получаем имя файла без расширения
points_file = f"points1.txt"  # Генерируем имя файла для сохранения точек
analyzer = ba.PixelBrightnessAnalyzer("Input", image_name + ".bmp", points_file, "Output")
analyzer.track_max_dispersion_points_From_Top_To_Bottom_And_Bottom_To_Top(49, 4, 200, 200, 80, 80, 40, 238 - 40)
