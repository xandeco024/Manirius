import os
from PIL import Image

def reduce_frames(image_folder, output_folder, frame_rate):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(0, len(images), frame_rate):
        img = Image.open(os.path.join(image_folder, images[i]))
        rgb_img = img.convert('RGB')
        rgb_img.save(os.path.join(output_folder, f"frame_{i//frame_rate}.jpg"), "JPEG")

# Uso da função
reduce_frames('Sprites/Splash/original', 'Sprites/Splash/reduced', 2)
