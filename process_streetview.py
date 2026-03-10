import os
import glob
import sys
import torch

da3_path = os.path.abspath(os.path.join("Depth_Anything", "src"))
sys.path.append(da3_path)

import torch
from depth_anything_3.api import DepthAnything3

def generate_pointcloud(input_folder, output_folder):
    # 1. Grab all JPG/PNG images from the folder
    # Adjust the extension if your images are .jpeg or .png
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
    # Options: "depth-anything/da3-small", "depth-anything/da3-base", "depth-anything/da3-large"
    print("Loading Depth Anything 3 model into VRAM...")
    model = DepthAnything3.from_pretrained("depth-anything/da3-large")
    model = model.to(device)

    # 4. Run the inference pipeline
    print(f"Processing {len(image_paths)} images...")
    
    os.makedirs(output_folder, exist_ok=True)

    # Passing a list of images triggers multi-view 3D reconstruction
    prediction = model.inference(
        images=image_paths,
        export_dir=output_folder,
        export_format="ply"  # 'ply' is the standard point cloud format
    )

    print(f"Success! Point cloud saved to: {output_folder}")
    
    # (Optional) You can directly access the raw PyTorch tensors if needed for custom math:
    # print("Depth maps shape:", prediction.depth.shape)
    # print("Estimated Camera Poses shape:", prediction.extrinsics.shape)

if __name__ == "__main__":
    # Define your target directories here
    INPUT_DIR = "street_images"
    OUTPUT_DIR = "3d_outputs"
    
    generate_pointcloud(INPUT_DIR, OUTPUT_DIR)

