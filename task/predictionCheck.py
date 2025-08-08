import cv2
import random

def visualize_yolo_annotations(image_path, txt_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image {image_path}")
        return
    
    h, w = img.shape[:2]
    
    # Create a color map for different classes
    color_map = {}
    
    with open(txt_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) != 5:
                print(f"Skipping invalid line: {line}")
                continue
            
            try:
                class_id, x_center, y_center, box_w, box_h = map(float, parts)
            except ValueError:
                print(f"Skipping line with invalid numbers: {line}")
                continue
            
            # Generate or retrieve a unique color for each class
            if int(class_id) not in color_map:
                # Generate random color (but avoid too dark colors)
                color_map[int(class_id)] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            color = color_map[int(class_id)]
            
            # Convert YOLO to pixel coordinates
            x_center *= w
            y_center *= h
            box_w *= w
            box_h *= h
            xmin = int(x_center - box_w / 2)
            ymin = int(y_center - box_h / 2)
            xmax = int(x_center + box_w / 2)
            ymax = int(y_center + box_h / 2)
            
            # Draw bounding box
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)
            
            # Draw class label with background for better visibility
            label = f"Class {int(class_id)}"
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(img, (xmin, ymin - text_height - 10), (xmin + text_width, ymin), color, -1)
            cv2.putText(img, label, (xmin, ymin - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Display legend
    legend_y = 30
    for class_id, color in color_map.items():
        cv2.rectangle(img, (10, legend_y - 20), (30, legend_y), color, -1)
        cv2.putText(img, f"Class {class_id}", (40, legend_y - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        legend_y += 30
    
    # Show and save results
    cv2.imshow("YOLO Annotations with Class Colors", img)
    cv2.imwrite("annotated_image_colored.png", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
visualize_yolo_annotations("C:\\Users\\s66\\Desktop\\check annto\\536024944-SEPT-20_page_1.png", "output_file.txt")