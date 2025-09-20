# Installing Poppler for Windows

The PDF processing functionality requires poppler-utils to be installed. Here are several ways to install it:

## Option 1: Using Conda (Recommended)
If you have Anaconda or Miniconda installed:
```bash
conda install -c conda-forge poppler
```

## Option 2: Manual Installation
1. Download poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the zip file to a folder (e.g., `C:\poppler`)
3. Add the `bin` folder to your system PATH:
   - Open System Properties → Advanced → Environment Variables
   - Edit the PATH variable and add `C:\poppler\poppler-23.01.0\Library\bin`
   - Restart your terminal/IDE

## Option 3: Using Chocolatey
If you have Chocolatey installed:
```bash
choco install poppler
```

## Option 4: Using the automated installer
Run the provided installer script:
```bash
python install_poppler_windows.py
```

## Verify Installation
After installation, verify poppler is working:
```bash
pdftoppm -h
```

You should see the help text for pdftoppm if installation was successful.

## Troubleshooting
- Make sure to restart your terminal/IDE after installation
- Verify the PATH environment variable includes the poppler bin directory
- Try running `where pdftoppm` to check if the executable is found

Once poppler is installed, you should be able to upload PDF files successfully!