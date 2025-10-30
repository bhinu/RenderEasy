from renderease import process_room

# DeepLab is better at semantic segmentation
result = process_room(
    "test_room.JPG",
    "brick_texture.jpg",
    method="deeplab",  # Use deep learning
    surface_type="wall",
)
