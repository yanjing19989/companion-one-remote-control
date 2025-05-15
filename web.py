from flask import Flask, request, render_template, redirect, jsonify, url_for, send_from_directory
import os
from PIL import Image
import time
import threading

app = Flask(__name__)
BASE_UPLOAD_DIR = './uploads'
THUMBNAIL_FOLDER = './thumbnails'
CURRENT_UPLOAD_FOLDER = BASE_UPLOAD_DIR  # 默认使用基础目录
lastpid = None
auto_play_active = False
auto_play_thread = None

# sd卡超频
# os.system('echo 100000000 | sudo tee /sys/kernel/debug/mmc0/clock')
os.system(f'sudo killall fbi')

if not os.path.exists(BASE_UPLOAD_DIR):
    os.makedirs(BASE_UPLOAD_DIR)
if not os.path.exists(THUMBNAIL_FOLDER):
    os.makedirs(THUMBNAIL_FOLDER)

def create_thumbnail(image_path, filename):
    """创建缩略图并保存"""
    try:
        img = Image.open(image_path)
        img.thumbnail((256, 512))
        thumb_path = os.path.join(THUMBNAIL_FOLDER, f"{os.path.splitext(filename)[0]}.jpg")
        img.convert("RGB").save(thumb_path, "JPEG", optimize=True)
        return thumb_path
    except Exception as e:
        print(f"缩略图创建失败: {e}")
        return None

def get_all_folders(base_dir):
    """获取base_dir下所有子文件夹，包括base_dir本身"""
    folders = [base_dir]
    
    for root, dirs, _ in os.walk(base_dir):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            folders.append(full_path)
    
    return folders

def show_image(filepath):
    os.system(f'sudo fbi -T 1 -a -noverbose {os.path.join(CURRENT_UPLOAD_FOLDER, filepath)}')
    # os.system(f'echo your_sudo_password | sudo -S fbi -T 1 -a -noverbose {filepath}') # 如果不使用sudo启动，需要脚本申请sudo权限
    global lastpid
    if lastpid:
        os.system(f'sudo kill -9 {lastpid}')
    lastpid = os.popen('pgrep fbi | tail -n 1').read().strip()

def stop_auto_play():
    global auto_play_active, auto_play_thread
    auto_play_active = False
    if auto_play_thread and auto_play_thread.is_alive():
        auto_play_thread.join(0.1)  # 等待线程结束，设置短超时

def auto_play(interval=5):
    global auto_play_active, findex
    while auto_play_active:
        time.sleep(interval)  # 等待指定的间隔
        if auto_play_active:  # 再次检查，以便及时响应停止命令
            findex = (findex + 1) % listsize
            show_image(findex)

@app.route('/get_folders')
def get_folders():
    """返回可用的文件夹列表"""
    folders = get_all_folders(BASE_UPLOAD_DIR)
    # 转换为相对于BASE_UPLOAD_DIR的路径，使显示更简洁
    folder_options = []
    for folder in folders:
        if folder == BASE_UPLOAD_DIR:
            display_name = "根目录"
        else:
            display_name = folder.replace(BASE_UPLOAD_DIR + '/', '')
        
        folder_options.append({
            'path': folder,
            'display_name': display_name
        })
    
    return jsonify({
        'folders': folder_options,
        'current_folder': CURRENT_UPLOAD_FOLDER
    })

@app.route('/set_folder', methods=['POST'])
def set_folder():
    """设置当前使用的文件夹"""
    global CURRENT_UPLOAD_FOLDER
    
    folder_path = request.json.get('folder_path')
    # 确保只能选择BASE_UPLOAD_DIR下的文件夹
    if not folder_path.startswith(BASE_UPLOAD_DIR):
        return jsonify({'success': False, 'message': '无效的文件夹路径'})
    
    # 确保文件夹存在
    if not os.path.isdir(folder_path):
        return jsonify({'success': False, 'message': '文件夹不存在'})
    
    CURRENT_UPLOAD_FOLDER = folder_path
    
    # 确保目录存在
    if not os.path.exists(CURRENT_UPLOAD_FOLDER):
        os.makedirs(CURRENT_UPLOAD_FOLDER)
    
    return jsonify({
        'success': True, 
        'message': f'已切换到文件夹: {folder_path}',
        'current_folder': CURRENT_UPLOAD_FOLDER
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """修改为支持子文件夹的文件访问"""
    # 从CURRENT_UPLOAD_FOLDER的相对路径获取文件
    return send_from_directory(CURRENT_UPLOAD_FOLDER, filename)

@app.route('/thumbnails/<filename>')
def thumbnail_file(filename):
    return send_from_directory(THUMBNAIL_FOLDER, filename)

@app.route('/get_images')
def get_images():
    images = []
    for file in os.listdir(CURRENT_UPLOAD_FOLDER):
        file_path = os.path.join(CURRENT_UPLOAD_FOLDER, file)
        if os.path.isfile(file_path) and file.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
            # 检查是否已有缩略图，没有则创建
            thumb_path = os.path.join(THUMBNAIL_FOLDER, f"{os.path.splitext(file)[0]}.jpg")
            if not os.path.exists(thumb_path):
                create_thumbnail(file_path, file)
            
            images.append({
                'id': file,
                'name': file,
                'thumbnail_url': url_for('thumbnail_file', filename=f"{os.path.splitext(file)[0]}.jpg"),
                'image_url': url_for('uploaded_file', filename=file)
            })
    return jsonify(images)

@app.route('/show_image/<filename>', methods=['POST'])
def show_selected_image(filename):
    try:
        filepath = os.path.join(CURRENT_UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            show_image(filepath)
            return jsonify({'success': True, 'message': f'Image {filename} displayed'})
        else:
            return jsonify({'success': False, 'message': 'Image not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    try:
        filepath = os.path.join(CURRENT_UPLOAD_FOLDER, filename)
        thumb_path = os.path.join(THUMBNAIL_FOLDER, f"{os.path.splitext(filename)[0]}.jpg")
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
        return jsonify({'success': True, 'message': f'Image {filename} deleted'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    # 在BASE_UPLOAD_DIR目录下搜索，如果已经存在同名文件，则返回失败
    for path, dirs, files in os.walk(BASE_UPLOAD_DIR):
        print(path, dirs, files)
        if file.filename in files:
            return jsonify({'success': False, 'message': '文件已存在，请重命名后再上传'})
    if file:
        filepath = os.path.join(CURRENT_UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        # 创建缩略图
        create_thumbnail(filepath, file.filename)
        
        os.system(f'sudo fbi -T 1 -a -noverbose {filepath}')
        global lastpid
        if lastpid:
            os.system(f'sudo kill -9 {lastpid}')
        lastpid = os.popen('pgrep fbi | tail -n 1').read().strip()
        return jsonify({'success': True, 'message': 'File uploaded and processed successfully'})
    return jsonify({'success': False, 'message': 'File upload failed'})

@app.route('/startppt', methods=['POST'])
def startppt():
    # filelist 当前目录下的所有图片文件
    global listsize, findex, filelist, lasttime
    filelist = []
    for file in os.listdir(CURRENT_UPLOAD_FOLDER):
        if os.path.isfile(os.path.join(CURRENT_UPLOAD_FOLDER, file)) and (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg')):
            filelist.append(file)
    findex = 0
    listsize = len(filelist)
    # os.system(f'echo your_sudo_password | sudo -S fbi -T 1 -a -noverbose {filelist[findex]}') # 如果不使用sudo启动，需要脚本申请sudo权限
    if listsize > 0:
        show_image(filelist[findex])
    else:
        return jsonify({'success': False, 'message': '当前文件夹没有图片'})
    return jsonify({'success': True, 'message': 'started'})

@app.route('/left', methods=['POST'])
def left():
    global listsize, findex, filelist, lasttime
    stop_auto_play()  # 手动操作时停止轮播
    findex = (findex-1)%listsize
    show_image(filelist[findex])
    return jsonify({'success': True, 'message': 'left'})

@app.route('/right', methods=['POST'])
def right():
    global listsize, findex, filelist, lasttime
    stop_auto_play()  # 手动操作时停止轮播
    findex = (findex+1)%listsize
    show_image(filelist[findex])
    return jsonify({'success': True, 'message': 'right'})

@app.route('/startautoplay', methods=['POST'])
def start_auto_play():
    global auto_play_active, auto_play_thread, filelist, listsize, findex
    
    # 先初始化filelist
    filelist = []
    for file in os.listdir(CURRENT_UPLOAD_FOLDER):
        if os.path.isfile(os.path.join(CURRENT_UPLOAD_FOLDER, file)) and (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg')):
            filelist.append(file)
    
    findex = 0
    listsize = len(filelist)
    
    if listsize == 0:
        return jsonify({'success': False, 'message': '当前文件夹没有图片'})
    
    if listsize > 0:
        show_image(findex)
    
    # interval = request.json.get('interval', 5)  # 从请求中获取间隔时间，默认5秒
    interval = 30  # 默认30秒间隔
    
    # 确保之前的轮播已经停止
    stop_auto_play()
    
    # 启动新的轮播
    auto_play_active = True
    auto_play_thread = threading.Thread(target=auto_play, args=(interval,))
    auto_play_thread.daemon = True
    auto_play_thread.start()
    
    return jsonify({'success': True, 'message': f'Auto play started with interval {interval} seconds'})

@app.route('/stopautoplay', methods=['POST'])
def stop_auto_play_route():
    stop_auto_play()
    return jsonify({'success': True, 'message': 'Auto play stopped'})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # 3秒后关机
    os.system(f'sudo shutdown -h +3')
    return jsonify({'success': True, 'message': 'shutdown'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')