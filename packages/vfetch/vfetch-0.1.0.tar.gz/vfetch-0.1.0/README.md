# vfetch 🖥️

<div align="center">
  <img src="screenshots/vfetch_logo.png" alt="vfetch logo" width="200"/>
  <h3>A beautiful system information display tool</h3>
  <p>🔥 Like neofetch, but better 🔥</p>
  
  [![PyPI Version](https://img.shields.io/pypi/v/vfetch.svg)](https://pypi.org/project/vfetch/)
  [![Python Versions](https://img.shields.io/pypi/pyversions/vfetch.svg)](https://pypi.org/project/vfetch/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

## Features ✨

- **Enhanced Visuals**: 14+ stunning themes and 15+ ASCII art options
- **Comprehensive System Details**: CPU, memory, disk, network, OS, and more
- **Visual Indicators**: Graphical displays for memory and disk usage
- **Responsive Layout**: Adapts to your terminal size
- **Customizable**: Mix and match themes and ASCII art to suit your style
- **Minimal Mode**: Clean, elegant display when options aren't specified
- **Demo Mode**: Showcase all the available themes and ASCII art combinations

## Screenshots 📸

### Cyberpunk Theme with Dragon ASCII
![Cyberpunk Theme with Dragon ASCII](screenshots/cyberpunk_dragon.png)

### Neon Theme with Cat ASCII
![Neon Theme with Cat ASCII](screenshots/neon_cat.png)

### Minimal Mode (Default when no theme/ASCII specified)
![Minimal Mode](screenshots/minimal_mode.png)

## Installation 🔧

### From PyPI

```bash
pip install vfetch
```

### From Source

```bash
git clone https://github.com/yourusername/vfetch.git
cd vfetch
pip install .
```

## Usage 🚀

Basic usage:

```bash
vfetch
```

Specify theme and ASCII art:

```bash
vfetch -t cyberpunk -a dragon
```

### Options

| Option | Description |
|--------|-------------|
| `-t, --theme THEME` | Specify the theme (e.g., cyberpunk, neon, replit) |
| `-a, --ascii ART` | Specify the ASCII art (e.g., dragon, cat, cube) |
| `-r, --refresh SECONDS` | Auto-refresh every N seconds |
| `-p, --performance` | Include performance metrics |
| `--list-themes` | Display all available themes |
| `--list-ascii` | Display all available ASCII art options |
| `--demo-mode` | Showcase all theme/ASCII combinations |

## Available Themes 🎨

- default
- cyberpunk
- neon
- replit
- dracula
- matrix
- ocean
- sunset
- retro
- forest
- space
- fire
- ice
- monochrome

## Available ASCII Art 🖼️

- dragon
- cat
- dog
- fox
- penguin
- owl
- keycaps
- circuit
- replit
- cube
- pixel
- blocks
- space
- computer
- ...and more!

## Dependencies 📦

- psutil (>= 5.9.0)
- rich (>= 10.12.0)

## Contributing 👥

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements or new features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙏

- Inspired by [neofetch](https://github.com/dylanaraps/neofetch)
- Built with [rich](https://github.com/Textualize/rich) for beautiful terminal rendering
- Uses [psutil](https://github.com/giampaolo/psutil) for system information gathering