#!/usr/bin/env python3
"""
Create a shield favicon for EduSecure
"""
from PIL import Image, ImageDraw
import os

def create_shield_favicon():
    """Create a shield-shaped favicon"""
    # Create a 32x32 image with transparent background
    size = 32
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define shield shape points
    shield_points = [
        (16, 2),   # Top center
        (6, 6),    # Top left
        (6, 14),   # Middle left
        (10, 22),  # Bottom left curve
        (16, 28),  # Bottom center
        (22, 22),  # Bottom right curve
        (26, 14),  # Middle right
        (26, 6),   # Top right
        (16, 2)    # Back to top
    ]
    
    # Draw shield with gradient-like effect
    # Main shield body
    draw.polygon(shield_points[:-1], fill=(14, 165, 233, 255), outline=(255, 255, 255, 255), width=1)
    
    # Add inner highlight
    inner_points = [
        (16, 4),
        (8, 7),
        (8, 13),
        (12, 20),
        (16, 25),
        (20, 20),
        (24, 13),
        (24, 7),
        (16, 4)
    ]
    draw.polygon(inner_points[:-1], fill=(16, 185, 129, 200))
    
    # Save as PNG (modern browsers support PNG favicons)
    img.save('public/favicon.png', 'PNG')
    
    # Also save as ICO for older browsers
    try:
        img.save('public/favicon.ico', 'ICO')
        print("✓ Created favicon.ico")
    except:
        print("⚠ Could not create ICO format, PNG will be used")
    
    print("✓ Created shield favicon")

if __name__ == "__main__":
    create_shield_favicon()