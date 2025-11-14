#!/usr/bin/env python3
"""
Simple LSB Steganography Decoder (Online Tool Compatible)

This script decodes messages hidden using LSB steganography compatible with online tools:
- Message is encoded sequentially across RGB channels
- Null terminator (0x00) marks the end of the message
- Compatible with stylesuxx.github.io/steganography, cypherchief, etc.

Usage:
    python decode_lsb.py <image_file>
    python decode_lsb.py docs/images/steganpuzzle/encoded.png
"""

from PIL import Image
import numpy as np
import sys


def decode_lsb_online_compatible(img_path):
    """
    Decode message from image using online-compatible LSB method
    
    Online tools (stylesuxx, cypherchief, etc.) approach:
    - Read LSBs sequentially from RGB channels
    - Convert 8 bits at a time to characters
    - Stop when null byte (0x00) is encountered
    
    Args:
        img_path: path to the image file
    
    Returns:
        Decoded message string
    """
    # Load image
    print(f"Loading image: {img_path}")
    img = Image.open(img_path)
    img_array = np.array(img)
    
    height, width, channels = img_array.shape
    print(f"Image size: {width}x{height}, Channels: {channels}")
    
    binary_data = ''
    
    # Extract LSBs sequentially from RGB channels
    for i in range(height):
        for j in range(width):
            for c in range(channels):  # R, G, B channels
                pixel_value = img_array[i, j, c]
                binary_data += str(pixel_value & 1)
    
    # Convert binary to text, stopping at null byte (0x00)
    message = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            char_code = int(byte, 2)
            # Stop at null terminator (0x00)
            if char_code == 0:
                break
            # Only add printable characters (online tools often filter these)
            if 32 <= char_code <= 126 or char_code >= 128:  # Printable ASCII + extended
                message += chr(char_code)
            else:
                # Non-printable character - might be end of message
                break
    
    return message


def main():
    if len(sys.argv) < 2:
        print("Usage: python decode_lsb.py <image_file>")
        print("Example: python decode_lsb.py docs/images/steganpuzzle/encoded.png")
        sys.exit(1)
    
    img_path = sys.argv[1]
    
    try:
        message = decode_lsb_online_compatible(img_path)
        
        if message:
            print("\n" + "=" * 60)
            print("DECODED MESSAGE:")
            print("=" * 60)
            print(message)
            print("=" * 60)
        else:
            print("\nNo message found or unable to decode.")
            
    except FileNotFoundError:
        print(f"Error: File '{img_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

