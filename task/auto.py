import numpy as np
from collections import defaultdict

def auto_identify_labels(annotations):
   
    # Table = class with largest boxes (by area)
    table_class = max(annotations.keys(), key=lambda c: sum(w*h for _,_,w,h in annotations[c]))
    
    remaining = [c for c in annotations if c != table_class]
    if not remaining:
        raise ValueError("Only table class found")
    
    # Header = class with highest boxes (minimum y-center)
    header_class = min(remaining, key=lambda c: min(b[1] for b in annotations[c]))
    
    # Data = remaining classes   
    data_class = [c for c in remaining if c != header_class][0] if len(remaining) > 1 else header_class
    
    return {"table": table_class, "header": header_class, "data": data_class}

def annotate_remaining_cells(raw_data):
    """Extend table rows while respecting table boundaries"""
    # Parse annotations
    annotations = defaultdict(list)
    for line in raw_data.strip().split('\n'):                     # Removing empty lines if present
        if line.strip() and len(line.split()) == 5:
            class_id, *coords = map(float, line.split())
            annotations[int(class_id)].append(tuple(coords))
    
    # Detect labels
    try:
        labels = auto_identify_labels(annotations)
    except ValueError as e:
        return f"Error: {str(e)}"
    
    # Get table boundaries (using largest table box)
    table_boxes = annotations.get(labels['table'], [])
    if table_boxes:
        table_box = max(table_boxes, key=lambda b: b[2]*b[3])
        table_bottom = table_box[1] + table_box[3]/2  # y_center + height/2
    else:
        table_bottom = 1.0  # Fallback to image bottom if no table box
    
    # Get and sort data cells
    data_cells = sorted(annotations.get(labels['data'], []), key=lambda b: (b[1], b[0]))
    
    # Group into rows
    rows = []
    if data_cells:
        current_row = [data_cells[0]]
        for cell in data_cells[1:]:
            if abs(cell[1] - current_row[-1][1]) < 0.02:  # Similar y-coordinate
                current_row.append(cell)
            else:
                rows.append(current_row)
                current_row = [cell]
        rows.append(current_row)
    
    if len(rows) < 2:
        return "Error: Need at least 2 rows to extend"
    
    # Calculate row spacing (average y-difference between rows)
    row_spacing = np.mean([rows[i+1][0][1]-rows[i][0][1] for i in range(len(rows)-1)])
    
    # Create new rows until reaches to table bottom
    new_annotations = []
    last_row = rows[-1]
    while True:
        new_row = []
        for cell in last_row:
            new_y = cell[1] + row_spacing
            # Stop if new row goes beyond table bottom
            if new_y + cell[3]/2 > table_bottom:
                break
            new_row.append((cell[0], new_y, cell[2], cell[3]))
        
        if not new_row or new_row[0][1] > 0.95: 
            break
            
        new_annotations.extend([f"{labels['data']} {x:.6f} {y:.6f} {w:.6f} {h:.6f}" 
                               for x,y,w,h in new_row])
        last_row = new_row
    
    return raw_data + '\n' + '\n'.join(new_annotations) if new_annotations else raw_data


input_file = "C:\\Users\\s66\\Desktop\\check annto\\536024944-SEPT-20_page_1.txt"  
with open(input_file) as f:
    raw_data = f.read()

result = annotate_remaining_cells(raw_data)
print("\nResult:")
print(result)


try:
    with open('output_file.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"\nSuccessfully saved to output_file.txt")
except Exception as e:

    print(f"\nError saving file: {str(e)}")
