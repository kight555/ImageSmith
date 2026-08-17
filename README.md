<p align="center">
  <br>
  <img src="./.assets/imagesmith.png" alt="Image-Smith Logo" width="250">
  <br>
  <br>
</p>




## ImageSmith

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

## ✨ Features

* 🖱️ **Drag & Drop** — Drop images directly into ImageSmith or open them through the file dialog.
* ✂️ **Crop & Resize** — Crop images with an intuitive bounding box and resize them with precise pixel controls.
* 📐 **Perspective & Tilt** — Adjust horizontal and vertical tilt with live previews.
* 🎨 **Image Enhancements** — Quickly adjust contrast, color, and sharpness or apply automatic contrast.
* 🔄 **Rotation** — Rotate images in 90° increments.
* ⬜ **Square Padding** — Add clean padding to make an image perfectly square.
* 🧩 **SVG Support** — Open SVG artwork and convert it into raster image formats for editing and export.
* 📁 **Multiple Formats** — Work with PNG, JPEG, WebP, BMP, TIFF, and SVG.
* 🚀 **Portable** — Distributed as a self-contained Linux AppImage.

---

## 💡 Why ImageSmith?

There are plenty of powerful image editors available for Linux, and they're great when you need everything they offer.

But sometimes you don't.

Sometimes you just need to crop an image, resize it, fix its perspective, convert an SVG, or make a few quick adjustments — **without launching a huge application built for a completely different workflow.**

That's where ImageSmith comes in.

ImageSmith is intentionally focused on common image tasks while avoiding unnecessary complexity and feature bloat.

**Small. Focused. Fast. Easy to use.**

---

## 🖼️ Supported Formats

ImageSmith supports both **raster and vector image workflows**.

### 🧩 SVG

* Open SVG images
* Convert SVG artwork to raster formats
* Apply ImageSmith's editing tools
* Export the finished image

### 🖼️ Raster

* PNG
* JPEG / JPG
* WebP
* BMP
* TIFF

---

## 📦 Portable by Design

ImageSmith is distributed as a self-contained **AppImage**.

The AppImage bundles the application's required runtime and Python dependencies, including:

* Python
* PyQt6
* Pillow

This means you don't need to manually install Python packages or configure a Python environment before running ImageSmith.

### Download → Run → Get the job done

Make the AppImage executable:

```bash
chmod +x ImageSmith-x86_64.AppImage
```

Then launch it:

```bash
./ImageSmith-x86_64.AppImage
```

---

## 🖥️ Add ImageSmith to Your Application Menu

If you want ImageSmith to appear alongside your other Linux applications, you can install its desktop entry and icon locally.

Create the required directories:

```bash
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/256x256/apps
```

Copy the desktop entry:

```bash
cp imagesmith.desktop ~/.local/share/applications/imagesmith.desktop
```

Copy the application icon:

```bash
cp imagesmith.png ~/.local/share/icons/hicolor/256x256/apps/imagesmith.png
```

Refresh the application database:

```bash
update-desktop-database ~/.local/share/applications
```

ImageSmith should now appear in your desktop environment's application launcher.

---

## 🛠️ Built With

ImageSmith is built around a small, focused Python stack.

| Technology       | Role                                                          |
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
* Contrast adjustment
* Color enhancement
* Sharpness adjustment
* Image format conversion
* Raster image processing

Keeping the image-processing work centered around Pillow helps ImageSmith remain focused without pulling in a large collection of unnecessary libraries.

---

## 🎯 The Goal

ImageSmith isn't trying to replace full-featured image editors.

It's trying to make the **simple stuff simple**.

If you need advanced photo manipulation, illustration tools, layers, or a massive collection of professional features, a full image editor may be the better choice.

If you just need to **open an image, make a few changes, convert it, and move on**, ImageSmith is built for that.

> **Less bloat. Less complexity. More getting things done.**

---

## 🐧 Linux

ImageSmith is currently distributed as an **x86_64 Linux AppImage**.

Because it is packaged as an AppImage, it can run across many Linux distributions without requiring users to separately install the application's Python dependencies.

---
