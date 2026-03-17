import os
import requests
from dotenv import load_dotenv

# load enviornment variables from the .env file
load_dotenv()


API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not API_KEY:
    raise RuntimeError("Google API key not found. Set GOOGLE_MAPS_API_KEY first.")


def download_streetview(api_key, lat, lng, heading, save_folder, file_name):
    """
    Downloads a single Google Street View image.
    """
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    
    # Parameters for the API
    params = {
        "size": "640x640",         # Max free tier resolution (width x height)
        "location": f"{lat},{lng}",
        "heading": heading,        # Compass direction (0=North, 90=East, 180=South, 270=West)
        "pitch": 0,                # Camera angle up/down (-90 to 90)
        "fov": 90,                 # Field of view (Zoom level, max 120)
        "key": api_key,
        "return_error_code": "true" # Returns a 404 if no image exists here
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, file_name)
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name} (Heading: {heading})")
    else:
        print(f"Failed to download {file_name}. No imagery found or API error (Status: {response.status_code})")


if __name__ == "__main__":
    OUTPUT_FOLDER = "street_images"

    # ==========================================
    # SCENARIO A: Moving down a street (Driving Sequence)
    # Great for unified multi-view point clouds
    # ==========================================
    
    # List of GPS coordinates moving forward down a street
    # (Example: moving down a block in New York City)
    path_coordinates =[
        (33.76433, -84.38209),
        (33.76453, -84.38209),
        (33.76473, -84.38209),
        (33.76493, -84.38209),
        (33.76513, -84.38209),
        (33.76533, -84.38209),
        (33.76553, -84.38209),
        (33.76573, -84.38209)
    ]
    
    print("Downloading forward-facing sequence...")
    for index, (lat, lng) in enumerate(path_coordinates):
        # Using heading 45 (Northeast) to face down the road
        # Using heading 180 (South) to face down the road
        # Using heading 270 (West) to face down the road
        download_streetview(
            api_key=API_KEY,
            lat=lat,
            lng=lng,
            heading=270, 
            save_folder=OUTPUT_FOLDER,
            file_name=f"sequence_{index:03d}.jpg"
        )

    # ==========================================
    # SCENARIO B: 360 Sweep from ONE Location
    # Great for wrapping a point cloud around the camera
    # ==========================================
    '''
    target_lat = 33.76433
    target_lng = -84.38209
    
    print("\nDownloading 360-degree sweep...")
    # Headings: 0, 60, 120, 180, 240, 300 (6 overlapping shots)
    for heading in range(0, 360, 60):
        download_streetview(
            api_key=API_KEY,
            lat=target_lat,
            lng=target_lng,
            heading=heading,
            save_folder=OUTPUT_FOLDER,
            file_name=f"sweep_heading_{heading}.jpg"
        )
        '''
