# 🎨 img-to-ascii - Effortless Image to ASCII Conversion

[![Release](https://img.shields.io/badge/Download-Release-brightgreen)](https://github.com/create41/img-to-ascii/releases)

## 📖 Overview
`img-to-ascii` is a simple tool that lets you convert images into ASCII art using a Python command-line interface. Whether you're looking to create unique text art for your terminal or for social media, this tool makes it easy and fun. With intelligent resizing, you can adjust the output size, choose from different character sets, and save your creations as plain-text files or rendered PNG images.

## 🚀 Getting Started

### 💻 Requirements
To run this application, you need:

- A computer running Windows, macOS, or Linux.
- Python version 3.6 or later installed on your machine.
- Basic familiarity with using a terminal or command prompt.

### 🔄 Installation
1. Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
2. Open a terminal or command prompt.

### 📥 Download & Install
You can download the latest version of `img-to-ascii` from our [Releases page](https://github.com/create41/img-to-ascii/releases). 

1. Click on the link above to visit the page.
2. Download the appropriate file for your system.

Once downloaded, extract the files to a desired location on your computer.

### 📜 How to Use
After installing, you can run the application easily:

1. Open your terminal or command prompt.
2. Navigate to the folder where you extracted the files.
3. Type the following command to run the application:
   ```
   python img_to_ascii.py --input <path_to_image> --output <output_file>
   ```

**Here’s a breakdown of the command:**
- `--input <path_to_image>`: The path to the image file you want to convert.
- `--output <output_file>`: The name of the output file where the ASCII art will be saved.

For example:
```
python img_to_ascii.py --input my_image.jpg --output output.txt
```

### 🖼️ Resizing and Charset Options
To enhance your ASCII art, you may want to resize the output or select a specific character set. Use the `--resize` and `--charset` options.

For example:
```
python img_to_ascii.py --input my_image.jpg --output output.txt --resize 80x40 --charset standard
```

**Options:**
- `--resize <width>x<height>`: Set the width and height of the output.
- `--charset <option>`: Choose between standard, grayscale, or custom character sets.

### 📂 Output Formats
You can save your output in two formats:
1. **Plain-Text File**: A simple text file containing the ASCII representation of your image.
2. **Rendered PNG**: A visual representation of your ASCII art in PNG format.

To save as a PNG, add the `--render` parameter:
```
python img_to_ascii.py --input my_image.jpg --render --output output.png
```

### 🎨 Example Commands
- Convert image and save as text:
  ```
  python img_to_ascii.py --input my_photo.png --output art.txt
  ```
- Convert image with resizing:
  ```
  python img_to_ascii.py --input pets.jpg --output pet_art.txt --resize 100x50
  ```
- Convert image with custom charset:
  ```
  python img_to_ascii.py --input logo.png --output logo_art.txt --charset custom
  ```

### 🔍 Troubleshooting
If you encounter any issues while using the tool, here are a few common fixes:

- **Python not found**: Ensure Python is properly installed. Check your PATH settings.
- **File not found**: Make sure the file path you entered is correct.
- **Invalid options**: Refer to the help section by typing:
  ```
  python img_to_ascii.py --help
  ```

### ✍️ Contribute
If you wish to contribute to the project, feel free to fork the repository and submit a pull request. We welcome improvements, bug fixes, or enhancements. 

### 📞 Support
For additional help or inquiries, visit the GitHub Issues page. You can report bugs or ask questions there. 

### 📢 Follow Upgrades
Stay updated with new features and improvements by checking our [Releases page](https://github.com/create41/img-to-ascii/releases) regularly. 

Start creating your ASCII artwork today! 