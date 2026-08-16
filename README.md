# ImageSmith

ImageSmith is a lightweight, clean, and efficient desktop image utility built with Python and PyQt6, packaged as a portable AppImage. It allows you to quickly view, crop, resize, tilt/perspective-correct, rotate, pad to square, and enhance images with a streamlined user interface.

## Features

* **Drag & Drop Support:** Easily drop images directly into the interface or use the open file dialog.
* **Cropping & Resizing:** Intuitive crop bounding box with handle controls and precise pixel-based resizing.
* **Perspective & Tilt Controls:** Adjust horizontal and vertical tilt with live previews.
* **Enhancements & Adjustments:** One-click auto-contrast, color boost, contrast, and sharpness tuning using Pillow.
* **Rotation & Padding:** Rotate images 90° or pad them cleanly to a square aspect ratio.
* **Multiple Formats:** Support for opening and exporting across various formats including PNG, JPEG, WebP, BMP, TIFF, and SVG vector wrappers.

## Requirements

ImageSmith is packaged as a self-contained **AppImage**, meaning it bundles its required dependencies (including Python, PyQt6, and Pillow) so it runs portably on most Linux distributions without requiring manual library installations.

## Installation & Usage

1. Download the latest `ImageSmith-x86_64.AppImage` from the GitHub Releases page.
2. Make the file executable via your terminal:
   ```bash
   chmod +x ImageSmith-x86_64.AppImage


   Adding to Your Application Menu

To install and integrate ImageSmith into your Linux desktop application launcher so it appears alongside your other apps, run the following commands in your terminal:

mkdir -p ~/.local/share/applications ~/.local/share/icons/hicolor/256x256/apps
cp imagesmith.desktop ~/.local/share/applications/imagesmith.desktop
cp imagesmith.png ~/.local/share/icons/hicolor/256x256/apps/imagesmith.png
update-desktop-database ~/.local/share/applications

Built With

    Python

    PyQt6

    Pillow (PIL)
