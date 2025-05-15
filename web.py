from flask import Flask, request, render_template, redirect, jsonify, url_for, send_from_directory
import os
from PIL import Image
import uuid
import time

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
THUMBNAIL_FOLDER = './thumbnails'
lastpid = None
os.system(f'sudo killall fbi')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
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

def show_image(index):
    global filelist
    os.system(f'sudo fbi -T 1 -a -noverbose {UPLOAD_FOLDER}/{filelist[index]}')
    global lastpid
    if lastpid:
        os.system(f'sudo kill -9 {lastpid}')
    lastpid = os.popen('pgrep fbi | tail -n 1').read().strip()
    print(filelist[index])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/thumbnails/<filename>')
def thumbnail_file(filename):
    return send_from_directory(THUMBNAIL_FOLDER, filename)

@app.route('/get_images')
def get_images():
    images = []
    for file in os.listdir(UPLOAD_FOLDER):
        if file.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
            # 检查是否已有缩略图，没有则创建
            thumb_path = os.path.join(THUMBNAIL_FOLDER, f"{os.path.splitext(file)[0]}.jpg")
            if not os.path.exists(thumb_path):
                create_thumbnail(os.path.join(UPLOAD_FOLDER, file), file)
            
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
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.system(f'sudo fbi -T 1 -a -noverbose {filepath}')
            global lastpid
            if lastpid:
                os.system(f'sudo kill -9 {lastpid}')
            lastpid = os.popen('pgrep fbi | tail -n 1').read().strip()
            return jsonify({'success': True, 'message': f'Image {filename} displayed'})
        else:
            return jsonify({'success': False, 'message': 'Image not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
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
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
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
    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
            filelist.append(file)
    findex = 0
    listsize = len(filelist)
    show_image(findex)
    return jsonify({'success': True, 'message': 'started'})

@app.route('/left', methods=['POST'])
def left():
    global listsize, findex, lasttime
    findex = (findex-1)%listsize
    show_image(findex)
    return jsonify({'success': True, 'message': 'left'})

@app.route('/right', methods=['POST'])
def right():
    global listsize, findex, lasttime
    findex = (findex+1)%listsize
    show_image(findex)
    return jsonify({'success': True, 'message': 'right'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')