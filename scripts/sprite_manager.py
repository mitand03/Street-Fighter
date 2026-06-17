import pygame
import os

# Helper function to load images
def load_sprite_sequence(folder_path, base_filename, num_images):
    sprites = []
    for i in range(num_images):
        # Construct the filename based on the index
        filename = f"{base_filename}{i:03d}.png"  # Example: Throw__000.png, Throw__001.png
        image_path = os.path.join(folder_path, filename)

        # Load the image and append it to the list
        if os.path.exists(image_path):
            image = pygame.image.load(image_path)
            image = pygame.transform.rotozoom(image, 1, 0.2)
            sprites.append(image)
        else:
            print(f"Warning: {image_path} not found.")
    return sprites

def load_sprite_sequence2(folder_path, base_filename, num_images):
    sprites = []
    for i in range(num_images):
        # Construct the filename based on the index
        filename = f"{base_filename} ({i+1}).png"  # Example: Run (1).png, Run (2).png
        image_path = os.path.join(folder_path, filename)

        # Load the image and append it to the list
        if os.path.exists(image_path):
            image = pygame.image.load(image_path)
            image = pygame.transform.rotozoom(image, 1, 0.15)
            sprites.append(image)
        else:
            print(f"Warning: {image_path} not found.")
    return sprites