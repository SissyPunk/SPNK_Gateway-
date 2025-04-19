import os
import random
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import io
import base64
import logging

# Set up logging
logger = logging.getLogger(__name__)

def add_glitch_effect(img, intensity=0.5):
    """Add a digital glitch effect to the image."""
    img_array = np.array(img)
    channels = []
    
    # Split channels and apply glitch to each
    if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
        # Handle RGB/RGBA images
        for i in range(3):  # Process R, G, B channels
            channel = img_array[:, :, i].copy()
            
            # Random shift rows
            num_shifts = int(5 * intensity)
            for _ in range(num_shifts):
                row = random.randint(0, img_array.shape[0] - 1)
                shift = random.randint(-10, 10)
                if 0 <= row < img_array.shape[0]:
                    channel[row, :] = np.roll(channel[row, :], shift)
            
            # Random blocks
            num_blocks = int(3 * intensity)
            for _ in range(num_blocks):
                x = random.randint(0, img_array.shape[1] - 30)
                y = random.randint(0, img_array.shape[0] - 10)
                w = random.randint(10, 30)
                h = random.randint(5, 10)
                if y + h < img_array.shape[0] and x + w < img_array.shape[1]:
                    block = channel[y:y+h, x:x+w].copy()
                    channel[y:y+h, x:x+w] = np.roll(block, random.randint(-5, 5))
            
            channels.append(channel)
        
        # Reconstruct image with glitched channels
        for i in range(3):
            img_array[:, :, i] = channels[i]
        
        # Convert back to PIL Image
        glitched_img = Image.fromarray(img_array)
    else:
        # Handle grayscale images
        glitched_img = Image.fromarray(img_array)
        
        # Apply some alternative glitch effects for grayscale
        draw = ImageDraw.Draw(glitched_img)
        width, height = glitched_img.size
        
        # Add random lines
        for _ in range(int(10 * intensity)):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = y1 + random.randint(-5, 5)
            color = random.randint(0, 255)
            draw.line((x1, y1, x2, y2), fill=color, width=1)
    
    # Apply additional effects
    glitched_img = glitched_img.filter(ImageFilter.SHARPEN)
    contrast = ImageEnhance.Contrast(glitched_img)
    glitched_img = contrast.enhance(1.2)
    
    return glitched_img

def apply_cyberpunk_effect(img, intensity=0.8):
    """Apply a cyberpunk-style color scheme and effects."""
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Increase color saturation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.8)
    
    # Split the channels and adjust colors for cyberpunk feel
    r, g, b = img.split()
    
    # Enhance reds and blues for neon effect
    r = ImageEnhance.Brightness(r).enhance(1.2)
    b = ImageEnhance.Brightness(b).enhance(1.3)
    
    # Reconstruct the image with adjusted channels
    cyberpunk_img = Image.merge("RGB", (r, g, b))
    
    # Add a subtle texture/noise
    width, height = cyberpunk_img.size
    noise = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(noise)
    
    # Add random pixels for noise texture
    for _ in range(int(width * height * 0.1 * intensity)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        draw.point((x, y), fill=(
            random.randint(0, 50),
            random.randint(0, 50),
            random.randint(0, 50)
        ))
    
    # Overlay noise with reduced opacity
    cyberpunk_img = Image.blend(cyberpunk_img, noise, 0.05)
    
    return cyberpunk_img

def add_signal_lines(img, num_lines=5):
    """Add horizontal signal/scan lines effect."""
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    # Draw semi-transparent scan lines
    for _ in range(num_lines):
        y = random.randint(0, height - 1)
        draw.line((0, y, width, y), fill=(0, 255, 255, 60), width=1)
    
    # Add a few vertical glitch lines
    for _ in range(int(num_lines / 2)):
        x = random.randint(0, width - 1)
        draw.line((x, 0, x, height), fill=(255, 0, 255, 50), width=1)
    
    return img

def convert_png_to_signal_image(input_file, output_file, glitch_intensity=0.5, cyberpunk_intensity=0.8):
    """
    Convert a regular PNG to an 'optimized signal image' with glitch and cyberpunk effects.
    
    Args:
        input_file: Path to input PNG file
        output_file: Path where the processed file will be saved
        glitch_intensity: How strong the glitch effect should be (0.0 to 1.0)
        cyberpunk_intensity: How strong the cyberpunk effect should be (0.0 to 1.0)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open and convert image to RGB mode to ensure compatibility
        img = Image.open(input_file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply effects
        img = apply_cyberpunk_effect(img, cyberpunk_intensity)
        img = add_glitch_effect(img, glitch_intensity)
        img = add_signal_lines(img, num_lines=int(10 * glitch_intensity))
        
        # Save the result
        img.save(output_file)
        
        return True
    except Exception as e:
        logger.error(f"Error converting image: {str(e)}")
        return False

def convert_png_to_signal_svg(input_file, output_file):
    """
    Convert a PNG to an SVG with embedded image data and glitch effect styling.
    
    Args:
        input_file: Path to input PNG file
        output_file: Path where the processed SVG will be saved
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Process the image first with glitch effects
        img = Image.open(input_file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply effects to create the signal image
        img = apply_cyberpunk_effect(img)
        img = add_glitch_effect(img)
        img = add_signal_lines(img)
        
        # Convert to base64 for embedding in SVG
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Create SVG with embedded image and glitch filter definitions
        svg_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{img.width}" height="{img.height}" viewBox="0 0 {img.width} {img.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Digital glitch filter -->
    <filter id="glitchFilter" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" result="noise" seed="{random.randint(1, 100)}" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="10" xChannelSelector="R" yChannelSelector="G" result="glitch1" />
    </filter>
    
    <!-- Scanlines effect -->
    <pattern id="scanlines" patternUnits="userSpaceOnUse" width="4" height="4" patternTransform="rotate(0)">
      <line x1="0" y1="2" x2="{img.width}" y2="2" stroke="#00ffff" stroke-width="1" stroke-opacity="0.2"/>
    </pattern>
    
    <!-- Glow effect -->
    <filter id="glowEffect" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 5 -1" result="glow" />
      <feComposite in="SourceGraphic" in2="glow" operator="over" />
    </filter>
  </defs>
  
  <!-- Embedded image with processed effects -->
  <image width="100%" height="100%" href="data:image/png;base64,{img_data}" />
  
  <!-- Overlay elements -->
  <rect width="100%" height="100%" fill="url(#scanlines)" opacity="0.3" />
  
  <!-- Border with glitch effect -->
  <rect x="0" y="0" width="100%" height="100%" fill="none" stroke="#ff00ff" stroke-width="3" filter="url(#glitchFilter)" />
  
  <!-- SPNK NFT text -->
  <text x="50%" y="90%" font-family="'Courier New', monospace" font-size="20" fill="#00ffff" text-anchor="middle" filter="url(#glowEffect)">SPNK SIGNAL</text>
</svg>"""
        
        # Write SVG to file
        with open(output_file, 'w') as f:
            f.write(svg_content)
        
        return True
    except Exception as e:
        logger.error(f"Error converting image to SVG: {str(e)}")
        return False