import json
import numpy as np
from PIL import Image
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def plot_masks_and_scores(image, masks, scores=None, num_cols=3):
    """
    Plots boolean masks on separate copies of a given Pillow image in a grid layout.
    
    Args:
    - image (PIL.Image): The background image.
    - masks (numpy.ndarray): A boolean array of shape (num_objects, H, W).
    - num_cols (int): Number of columns in the grid.
    """
    plt.close('all')
    num_masks = masks.shape[0]
    # Correctly calculate grid size
    num_rows = int(np.ceil((num_masks + 1) / num_cols))
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, num_rows * 4))  # Adjust figure size based on the number of rows
    axes = np.atleast_2d(axes).flatten()  # Flatten axes array for easier access and ensure it works for single-row grids
    
    # Plot the original image in the first subplot
    axes[0].imshow(image)
    axes[0].set_title("Original Image")
    axes[0].axis('off')
    
    colors = list(mcolors.TABLEAU_COLORS.values())  # Distinct colors for masks
    
    for i, mask in enumerate(masks):
        # Copy the original image
        image_with_mask = image.convert("RGBA")
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))  # Transparent overlay
        
        # Create a color for the mask
        mask_color_rgba = mcolors.to_rgba(colors[i % len(colors)], alpha=0.5)
        mask_color_255 = tuple(int(255 * c) for c in mask_color_rgba)
        
        # Apply color to the mask
        for y in range(mask.shape[0]):
            for x in range(mask.shape[1]):
                if mask[y, x]:
                    overlay.putpixel((x, y), mask_color_255)
        
        # Composite the colored overlay with the image
        image_with_mask = Image.alpha_composite(image_with_mask, overlay)
        
        # Plot the image with the mask
        axes[i + 1].imshow(image_with_mask)
        title = f"Mask {i + 1}"
        if scores is not None:
            title += f', Score = {scores[i]}'
        axes[i + 1].set_title(title)
        axes[i + 1].axis('off')
    
    # Hide any unused subplots
    for ax in axes[num_masks + 1:]:
        ax.axis('off')
    
    # Adjust layout padding
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)


def get_images_masks_scores(base_dir, mask_ext='.npy', image_ext='.png'):
    image_dir = os.path.join(base_dir, 'images')
    mask_dir = os.path.join(base_dir, 'masks')
    with open(os.path.join(base_dir, 'scores.json')) as f:
        scores = json.load(f)
    images, masks = {}, {}
    for filename in scores:
        images[filename] = Image.open(os.path.join(image_dir, filename + image_ext))
        masks[filename] = np.load(os.path.join(mask_dir, filename + mask_ext))
    return images, masks, scores