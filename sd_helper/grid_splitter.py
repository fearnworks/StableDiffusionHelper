import cv2
import os

def calculate_aspect_ratio(width, height):
    return round(width / height, 2)

def find_closest_aspect_ratio(aspect_ratio, aspect_ratio_map):
    closest_aspect_ratio = min(aspect_ratio_map.keys(), key=lambda k: abs(k - aspect_ratio))
    return closest_aspect_ratio

def split_image_into_grid(image_path, output_dir, aspect_ratio_map):
    img = cv2.imread(image_path)
    img_height, img_width, _ = img.shape
    aspect_ratio = calculate_aspect_ratio(img_width, img_height)
    closest_aspect_ratio = find_closest_aspect_ratio(aspect_ratio, aspect_ratio_map)
    rows, cols = aspect_ratio_map[closest_aspect_ratio]
    
    cell_width = img_width // cols
    cell_height = img_height // rows
    
    sub_dir = f"{closest_aspect_ratio}_r{rows}_c{cols}"
    sub_output_dir = os.path.join(output_dir, sub_dir)
    
    if not os.path.exists(sub_output_dir):
        os.makedirs(sub_output_dir)
        
    for i in range(rows):
        for j in range(cols):
            y1 = i * cell_height
            y2 = (i + 1) * cell_height
            x1 = j * cell_width
            x2 = (j + 1) * cell_width
            
            cropped_cell = img[y1:y2, x1:x2]
            cell_filename = f"{os.path.basename(image_path).split('.')[0]}_r{i+1}_c{j+1}.png"
            cell_filepath = os.path.join(sub_output_dir, cell_filename)
            cv2.imwrite(cell_filepath, cropped_cell)

def split_images_in_directory(input_dir, output_dir):
    aspect_ratio_map = {
        0.67: (2, 2),  # Closest for 2:3 aspect ratio
        0.56: (2, 2),  # Closest for 9:16 aspect ratio
        1.0 : (2, 2),  # Closest for 1:1 aspect ratio
        1.33: (2, 2),  # Closest for 4:3 aspect ratio
        1.78: (2, 2)   # Closest for 16:9 aspect ratio
    }
    
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(input_dir, filename)
            split_image_into_grid(filepath, output_dir, aspect_ratio_map)