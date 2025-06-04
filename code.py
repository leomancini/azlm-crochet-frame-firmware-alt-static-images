import board
import time
from adafruit_matrixportal.matrix import Matrix
import displayio

print("Starting Matrix Portal with image display...")

def load_image(filename):
    """Load a BMP image file and return a TileGrid for display"""
    try:
        print(f"Attempting to load {filename}...")
        # Load the bitmap image
        image_file = open(filename, "rb")
        odb = displayio.OnDiskBitmap(image_file)
        
        print(f"Image loaded: {odb.width}x{odb.height}")
        
        # Check if dimensions are reasonable
        if odb.width > 128 or odb.height > 128:
            print(f"WARNING: Image dimensions seem wrong! {odb.width}x{odb.height}")
            print("This suggests the BMP format may not be compatible")
            image_file.close()
            return None, None
        
        # Create a TileGrid to hold the image
        image_tilegrid = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
        
        # Rotate the image 90 degrees left (counterclockwise)
        print("Rotating image 90 degrees left...")
        image_tilegrid.transpose_xy = True
        image_tilegrid.flip_x = True
        
        # Center the rotated image if needed
        # Note: After rotation, width and height are swapped
        rotated_width = odb.height
        rotated_height = odb.width
        
        if rotated_width < 64:
            image_tilegrid.x = (64 - rotated_width) // 2
        if rotated_height < 64:
            image_tilegrid.y = (64 - rotated_height) // 2
            
        print(f"Rotated image positioned at ({image_tilegrid.x}, {image_tilegrid.y})")
        return image_tilegrid, image_file
    except Exception as e:
        print(f"Error loading image {filename}: {e}")
        return None, None

def create_fallback_pattern():
    """Create a colorful fallback pattern if image loading fails"""
    print("Creating fallback pattern...")
    
    bitmap = displayio.Bitmap(64, 64, 4)
    palette = displayio.Palette(4)
    palette[0] = 0x000000  # Black
    palette[1] = 0xFF0000  # Red
    palette[2] = 0x00FF00  # Green
    palette[3] = 0x0000FF  # Blue
    
    # Create a simple pattern
    for x in range(64):
        for y in range(64):
            if x < 32 and y < 32:
                bitmap[x, y] = 1  # Red quadrant
            elif x >= 32 and y < 32:
                bitmap[x, y] = 2  # Green quadrant
            elif x < 32 and y >= 32:
                bitmap[x, y] = 3  # Blue quadrant
            else:
                bitmap[x, y] = 0  # Black quadrant
    
    return displayio.TileGrid(bitmap, pixel_shader=palette)

try:
    # Matrix setup
    print("Initializing matrix...")
    matrix = Matrix(width=64, height=64)
    display = matrix.display
    
    print(f"Display size: {display.width}x{display.height}")
    print("Matrix initialized successfully!")
    
    # Clear display
    display.root_group = displayio.Group()
    
    # Try to load the image
    image_tilegrid, image_file = load_image("image.bmp")
    
    # Create display group
    group = displayio.Group()
    
    if image_tilegrid:
        print("Image loaded successfully! Displaying image...")
        group.append(image_tilegrid)
    else:
        print("Image not found or failed to load. Showing fallback pattern...")
        fallback_tilegrid = create_fallback_pattern()
        group.append(fallback_tilegrid)
        image_file = None
    
    # Set the display
    print("Setting display...")
    display.root_group = group
    display.refresh()
    
    print("Display updated! Check your matrix.")
    
except Exception as e:
    print(f"Error during initialization: {e}")
    import traceback
    traceback.print_exception(type(e), e, e.__traceback__)

# Main loop
print("Entering main loop...")
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted")
        break
    except Exception as e:
        print(f"Error in loop: {e}")
        time.sleep(1)