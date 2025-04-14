# SD SAXS File Viewer

A graphical tool for visualizing SAXS (Small-Angle X-ray Scattering) data files in TIFF and EDF formats.

## Features

- Support for TIFF and EDF file formats
- Interactive visualization with adjustable contrast
- Multiple colormap options
- Various normalization methods (Linear, Log, Power)
- Zoom lock feature for comparing multiple images
- Dark-themed UI for comfortable viewing

## Installation

```bash
pip install sdsaxsviewer
```

## Usage

After installation, you can run the application with:

```bash
# Run as a module
python -m sdsaxsviewer

# Or if entry points are installed
sdsaxsviewer
```

## Requirements

- Python 3.7+
- PySide6
- NumPy
- Matplotlib
- tifffile
- fabio

## Development

To contribute:

```bash
git clone https://github.com/yourusername/sdsaxsviewer.git
cd sdsaxsviewer
pip install -e .
```

## License

MIT License