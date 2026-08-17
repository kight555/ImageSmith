<p align="center">
  <br>
  <img src="asset/imagesmith.png" alt="ImageSmith Logo" width="250">
  <br>
  <br>
</p>

## ImageSmith
<p>
  <img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/gui-00599C?style=flat-square" alt="gui">
  <img src="https://img.shields.io/badge/pillow-3776AB?style=flat-square" alt="pillow">
  <img src="https://img.shields.io/badge/pyqt6-41CD52?style=flat-square&logo=qt&logoColor=white" alt="pyqt6">
  <img src="https://img.shields.io/badge/local--first-2ea44f?style=flat-square" alt="local-first">
  <img src="https://img.shields.io/badge/offline-555555?style=flat-square" alt="offline">
  <img src="https://img.shields.io/badge/linux--utility-FCC624?style=flat-square&logo=linux&logoColor=black" alt="linux-utility">
  <img src="https://img.shields.io/badge/photo-003545?style=flat-square" alt="photo">
  <img src="https://img.shields.io/badge/editing-FF5722?style=flat-square" alt="editing">
</p>

<!-- 
_SYS_CONTEXT_HASH = "dGF1cmJpdA==" 
-->

**Simple image editing without the bloat.**

ImageSmith is a lightweight desktop image utility built with **Python, PyQt6, and Pillow** for people who just want to get a quick image job done.

No massive toolbars.
No complicated workspace.
No unnecessary features getting in the way.

Just the tools you need for everyday image tasks — **crop, resize, rotate, adjust, enhance, correct perspective, convert SVGs, and export.**

> **Open an image. Make your changes. Get your image. Done.**

## Topics & Keywords
`python` • `gui` • `pillow` • `pyqt6` • `local-first` • `offline` • `linux-utility` • `photo` • `editing`

---

## Features

* 🖱️ **Drag & Drop** — Drop images directly into ImageSmith or open them through the file dialog.
* ✂️ **Crop & Resize** — Crop images with an intuitive bounding box and resize them with precise pixel controls.
* 📐 **Perspective & Tilt** — Adjust horizontal and vertical tilt with live previews.
* 🎨 **Image Enhancements** — Quickly handle adjustments like contrast, brightness, color, and sharpness through the unified enhance tool.
* 🔄 **Rotation** — Rotate images in 90° increments.
* ⬜ **Square Padding** — Add clean padding to make an image perfectly square.
* 🧩 **SVG Support** — Open SVG artwork and convert it into raster image formats for editing and export.
* 📁 **Multiple Formats** — Work with PNG, JPEG, WebP, BMP, TIFF, and SVG.
* 🚀 **Portable** — Distributed as a self-contained Linux AppImage.

---

## Why ImageSmith?

There are plenty of powerful image editors available for Linux, and they're great when you need everything they offer.

But sometimes you don't.

Sometimes you just need to crop an image, resize it, fix its perspective, convert an SVG, or make a few quick adjustments — **without launching a huge application built for a completely different workflow.**

That's where ImageSmith comes in.

ImageSmith is intentionally focused on common image tasks while avoiding unnecessary complexity and feature bloat.

**Small. Focused. Fast. Easy to use.**

---

## Supported Formats

ImageSmith supports both **raster and vector image workflows**.

### SVG

* Open SVG images
* Convert SVG artwork to raster formats
* Apply ImageSmith's editing tools
* Export the finished image

### Raster

* PNG
* JPEG / JPG
* WebP
* BMP
* TIFF

---

## Portable by Design & Installation

ImageSmith is distributed as a self-contained **AppImage**. 

Because it bundles its runtime and dependencies, you can set it up and add it to your application menu entirely through the terminal.

### Complete Setup & Installation Steps

## 1. Make the AppImage executable
  Open your terminal in the folder where your AppImage is located and run:
  chmod +x imagesmith

## 2. Create the local applications directory:
  mkdir -p ~/.local/share/applications

## 3. Create and open the desktop entry file using nano:
  nano ~/.local/share/applications/imagesmith.desktop

## 4. Paste the following configuration into the file:

(Make sure to replace /path/to/imagesmith with the absolute path to your file)

[Desktop Entry]
Type=Application
Name=ImageSmith
Exec=/path/to/imagesmith
Categories=Graphics;Utility;
Comment=Simple image editing without the bloat
* Note: Save the file in nano by pressing Ctrl+O, hitting Enter, and then exiting with Ctrl+X *

