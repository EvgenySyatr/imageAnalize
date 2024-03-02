import imageCropper as ic
import blackWhiteConverter as bwc
import brightnessAnalyzer as ba


# Создаем экземпляр класса ImageCropper
# cropper = ic.ImageCropper()
# Вызываем метод crop_images
# cropper.crop_images()

# Пути к папкам Input и Output
input_folder = "Input"
output_folder = "Output"



# Создаем экземпляр класса BlackAndWhiteConverter
#converter = bwc.BlackAndWhiteConverter(input_folder, output_folder)
# Вызываем метод convert_to_black_and_white
#converter.convert_to_black_and_white()

analyzer = ba.PixelBrightnessAnalyzer(input_folder)

points_text = """
0008 0007
"""
x = 8
y = 7

file_name = "image2.bmp"
#points = analyzer.get_surrounding_pixel_brightness(x, y, file_name) #Яркость по точке центральной
#disp = analyzer.calculate_brightness_variance(x, y, file_name) # дисперсия по точке центральной
#print(f"0008 0007 Средняя яркость: {analyzer.analyze_pixel_and_surroundings(8, 7, file_name)} Средняя дисперсия: {disp}")


# print(analyzer.get_pixel_brightness(27, 21, "Image2.bmp"))
analyzer.analyze_points_from_file("points.txt", "Image1.bmp")