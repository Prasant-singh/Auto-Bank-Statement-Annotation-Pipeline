import fitz
import os


upload_folder = "C:\\Users\\s66\\Desktop\\task\\data"
save_folder = "C:\\Users\\s66\\Desktop\\task\\converted_images"

if not os.path.exists(save_folder):
    os.makedirs(save_folder)
    print(f"Created save folder at: {save_folder}")

# Iterating each pdf file
for filename in os.listdir(upload_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(upload_folder, filename)
        
        try:
            
            doc = fitz.open(pdf_path)

            #  Checking for encryption BEFORE trying to access pages
            if doc.is_encrypted:
                print(f"--> SKIPPING '{filename}' because it is password-protected.")
                continue

        
            print(f"Processing '{filename}'...")
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap(dpi=150)

               
                base_name = os.path.splitext(filename)[0]    #"company_report.pdf" and split ('company_report', '.pdf') to remove the extension .pdf from images
                save_path = os.path.join(save_folder, f"{base_name}_page_{page_num + 1}.png")
                
                pix.save(save_path)
            
            doc.close()

        except Exception as e:

            print(f"--> FAILED to process '{filename}'. Reason: {e}")

print("\nConversion process finished.")