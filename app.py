from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.utils import secure_filename 
import hashlib
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Thay thế bằng một secret key bất kỳ
app.config['UPLOADED_VIDEOS_DEST'] = 'static/uploads'
app.config['UPLOADED_VIDEOS_URL'] = '/static/uploads/videos/'
#app.config['UPLOADED_VIDEOS_URL'] = '/static/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db' 
app.config['SQLALCHEMY_BINDS'] = {
    'teachers': 'sqlite:///teachers.db',
    'students': 'sqlite:///students.db'
}   # Sử dụng SQLite database, bạn có thể thay đổi thành database khác nếu muốn

app.config['UPLOAD_FOLDER'] = 'static/uploads'
videos = UploadSet('videos', extensions=('mp4', 'avi', 'mov'))
configure_uploads(app, videos)
db = SQLAlchemy(app)

def create_tables():
    with app.app_context():
        db.create_all()

class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    def hash_password(self, password):
        # Hàm mã hóa mật khẩu sử dụng hashlib (SHA256)
        return hashlib.sha256(password.encode()).hexdigest()
    def set_password(self, password):
        # Hàm thiết lập mật khẩu mới và mã hóa nó
        self.password = self.hash_password(password)
    def check_password(self, input_password):
        # Hàm kiểm tra mật khẩu
        return self.password == self.hash_password(input_password)

    #def get_related_content(self):
        # Tìm các nội dung liên quan dựa trên các thẻ tag đã chọn
        #related_content = Content.query.filter(Content.tags.contains(self.tags)).all()
        #return related_content
class Students(User):
    __bind_key__ = 'students'
    tags = db.Column(db.String(200))
    report = db.Column(db.Text)
    def get_tags(self):
        if self.tags:
            tags_json = self.tags
            tags_list = json.loads(tags_json)  # Chuyển đổi chuỗi JSON thành list
            return tags_list
        else:
            return []
    
"""def get_videos_by_tag(tag):
    # Hàm này trả về danh sách các video dựa trên thẻ tag đã chọn
    courses = Courses.query.filter(Courses.tag == tag).all()
    return courses"""
#playlist_video_association = db.Table('playlist_video_association',
    #db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    #db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
#)
          
class Teachers(User):
    __bind_key__ = 'teachers'
    courses = db.relationship('Courses', backref='teacher', lazy=True)
    #username = db.Column(db.String(80), unique=True, nullable=False)   #thêm sau
    playlists = db.relationship('Playlist', backref='teacher', lazy=True)
    
    
class Courses(db.Model):
    __bind_key__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(200))
    #video_filename = db.Column(db.String(200))  # Thêm thuộc tính mới để lưu tên tệp video đã tải lên
    tag = db.Column(db.String(100))
    playlist = db.Column(db.Text)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    teacher_name = db.Column(db.String(80), nullable=False)
    
    
class Playlist(db.Model):
    __bind_key__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    

 # Assuming you have a playlist object, e.g., `playlist`
#video_ids = [video.id for video in playlist.videos]   
    
"""def get_teacher_playlists():
    teacher_playlists = []
    
    for teacher in Teachers.query.all():
        playlists = Playlist.query.filter_by(teacher_id=teacher.id).all()
        
        for playlist in playlists:
            playlist_tags = {}  # Dictionary to hold tags for each playlist's videos
            video_urls = []
            
            for course in Courses.query.filter(
                Courses.teacher_id == teacher.id,
                (Courses.playlist_id == playlist.id) | (Courses.playlist_id == None)
            ).all():
                if course.playlist_id is None:
                    pass
                else:
                    video_urls.append(course.video_url)
                    # Store tags in the playlist_tags dictionary for each video
                    for tag in course.tag.split(','):  # Assuming tags are comma-separated
                        playlist_tags[tag.strip()] = playlist_tags.get(tag.strip(), 0) + 1
            
            # Check if all videos in the playlist have the same tags
            unique_tags = [tag for tag, count in playlist_tags.items() if count == len(video_urls)]
            if unique_tags:
                tags = unique_tags
            else:
                tags = list(playlist_tags.keys())
            
            teacher_playlist = {
                'id': playlist.id,
                'teacher_id': teacher.id,
                'name': playlist.name,
                'playlist_videos': video_urls,
                'tags': tags,
                'num_videos': len(video_urls)
            }
            teacher_playlists.append(teacher_playlist)

    return teacher_playlists"""

def get_teacher_playlists():
    teacher_playlists = []
    
    for teacher in Teachers.query.all():
        playlists = Playlist.query.filter_by(teacher_id=teacher.id).all()
   
        
        for playlist in playlists:
            playlist_videos_by_tag = {}  # Dictionary to hold videos by tag
            video_urls = []
            
            for course in Courses.query.filter(
                Courses.teacher_id == teacher.id,
                (Courses.playlist_id == playlist.id) | (Courses.playlist_id == None)
            ).all():
                if course.playlist_id is None:
                    pass
                else:
                    video_urls.append(course.video_url)
                    # Group videos by tag
                    for tag in course.tag.split(','):  # Assuming tags are comma-separated
                        tag = tag.strip()
                        if tag not in playlist_videos_by_tag:
                            playlist_videos_by_tag[tag] = []
                        playlist_videos_by_tag[tag].append(course.video_url)
            
            # for tag, videos in playlist_videos_by_tag.items():
            #     # Create separate playlists for videos with different tags
            #     new_playlist_name = f"{playlist.name} - {tag}"
            #     new_playlist = {
            #         'id': playlist.id,
            #         'teacher_id': teacher.id,
            #         'name': new_playlist_name,
            #         'playlist_videos': videos,
            #         'tags': [tag],
            #         'num_videos': len(videos)
            #     }
            #     teacher_playlists.append(new_playlist)

            # Add the original playlist (with common tags among all videos) to the teacher_playlists
            unique_tags = [tag for tag, videos in playlist_videos_by_tag.items() if len(videos) == len(video_urls)]
            if unique_tags:
                tags = unique_tags
            else:
                tags = list(playlist_videos_by_tag.keys())
            
            original_playlist = {
                'id': playlist.id,
                'teacher_id': teacher.id,
                'name': playlist.name,
                'playlist_videos': video_urls,
                'tags': tags,
                'num_videos': len(video_urls),
                'teacher_name': teacher.username
            }
            teacher_playlists.append(original_playlist)

    return teacher_playlists
    

def tag_list():
    try:
        with open('tags list.txt', encoding='utf-8') as tep:
            tags = list(map(str.strip, tep.readlines()))
    except FileNotFoundError:
        tags = []

    return tags



def get_unique_filename(filename, upload_folder):
    """
    Trả về tên file duy nhất bằng cách thêm số thứ tự vào tên file nếu trùng lặp.
    Ví dụ: Nếu filename đã tồn tại, trả về 'filename(1).ext'.
    """
    name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(upload_folder, filename)):
        filename = f"{name}({counter}){ext}"
        counter += 1
    return filename
    
@app.route('/')
def home():
    return render_template("viewpage.html")

#def check_admin(name, password):
    data_admin = (
    ("An", {"password": "28082005"}),
    ("VietQuang", {"password": "456789"}),
    ("Hoàng", {"password": "123456"}),
    ("Tuệ_Mẫn", {"password": "Tuệ_Mẫn"})
)
    for admin_name, admin_password in data_admin:
        if admin_name == name:
            if admin_password["password"] == password:
                return True
            else:
                return False
    return False

#@app.route('/admin')
#def admin_login():
    error_message=None
    if request.method == "POST":
        name_admin_request = request.form['admin_name'] 
        name_admin_request =  request.form['password']     
        if check_admin(name_admin_request, name_admin_request):
            return redirect(url_for('admin_sys'))
        else:
            return render_template('home', error_message = "Tiễn vong")
        
#@app.route('/admin/sys', methods=['GET', 'POST'])
#def admin_sys():
    if request.method == "POST":
        video_id = request.form.get("video_id")
        video = Courses.query.get(video_id)  # Fetch the video from the 'Courses' table
        #general_content = Content.query.get(content_id)  # Fetch the general content from the 'Content' table

        if video:
            db.session.delete(video)
            db.session.commit()
            flash("Video đã được xóa thành công!")
        elif general_content:
            db.session.delete(general_content)
            db.session.commit()
            flash("Nội dung đã được xóa thành công!")
        else:
            flash("Không tìm thấy bài viết!")
        return redirect(url_for("admin_sys"))

    # Fetching both teacher videos and general content
    teachers_videos = Courses.query.all()  # Fetch teacher videos from the 'Courses' table
    general_content = Content.query.all()  # Fetch general user content from the 'Content' table

    teachers_videos.reverse()
    general_content.reverse()

    return render_template("admin.html", teachers_videos=teachers_videos, general_content=general_content)
 
@app.route('/logout')
def logout():
    # Clear the user's session data to log them out
    session.clear()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        # Xử lý thông tin đăng nhập
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        role = request.form.get('role')

        # Kiểm tra tên đăng nhập hoặc email
        if role == "hocvien":
            user = Students.query.filter((Students.username == username_or_email) | (Students.email == username_or_email)).first()
        elif role == "giaovien":
            user = Teachers.query.filter((Teachers.username == username_or_email) | (Teachers.email == username_or_email)).first()

        if user and user.check_password(password):
            # Đăng nhập thành công, chuyển hướng đến trang cá nhân của người dùng
            if role == "hocvien":
                return redirect(url_for('student_profile', username=user.username))
            elif role == "giaovien":
                return redirect(url_for('teacher_profile', username=user.username))
        else:
            error_message = "Tên đăng nhập hoặc mật khẩu không đúng!"

    return render_template('login.html', error_message=error_message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Xử lý thông tin đăng ký
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role')

        # Kiểm tra xem tên đăng nhập hoặc email đã tồn tại trong cơ sở dữ liệu chưa
        if role == "hocvien":
            if Students.query.filter((Students.username == username) | (Students.email == email)).first():
                return "Tên đăng nhập hoặc email đã tồn tại!"
            new_student = Students(username=username, email=email, password=User().hash_password(password))
            with app.app_context():
                db.session.add(new_student)
                db.session.commit()
        elif role == "giaovien":
            if Teachers.query.filter((Teachers.username == username) | (Teachers.email == email)).first():
                return "Tên đăng nhập hoặc email đã tồn tại!"
            new_teacher = Teachers(username=username, email=email, password=User().hash_password(password))
            with app.app_context():
                db.session.add(new_teacher)
                db.session.commit()

        # Chuyển hướng đến trang chủ sau khi đăng ký thành công
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/change_password/<username>/role/<role>', methods=['GET', 'POST'])
def change_password(username, role):


    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        role = request.form.get('role')
   
        if role == "hocvien":
            user = Students.query.filter_by(username=username).first()
        elif role == "giaovien":
            user = Teachers.query.filter_by(username=username).first()
 
            
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('home'))

        if new_password != confirm_password:
            flash('Password confirmation does not match!', 'danger')
            return render_template('change_password.html', username=username, role=role)

        # Cập nhật password mới và lưu vào cơ sở dữ liệu 
        #user.password = User().hash_password(new_password)
        #user.password = True
        #db.session.commit()
        
        user.set_password(new_password)  # Set and hash the new password
        db.session.commit()
        #with app.app_context():
         #   db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('change_password.html', username=username, role=role)


@app.route('/select_tags/<username>', methods=['GET', 'POST'])
def select_tags(username):
    tags = tag_list()
    user = Students.query.filter_by(username=username).first()
    if not user:
        return "User not found"
    if request.method == 'POST':
        tags_selected = request.form.getlist('tags')
        tags_json = json.dumps(tags_selected)  # Chuyển đổi list thành chuỗi JSON
        user.tags = tags_json
        db.session.commit()
        return redirect(url_for('student_profile', username=username))
    else:
        current_tags = user.get_tags()
        return render_template('select_tags.html', tags=tags, current_tags=current_tags, user=user)

@app.route('/playlist/<int:playlist_id>/<username>')
def playlist_page(playlist_id, username):
    # Lấy thông tin về playlist dựa trên playlist_id
    playlist = Playlist.query.get(playlist_id)  
    teacher = Teachers.query.filter_by(id=playlist.teacher_id).first()
    #thử
    
    playlists_show = []
    for course in Courses.query.filter(
                Courses.teacher_id == playlist.teacher_id,
                (Courses.playlist_id == playlist.id)).all():
        video_delta = {
                'id': playlist.id,
                'teacher_name': course.teacher_name,
                'name': playlist.name,
                'playlist_video': course.video_url,
                #'tags': tags,
                'title': course.title,
                'tag': course.tag,
                'description': course.description
            }
        playlists_show.append(video_delta)
                        
             
#dừng
    return render_template('playlist.html', playlist_id=playlist_id, playlist=playlist, playlists_show=playlists_show, teacher=teacher, username=username)
    
@app.route('/student/<username>')
def student_profile(username):
    user = Students.query.filter_by(username=username).first()
    tags = user.get_tags()  # Gọi hàm tags() của Students để lấy danh sách tags đã chọn
    
    if not tags:
        # Xử lý trường hợp phương thức get_tags() trả về None, có thể chuyển hướng đến trang select_tags
        return redirect(url_for('select_tags', username=username))
    
    # Tạo danh sách các điều kiện 'or_' cho mỗi thẻ tag đã chọn
    tag_conditions = [Courses.tag.in_(tags)]
    # Truy vấn danh sách video dựa trên các thẻ tag đã chọn
    videos_by_tags = Courses.query.filter(or_(*tag_conditions), Courses.playlist_id.is_(None)).all()
    
    teacher_playlists = get_teacher_playlists()

    return render_template('user_profile.html', username=username, tags=tags, videos_by_tags=videos_by_tags, teacher_playlists=teacher_playlists)




@app.route('/Teachers/<username>')
def teacher_profile(username):
    teacher = Teachers.query.filter_by(username=username).first()
    if not teacher:
        return "Teacher not found"

    courses = Courses.query.filter_by(teacher_id=teacher.id).all()
    courses.reverse()
    return render_template('teacher_profile.html', teacher=teacher, courses=courses, username=username )


@app.route('/Teachers/<username>/edit_video/<int:course_id>', methods=['GET', 'POST'])
def edit_video(username, course_id):
    teacher = Teachers.query.filter_by(username=username).first()
    if not teacher:
        return "Teacher not found"

    course = Courses.query.get_or_404(course_id)
    if course.teacher_id != teacher.id:
        return "You don't have permission to edit this video."

    if request.method == 'POST':
        course.title = request.form['title']
        course.tag = request.form['tag']
        course.description = request.form['description']
        # Thêm các phần xử lý cho việc chỉnh sửa nội dung video khác (nếu có)

        db.session.commit()
        return redirect(url_for('teacher_profile', username=username))

    return render_template('edit_video.html', teacher=teacher, course=course, tags=tag_list(), username=username)

@app.route('/Teachers/<username>/delete_video/<int:course_id>', methods=['GET', 'POST'])
def delete_video(username, course_id):
    teacher = Teachers.query.filter_by(username=username).first()
    if not teacher:
        return "Teacher not found"

    course = Courses.query.get_or_404(course_id)
    if course.teacher_id != teacher.id:
        return "You don't have permission to delete this video."

    if request.method == 'POST':
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('teacher_profile', username=username))

    return render_template('delete_video.html', teacher=teacher, course=course, username=username)




@app.route('/Teachers/<username>/upload_video', methods=['GET', 'POST'])
def upload_video(username):
    teacher = Teachers.query.filter_by(username=username).first()
    teacher_playlists = teacher.playlists if teacher else []
    
    #teacher_playlists = teacher.courses

    if not teacher:
            return "Teacher not found"
    if request.method == 'POST':
        video_file = request.files.get('video') 
        title = request.form['title']
        description = request.form['description']
        tag = request.form['tag']
        playlist = request.form.get('playlist')
        
  
        playlist_id = None
        if not playlist:
            playlist_text = None
        elif playlist == 'new':
            new_playlist_name = request.form.get('newPlaylist')
            if new_playlist_name:
                new_playlist = Playlist(name=new_playlist_name, teacher_id=teacher.id)
                db.session.add(new_playlist)
                db.session.commit()
                playlist_text = new_playlist.name
                playlist_id = new_playlist.id  #ông thêm phần này cho tui nha :>
        else:
            #playlist_text = playlist   cũ
            selected_playlist = Playlist.query.filter_by(name=playlist).first()
            if not selected_playlist:
                return "Selected playlist not found"

            playlist_text = selected_playlist.name
            playlist_id = selected_playlist.id
                

        
        if video_file and videos.file_allowed(video_file, video_file.filename):
            filename = secure_filename(video_file.filename)
            filename = get_unique_filename(filename, app.config["UPLOAD_FOLDER"])
            video_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            # Save the video to the server
            video_file.save(video_path)
            #video_url = f"{app.config['UPLOADED_VIDEOS_URL']}{filename}"  # Get the URL for the video
            # Get the relative URL for the video within the /static/uploads/videos/ directory
            video_url = url_for('uploaded_videos', filename=filename, _external=True) 
        
            
            if playlist_id is None:
                # For 'new' playlist, keep playlist_id as None
                new_video = Courses(title=title,
                                description=description,
                                video_url=video_url,
                                tag=tag,
                                teacher_id=teacher.id,
                                teacher_name=teacher.username,
                                playlist=playlist_text,
                                playlist_id=None
                                )
            else:
                new_video = Courses(title=title,
                                description=description,
                                video_url=video_url,
                                tag=tag,
                                teacher_id=teacher.id,
                                teacher_name=teacher.username,
                                playlist=playlist_text,
                                playlist_id=playlist_id
                                )            
            
            db.session.add(new_video)
            db.session.commit()
            return redirect(url_for('teacher_profile', username=teacher.username))
    tags = tag_list()
    return render_template('upload_video.html', tags=tags, username=username, teacher_playlists=teacher_playlists)

@app.route('/uploads/videos/<filename>')
def uploaded_videos(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=5000)

