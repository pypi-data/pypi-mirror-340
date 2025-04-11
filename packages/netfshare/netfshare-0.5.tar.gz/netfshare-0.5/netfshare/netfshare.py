import os
import time
import zipfile
import json
import datetime
import socket
from functools import wraps
from pythonping import ping

from flask import (Flask, Blueprint, request, redirect, url_for, 
                   send_file, flash, render_template, session)
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, _
from flask_socketio import SocketIO

SHARED_DIRECTORY = os.getcwd()
app = Flask(__name__)
socketio = SocketIO(app)

# Register this module as view Blueprint
netfshare = Blueprint('netfshare', __name__)
 

# Config app
local_config = os.path.join(SHARED_DIRECTORY, '.netfshare', 'config.json')
print(f'Starting netfshare in {SHARED_DIRECTORY}...')
try:
    print('config from local file: ', local_config)
    app.config.from_file(local_config, load=json.load, text=False)
except Exception as e:
    print(f'Exception: {e}\nUsing default config.')
    app.config.from_object('netfshare.config')


# Localizazion setup
def get_locale():
    """
    Returns the best matching language for the user.
    """
    if 'language' in session:
        language = session['language']
    else:
        language = request.accept_languages.best_match(app.config['LANGUAGES'])    
        session['language'] = language
    return language

babel = Babel(app, locale_selector=get_locale)


# Config database
db_path = os.path.join(SHARED_DIRECTORY, '.netfshare', 'dir_config.db')
print(os.path.dirname(db_path))
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)

# DB models
class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.Integer, default=0)
    path = db.Column(db.String(64), nullable=True)
    # # Backref relationships to access directory from download and upload:
    downloads = db.relationship('Download', backref='directory')
    uploads = db.relationship('Upload', backref='directory')

    def __init__(self, path):
        self.path = path
        self.mode = 0

    def __repr__(self):
        return f'Directory: {self.path} (share mode {self.mode})'
    
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.now)
    selected_name = db.Column(db.String(64), nullable=True)
    selected_id = db.Column(db.String(64), nullable=True)
    # Backref relationships to access client from download and upload:
    downloads = db.relationship('Download', backref='client')
    uploads = db.relationship('Upload', backref='client')
    socket_connected = db.Column(db.Boolean, default=False)

    def __init__(self, address):
        self.address = address

    @property
    def active(self):
        if (datetime.datetime.now() - self.last_seen).total_seconds() < 15:
            return True
        elif self.socket_connected:
            return True
        else:
            return False
    @active.setter
    def active(self, value):
        if value:
            self.last_seen = datetime.datetime.now()


    def __repr__(self):
        if self.selected_name:
            return f'Client: {self.address} (Name: {self.selected_name}, ID: {self.selected_id}), active: {self.active}, (last seen {self.last_seen})'
        else:
            return f'Client: {self.address} (ID: {self.selected_id}), active: {self.active}, (last seen {self.last_seen})'
    
class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    directory_id = db.Column(db.Integer, db.ForeignKey('directory.id'))
    download_time = db.Column(db.DateTime, default=datetime.datetime.now)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    directory_id = db.Column(db.Integer, db.ForeignKey('directory.id'))
    upload_time = db.Column(db.DateTime, default=datetime.datetime.now)
    files_count = db.Column(db.Integer)

class ConfigBool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=True)
    value = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(256), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=True)
    message = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(256), nullable=True)
    category = db.Column(db.String(64), nullable=True)


# Scan the shared directory and add subdirectories to the DB
def add_shared_folders():
    """
    Scans the shared directory and adds subdirectories to the DB.
    """
    count_added = 0
    for directory in os.listdir(SHARED_DIRECTORY):
        if os.path.isdir(directory):
            if not Directory.query.filter(Directory.path == directory).first():
                db.session.add(Directory(directory))
                count_added += 1
    db.session.commit()
    return count_added

with app.app_context():
    db.create_all()
    count_added_dirs = add_shared_folders()

    # Initialize some default settings
    if not ConfigBool.query.filter(ConfigBool.name == 'allow_multiple_uploads').first():
        db.session.add(ConfigBool(
            name = "allow_multiple_uploads",
            # Read value from config.py, default to False
            value = app.config.get('ALLOW_MULTIPLE_UPLOADS', False),
            description = "Allow multiple user uploads to the same directory. Replaces existing files."
        ))
        db.session.commit()

    if not ConfigBool.query.filter(ConfigBool.name == 'require_name_id').first():
        db.session.add(ConfigBool(
            name = "require_name_id",
            # Read value from config.py, default to True
            value = app.config.get('REQUIRE_NAME_ID', True),
            description = "Require clients to id by providing their name along with their ID."
        ))
        db.session.commit()

    if not Message.query.filter(Message.name == 'default_message').first():
        db.session.add(Message(
            name = "default_message",
            message = '',
            description = "Default message, visible to all users.",
            category='info'
        ))
        db.session.commit()


# Command line output
bcolors = {
    "HEADER": '\033[95m',
    "OKBLUE": '\033[94m',
    "OKGREEN": '\033[92m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
}
host_ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
port = int(app.config.get("PORT", 5000))

print()
print(f'{bcolors["OKGREEN"]}File sever running at: {bcolors["ENDC"]}')
for ip in host_ips:
    print(f'\t{bcolors["OKBLUE"]}http://{ip}:{port}{bcolors["ENDC"]}')
print()


# Helper functions
def available_dirs(mode):
    """
    Returns a list of all directories that are available for the given mode.
    Excludes directories that are in the exclude_dirnames list.
    """
    all_dirs = [dir for dir in os.listdir(SHARED_DIRECTORY) if os.path.basename(dir) not in app.config["EXCLUDE_DIRNAMES"]]
    matching_mode_paths = [dir.path for dir in Directory.query.filter(Directory.mode==mode).all()]
    return [_ for _ in all_dirs if _ in matching_mode_paths]

def check_admin(request):
    is_admin = False
    if (request.remote_addr) in str(request.host):
        is_admin = True
    return is_admin

# User identification decorators
def id_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client = Client.query.filter(Client.address==request.remote_addr).first()
        print('client: ', client)
        if client is None:
            flash(_('No user ID set.'), 'warning')
            return redirect(url_for('identify'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = check_admin(request)
        if not admin:
            message = _('Admin access required. Redirecting to index...')
            flash(message, 'danger')
            print(message)
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


# Context processor to inject data into templates
@app.context_processor
def inject_client():
    context = {}
    context['admin'] = check_admin(request)
    
    client = Client.query.filter(Client.address==request.remote_addr).first()
    context['client'] = client
    if client is not None:
        client.active = True
        client.last_seen = datetime.datetime.now()
        db.session.commit()
    return context

@app.context_processor
def inject_config():
    context = {}
    messages = Message.query.all()
    context['permanent_messages'] = messages
    context['supported_languages'] = app.config['LANGUAGES']
    context['require_name_id'] = ConfigBool.query.filter(ConfigBool.name=='require_name_id').first().value
    return context


# Views
@app.route("/id", methods=["GET", "POST"])
def identify():
    """
    View to identify the user on first access.
    """
    # Client database query
    client = Client.query.filter(Client.address==request.remote_addr).first()
    if client is not None:
        return redirect('/')
    
    if request.method == 'POST':
        id = request.form.get('id')
        if id:
            client = Client(request.remote_addr)
            client.selected_id = id

            # handle name if required
            if ConfigBool.query.filter(ConfigBool.name=='require_name_id').first().value:
                name = request.form.get('name')
                if name:
                    client.selected_name = name
                else:
                    flash(_('Please input your name.'), 'error')
                    return redirect('/')

            db.session.add(client)
            db.session.commit()
            return redirect('/')
        else:
            flash(_('Please input your ID number.'), 'error')
            return redirect('/')
        
    return render_template('identify.html')

# SocketIO connect and disconnect events
@socketio.on('connect')
def handle_connect():
    client = Client.query.filter(Client.address==request.remote_addr).first()
    if client:
        client.socket_connected = True
        db.session.commit()


@socketio.on('disconnect')
def handle_disconnect():
    client = Client.query.filter(Client.address==request.remote_addr).first()
    if client:
        client.socket_connected = False
        db.session.commit()

@app.route("/", methods=["GET", "POST"])
@id_required
def list_dirs():
    """
    View to list directories on the server.
    """
    #not_shared_dirs = available_dirs(0)
    read_only_dirs = available_dirs(1)
    upload_only_dirs = available_dirs(2)
    
    return render_template(
        'list_dirs.html',
        read_only_dirs=read_only_dirs, 
        upload_only_dirs=upload_only_dirs
        )


@app.route("/download/<path>")
@id_required
def download(path):
    """
    Download read_only directory.
    Package the directory as a zip file and serves it.
    """
    if not os.path.isdir(os.path.join(SHARED_DIRECTORY, path)):
        print(path, ' not a directory')
        flash(_('%(path)s is not a shared directory.', path=path), 'warning')
        return redirect(url_for('list_dirs'))
    else:
        zip_file = os.path.join(SHARED_DIRECTORY, '.netfshare', path + '.zip')
        refresh_file = False
        if os.path.isfile(zip_file):
            if os.path.getmtime(zip_file) < os.path.getmtime(os.path.join(SHARED_DIRECTORY, path)):
                refresh_file = True
                print('files changed')
            elif os.path.getmtime(zip_file)-time.time() > app.config['REFRESH_TIME']:
                print('file expired')
                refresh_file = True

        if not os.path.isfile(zip_file) or refresh_file:
            print(f'generating zip file {zip_file}...')
            with zipfile.ZipFile(zip_file, 'w') as zipf:
                for root, dirs, files in os.walk(os.path.join(SHARED_DIRECTORY, path)):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, os.path.join(SHARED_DIRECTORY, path))                                
                        zipf.write(file_path, relative_path)

        # Record download
        client = Client.query.filter(Client.address==request.remote_addr).first()
        download = Download(client_id=client.id, directory_id=Directory.query.filter(Directory.path==path).first().id)
        download.download_time = datetime.datetime.now()
        db.session.add(download)
        db.session.commit()

        return send_file(zip_file, as_attachment=True)



@app.route("/upload/<path>", methods=["GET", "POST"])
@id_required
def upload_dir(path):
    """
    Select a file to upload to the selected (`path`) directory
    on the server.
    """
    if request.method == 'POST':
        target_path = os.path.join(SHARED_DIRECTORY, path)
        client = Client.query.filter(Client.address==request.remote_addr).first()
        
        if ConfigBool.query.filter(ConfigBool.name=='require_name_id').first().value:
            upload_name = client.selected_name.replace(' ', '_') + '_' + client.selected_id
        else:
            upload_name = client.selected_id
        
        allow_multiple = ConfigBool.query.filter(ConfigBool.name=='allow_multiple_uploads').first().value

        target_path = os.path.join(target_path, upload_name.strip())
        uploaded_files = request.files.getlist('file') 

        if len(uploaded_files) > app.config['MAX_FILES']:
            flash(_('Too many files. Max. %(num_files)d files per upload.', num_files=app.config['MAX_FILES']), 'warning')
            return redirect(url_for('upload_dir', path=path))
        
        if os.path.exists(target_path):
            if not allow_multiple:
                flash(_('An upload with the same ID already exists.'), 'warning')
                return redirect(url_for('upload_dir', path=path))
            else:
                flash(_('An upload with the same ID already exists. Files with matching names were overwritten.'), 'warning')
        
        for file in uploaded_files:
            if file:
                dirname = os.path.dirname(file.filename)
                save_dir = os.path.join(target_path, dirname)
                filename = os.path.basename(file.filename)
                # Handle nested subdirectories
                file_path = os.path.join(save_dir, filename)
                os.makedirs(save_dir, exist_ok=True)
                file.save(file_path)

        # Record upload
        client = Client.query.filter(Client.address==request.remote_addr).first()
        upload = Upload(client_id=client.id, directory_id=Directory.query.filter(Directory.path==path).first().id)
        upload.upload_time = datetime.datetime.now()
        upload.files_count = len(uploaded_files)
        db.session.add(upload)
        db.session.commit()

        flash(_('%(num_files)d files successfully uploaded.', num_files=len(uploaded_files)), 'success')
        return redirect(url_for('upload_dir', path=path))

    return render_template('upload.html', path=path)


@app.route("/copy_config")
@admin_required
def copy_config():
    """
    Copy the current app configuration to a local file.
    Service restart required to apply any local changes.
    """
    if check_admin(request):
        config_copy_keys = [
            'DEBUG', 'SECRET_KEY', 'WTF_CSRF_ENABLED', 'SQLALCHEMY_DATABASE_URI', 
            'REFRESH_TIME', 'SHARE_MODES', 'EXCLUDE_DIRNAMES', 'MAX_FILES', 'LANGUAGES', 'PORT',
        ]
        config_items = [(k, app.config[k]) for k in config_copy_keys if k in app.config.keys()]
        with open(local_config, 'w') as f:
            json.dump(dict(config_items), f, indent=2)
        flash('Configuration copied to local file. Service restart required to apply any local changes.', 'success')
        return redirect(url_for('admin_view'))
    else:
        return redirect(url_for('list_dirs'))


@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin_view():
    """
    Admin view to manage the app settings, sucs as directory share modes,
    user messages, clients, downloads and uploads in current session.
    """
    # Admin check and management forms
    context = {}
    # Populate shared dir management forms
    manage_dirs = [dir for dir in Directory.query.all() if dir.path in os.listdir(SHARED_DIRECTORY)]
    context['manage_dirs'] = manage_dirs

    # Populate `messages`
    message = Message.query.filter(Message.name=='default_message').first()
    context['default_message'] = message

    # Populate `configs`
    configs = ConfigBool.query.all()
    context['configs'] = configs

    # Validate and update share mode
    if request.method == 'POST':
        messages = {}
        for name, value in request.form.items():
            
            # handle dir modes
            if name in [str(d.id) for d in Directory.query.all()]:
                if value in [str(k) for k in app.config["SHARE_MODES"].keys()]:
                    dir = Directory.query.filter(Directory.id == int(name)).first()
                    dir.mode = int(value)
                    db.session.commit()

            # handle messages and configs
            elif name == 'default_message':
                message.message = value
                db.session.commit()
                print(f'Setting {message.name} to "{value}".')

            elif 'config' in name:
                config_id = int(name.split('_')[-1])
                config_value = bool(int(value))
                config = ConfigBool.query.filter(ConfigBool.id==config_id).first()
                config.value = config_value
                db.session.commit()
                print(f'setting {config.name} to {config_value}')

        return redirect(url_for('admin_view'))
    
    return render_template(
        'admin.html',
        share_modes=app.config["SHARE_MODES"],
        exclude_dirnames=app.config["EXCLUDE_DIRNAMES"],
        **context
        )


@app.route("/manage_session")
@admin_required
def manage_session():
    """
    View to manage the current session (clients' status, lists of 
    uploads and downlaods).
    """
    if check_admin(request):
        clients = Client.query.all()
        downloads = Download.query.all()
        uploads = Upload.query.all()

        # ping client to update last_seen
        for client in clients:
            response = ping(client.address, count=1, timeout=0.1)
            if response.success() or client.socket_connected:
                client.last_seen = datetime.datetime.now()
            db.session.commit()

        return render_template('manage_session.html',
                               clients=clients, downloads=downloads, uploads=uploads)
    else:
        return redirect(url_for('list_dirs'))


@app.route("/reset_session")
@admin_required
def reset_session():
    """
    Resets the current session by deleting the list of clients,
    uploads and downlooads.
    """
    print('reset_session, admin: ', check_admin(request))
    if check_admin(request):
        nd_client = Client.query.delete()
        nd_download = Download.query.delete()
        nd_upload = Upload.query.delete()
        db.session.commit()
        flash(f'Session reset. Deleted {nd_client} client, {nd_download} download and {nd_upload} upload records.', 'success')
        return redirect(url_for('manage_session'))
    else:
        return redirect(url_for('manage_session'))
    
@app.route("/delete_client/<client_id>")
@admin_required
def delete_client(client_id):
    """
    Delete a client from the session.
    """
    client = Client.query.filter(Client.id==client_id).first()
    selected_id = client.selected_id
    if client:
        db.session.delete(client)
        db.session.commit()
        flash(f'Client {selected_id} deleted.', 'success')
    return redirect(url_for('manage_session'))
    

@app.route("/scan_shared_dir")
@admin_required
def scan_shared_dir():
    """
    View to scan the shared directory and add subdirectories to the DB.
    """
    count_added = add_shared_folders()
    flash(f'Shared directory scanned and added {count_added} folders to the database.', 'success')
    return redirect(url_for('admin_view'))
    

@app.route('/set-language/<language>')
def set_language(language):
    """
    Set localization language.
    """
    if language in app.config['LANGUAGES']:
        session['language'] = language.strip()
        print('setting language to: ', session['language'])
    return redirect(request.referrer or '/')


if __name__ == "__main__":
    port = int(app.config.get("PORT", 5000))
    app.run(port=port, host='0.0.0.0')