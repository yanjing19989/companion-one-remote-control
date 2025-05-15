# Companion-1 Remote Control

[English](#english) | [中文](#chinese)

<a name="english"></a>
## Image Display and Control System

A web-based application for uploading, managing, and displaying images on a connected display (such as Companion-1), with remote control capabilities.

### Features

- Upload images from any browser
- Image gallery with thumbnails
- Display selected images on connected screen
- Image slideshow mode with navigation controls
- Delete unwanted images
- Automatically switch images
- Select a subfolders and only use images within that folder
- Remote control through web interface

### Requirements

- Python 3.6+
- Flask
- PIL/Pillow
- FBI image viewer (on Linux device)
- Web browser

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/companion-1-remote-control.git
   cd companion-1-remote-control
   ```

2. Install required packages:
   ```
   pip install flask pillow
   ```

3. Install FBI on your Linux device and test display functionality:
   ```
   sudo apt-get install fbi
   sudo fbi -T 1 -a -noverbose 1.jpg
   ```

4. Ensure the upload directories exist:
   ```
   mkdir -p web/up_pic/uploads
   mkdir -p web/up_pic/thumbnails
   ```

5. Run the application:
   ```
   python web.py
   ```

### Usage

1. Access the web interface by navigating to `http://[device-ip]:5000` in your browser
2. Upload images through the interface
3. Click on images to display them on the connected screen
4. Use slideshow controls to browse through images
5. Delete unwanted images with the delete button

### API Endpoints

- `GET /` - Main web interface
- `GET /get_images` - Get list of all uploaded images
- `POST /upload` - Upload new image
- `POST /show_image/<filename>` - Display specific image
- `POST /delete_image/<filename>` - Delete specific image
- `POST /startppt` - Start slideshow mode
- `POST /left` - Show previous image in slideshow
- `POST /right` - Show next image in slideshow

---

<a name="chinese"></a>
## 图像显示和控制系统

一个基于Web的应用程序，用于在连接的显示器（如3D显示器Companion-1）上执行上传、管理和显示图像，具有远程控制功能。

### 功能特点

- 从任何浏览器上传图片
- 带有缩略图的图片库
- 在连接的屏幕上显示选定的图片
- 图片幻灯片模式和导航控制
- 删除不需要的图片
- 自动切换图片
- 选定子文件夹并只使用该文件夹下的图片
- 通过Web界面进行远程控制

### 系统要求

- Python 3.6+
- Flask
- PIL/Pillow
- FBI图像查看器（Linux设备上）
- Web浏览器

### 安装方法

1. 克隆此仓库：
   ```
   git clone https://github.com/yourusername/companion-1-remote-control.git
   cd companion-1-remote-control
   ```

2. 安装所需的包：
   ```
   pip install flask pillow
   ```

3. 在Linux设备上安装FBI并测试显示功能：
   ```
   sudo apt-get install fbi
   sudo fbi -T 1 -a -noverbose 1.jpg
   ```

4. 确保上传目录存在：
   ```
   mkdir -p web/up_pic/uploads
   mkdir -p web/up_pic/thumbnails
   ```

5. 运行应用程序：
   ```
   python web.py
   ```

### 使用方法

1. 在浏览器中访问`http://[设备IP]:5000`来打开Web界面
2. 通过界面上传图片
3. 点击图片在连接的屏幕上显示
4. 使用幻灯片控制浏览图片
5. 使用删除按钮删除不需要的图片

### API端点

- `GET /` - 主Web界面
- `GET /get_images` - 获取所有上传图片的列表
- `POST /upload` - 上传新图片
- `POST /show_image/<filename>` - 显示特定图片
- `POST /delete_image/<filename>` - 删除特定图片
- `POST /startppt` - 启动幻灯片模式
- `POST /left` - 在幻灯片中显示上一张图片
- `POST /right` - 在幻灯片中显示下一张图片
