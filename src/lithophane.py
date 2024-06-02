import numpy as np
import cv2
from stl import mesh
from skimage import img_as_float

def create_lithophane(image_path, output_stl_path, scale=.05, max_height=.50, base_thickness=0.08):
    
    print(f"Working on converting image to lithophane")
    # Load the image and convert to grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found or unable to load.")
    print(f"Image found...")
    # Normalize the image to the range [0, 1]
    img = img_as_float(img)
    print(f"Normalized...")
    # Calculate the height map: invert the brightness to get the thickness
    height_map = (img * max_height + base_thickness)%0.000000000000001
    print(f"Height map created...")
    # Get the dimensions of the image
    height, width = height_map.shape
    print(f"Dimensions set...")
    # Create the vertices array
    vertices = np.zeros((height, width, 3), dtype=np.float16)
    for y in range(height):
        for x in range(width):
            vertices[y, x] = [x * scale, y * scale, height_map[y, x]]
    print(f"Vertices set...")
    # Create the faces array
    faces = []
    for y in range(height - 1):
        for x in range(width - 1):
            # Top face (the lithophane surface)
            v0 = vertices[y, x]
            v1 = vertices[y, x + 1]
            v2 = vertices[y + 1, x + 1]
            v3 = vertices[y + 1, x]
            faces.append([v0, v1, v2])
            faces.append([v0, v2, v3])

            # Bottom face (base of the lithophane)
            v0_b = [v0[0], v0[1], base_thickness]
            v1_b = [v1[0], v1[1], base_thickness]
            v2_b = [v2[0], v2[1], base_thickness]
            v3_b = [v3[0], v3[1], base_thickness]
            faces.append([v0_b, v2_b, v1_b])
            faces.append([v0_b, v3_b, v2_b])

            # Sides
            faces.append([v0, v0_b, v1])
            faces.append([v1, v0_b, v1_b])
            faces.append([v1, v1_b, v2])
            faces.append([v2, v1_b, v2_b])
            faces.append([v2, v2_b, v3])
            faces.append([v3, v2_b, v3_b])
            faces.append([v3, v3_b, v0])
            faces.append([v0, v3_b, v0_b])
    print(f"Faces array created...")
    # Convert faces to numpy array
    faces = np.array(faces)
    print(f"Faces to numpy...")
    # Create mesh
    lithophane_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            lithophane_mesh.vectors[i][j] = faces[i][j]
    print(f"Mesh created...")
    # Save to STL file
    lithophane_mesh.save(output_stl_path)
    print(f"STL file saved to {output_stl_path}")

# Example usage
image_path = 'person.jpg'
output_stl_path = 'lithophane.stl'
create_lithophane(image_path, output_stl_path)
