import os
import glob
import torch
from depth_anything_3.api import DepthAnything3

def generate_pointcloud(input_folder, output_folder):
    # 1. Grab all JPG/PNG images from the folder
    image_paths = glob.glob(os.path.join(input_folder, "*.jpg"))
    
    if not image_paths:
        print(f"No images found in {input_folder}!")
        return

    # Sort images alphanumerically (important if they are sequential street views)
    image_paths.sort()
    
    # 2. Set up the GPU device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cpu":
        print("Warning: CUDA not detected. Processing will be very slow on CPU.")

    # 3. Load the DA3 Model 
    print("Loading Depth Anything 3 model into VRAM...")
    model = DepthAnything3.from_pretrained("depth-anything/da3-base")
    model = model.to(device)

    # 4. Run the inference pipeline
    print(f"Processing {len(image_paths)} images individually to save RAM...")
    
    os.makedirs(output_folder, exist_ok=True)

    with torch.autocast(device_type="cuda", dtype=torch.float16):
        # LOOP START: Process images one by one
        for img_path in image_paths:
            print(f" -> Generating pointcloud for: {os.path.basename(img_path)}")
            
            # Pass only a single image path as a list
            prediction = model.inference(
                image=[img_path], 
                export_dir=output_folder,
                export_format="glb"
            )
            
            # (Optional) If you need to access raw PyTorch tensors, do it inside the loop:
            # print("Depth maps shape:", prediction.depth.shape)
            
            # (Optional) Clear VRAM cache between iterations to prevent memory fragmentation
            # torch.cuda.empty_cache() 

    print(f"Success! Point clouds saved to: {output_folder}")

if __name__ == "__main__":
    # Define your target directories here
    INPUT_DIR = "street_images"
    OUTPUT_DIR = "3d_outputs"
    
    generate_pointcloud(INPUT_DIR, OUTPUT_DIR)

    

