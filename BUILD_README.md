# 2048 Game Build Tool

## Quick Start

### Build the Game
1. Double-click `build.bat`
2. Wait for the build to complete
3. Desktop shortcut will be created automatically

### Files

| File | Description |
|------|-------------|
| `build.bat` | Build script - double-click to build |
| `create_shortcut.vbs` | Creates desktop shortcut |
| `dist\2048.exe` | Game executable (created after build) |

## Usage

### First Time Build
1. Run `build.bat`
2. Wait 1-2 minutes for PyInstaller to package
3. Find `2048_Game.lnk` on your desktop
4. Double-click to play!

### Rebuild After Code Changes
1. Run `build.bat` again
2. Old files are cleaned automatically
3. New exe is created in `dist\` folder

## Troubleshooting

### "Python not found"
- Install Python 3.8+ from python.org
- Make sure to check "Add Python to PATH" during installation

### "PyInstaller not found"
- Run: `pip install pyinstaller`

### Build fails
- Delete `build` and `dist` folders manually
- Run `build.bat` again

## Manual Build (Alternative)

```batch
pyinstaller --onefile --windowed --name 2048 src\main.py
```
