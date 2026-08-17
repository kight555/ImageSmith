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

## Portable by Design

ImageSmith is distributed as a self-contained **AppImage**.

The AppImage bundles the application's required runtime and Python dependencies, including:

* Python
* PyQt6
* Pillow

This means you don't need to manually install Python packages or configure a Python environment before running ImageSmith.

### Download → Rename → Run → Get the job done

When you first download the AppImage, rename it to match the clean file name:

    mv ImageSmith-v1.0.0-x86_64.AppImage imagesmith

Make the AppImage executable:

    chmod +x imagesmith

Then launch it:

    ./imagesmith

---

## 🖥️ Add ImageSmith to Your Application Menu

If you want ImageSmith to appear in your application menu, create the required directory:

    mkdir -p ~/.local/share/applications

Create and open the desktop entry file using a text editor like nano:

    nano ~/.local/share/applications/imagesmith.desktop

Paste the following configuration into the file:

    [Desktop Entry]
    Type=Application
    Name=ImageSmith
    Exec=path/to/imagesmith
    Categories=Graphics;Utility;
    Comment=Simple image editing without the bloat

*(Note: Save the file in nano by pressing `Ctrl+O`, hitting `Enter`, and then exiting with `Ctrl+X`)*

Refresh the application database:

    update-desktop-database ~/.local/share/applications

ImageSmith should now appear in your desktop environment's application launcher.

---

## Built With

ImageSmith is built around a small, focused Python stack.

| Technology        | Role                                                          |
| ---------------- | ------------------------------------------------------------- |
| **Python**       | Core application                                              |
| **PyQt6**        | User interface and desktop integration                        |
| **Pillow (PIL)** | Image processing, editing, enhancement, and format conversion |
| **AppImage**     | Portable Linux packaging                                      |

### Pillow

**Pillow** provides the image-processing foundation behind ImageSmith.

It handles operations such as:

* Cropping
* Resizing
* Rotation
* Padding
* Contrast, brightness, and color adjustments (handled through the enhance feature)
* Sharpness adjustment
* Image format conversion
* Raster image processing

Keeping the image-processing work centered around Pillow helps ImageSmith remain focused without pulling in a large collection of unnecessary libraries.

---

## The Goal

ImageSmith isn't trying to replace full-featured image editors.

It's trying to make the **simple stuff simple**.

If you need advanced photo manipulation, illustration tools, layers, or a massive collection of professional features, a full image editor may be the better choice.

If you just need to **open an image, make a few changes, convert it, and move on**, ImageSmith is built for that.

> **Less bloat. Less complexity. More getting things done.**

---

## Linux

ImageSmith is currently distributed as an **x86_64 Linux AppImage**.
