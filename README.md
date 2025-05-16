# Companion-1 Remote Control

[English](#english) | [中文](#chinese)

<a name="english"></a>
## Image Display and Control System

A web-based application for uploading, managing, and displaying images on monitors(such as Companion-1) connected to non-desktop version Linux, with remote control capabilities.

### Features

- No need to rely on the Linux desktop environment
- Based on frame buffer, with low resource usage
- Upload images from any browser
- Image gallery with thumbnails (for raster images, the original image can be customized as the thumbnail)
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

4. Run the application:
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
- `GET /get_folders` - Get list of all uploaded image folders
- `GET /uploads/<filename>` - Get URL for specific image
- `GET /thumbnails/<filename>` - Get URL for specific image thumbnail
- `POST /set_folder` - Set the current folder in use
- `POST /upload` - Upload new image
- `POST /show_image/<filename>` - Display specific image
- `POST /delete_image/<filename>` - Delete specific image
- `POST /startppt` - Start slideshow mode
- `POST /left` - Show previous image in slideshow
- `POST /right` - Show next image in slideshow
- `POST /startautoplay` - Start autoplay mode
- `POST /stopautoplay` - Stop autoplay mode
- `POST /shutdown` - Shutdown the Linux device

---

<a name="chinese"></a>
## 图像显示和控制系统

一个基于Web的应用程序，用于在非桌面版Linux连接的显示器上（如3D显示器Companion-1）执行上传、管理和显示图像，具有远程控制功能。

### 功能特点

- 不需要依赖Linux桌面环境
- 基于frame buffer，资源占用小
- 从任何浏览器上传图片
- 带有缩略图的图片库（对于光栅图可以自定义原始图为缩略图）
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

4. 运行应用程序：
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
- `GET /get_folders` - 获取所有上传图片的文件夹列表
- `GET /uploads/<filename>` - 获取特定图片的URL
- `GET /thumbnails/<filename>` - 获取特定图片的缩略图URL
- `POST /set_folder` - 设置当前使用的文件夹
- `POST /upload` - 上传新图片
- `POST /show_image/<filename>` - 显示特定图片
- `POST /delete_image/<filename>` - 删除特定图片
- `POST /startppt` - 启动幻灯片模式
- `POST /left` - 在幻灯片中显示上一张图片
- `POST /right` - 在幻灯片中显示下一张图片
- `POST /startautoplay` - 启动自动播放模式
- `POST /stopautoplay` - 停止自动播放模式
- `POST /shutdown` - 关闭Linux设备
