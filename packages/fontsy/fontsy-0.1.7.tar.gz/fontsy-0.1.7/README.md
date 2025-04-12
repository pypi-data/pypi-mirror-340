# Fontsy - ASCII Art Font Explorer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A fun interactive ASCII art generator for your terminal that lets you explore, preview, and export text in hundreds of different font styles. Fontsy was a small exercise in so called "vibe coding" with our own agent framework called Flock. 

**Almost everything was written by Flock.** 

https://github.com/whiteducksoftware/flock


<p align="center">
  <img src="docs/fontsy.png" width="800" />
</p>

## ✨ Features

- Explore hundreds of ASCII art fonts interactively
- Preview text in different font categories: 3D, block, banner, bubble, digital, script, and more
- Two display modes: grid (compact) and list (detailed)
- Mark fonts as favorites for quick access
- Showcase mode to view your text in all available fonts
- Clipboard integration for quick copying
- Rich, colorful terminal interface

- Export creations to HTML, markdown, or plain text

<p align="center">
  <img src="docs/html_export.png" width="800" />
</p>

- Live input mode to see your text rendered in real-time

<p align="center">
  <img src="docs/input.png" width="800" />
</p>

## 🚀 Quick Start

The easiest way to use Fontsy is with [uv](https://github.com/astral-sh/uv):

```bash
# Run without installing
uvx fontsy
```

## 📋 Usage

Once running, Fontsy operates through a simple command interface:

- Type your **text** and press Enter to see it in different fonts
- Press **Enter** with empty input to see new fonts for the same text
- Type a **font category** to filter fonts (standard, small, medium, large, xlarge, ascii_only, 3d, etc.)
- Type **grid** or **list** to change display mode
- Type **showcase** to see your text in ALL fonts
- Type a **number** (e.g., '3') to favorite the font with that number
- Type **clipboard number** (e.g., 'clipboard 5') to copy a font to clipboard
- Type **favorite font_name** to mark a specific font as favorite
- Type **favorites** to see only your favorite fonts
- Type **export html/text/md** to save the current view
- Type **help** for a full list of commands
- Type **quit** to exit

## 🏗️ Architecture

Fontsy is a huge ass file.

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Fontsy Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- [art](https://github.com/sepandhaghighi/art) - ASCII art library
- [rich](https://github.com/Textualize/rich) - Terminal formatting
- [uv](https://github.com/astral-sh/uv) - Python packaging
