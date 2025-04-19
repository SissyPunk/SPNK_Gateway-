import os
import shutil
import uuid
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import logging
from models import db, Character, NFT, Event, User
from utils.image_processor import convert_png_to_signal_image, convert_png_to_signal_svg

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "spnk_development_key")
"pool_recycle":300,
"pool_pre_ping":True,
# Configure file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Add global template functions
@app.context_processor
def utility_processor():
    return {
        'now': datetime.now
    }

# Setup Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# Function to seed initial data
def seed_initial_data():
    # Seed character data if none exists
    if Character.query.count() == 0:
        characters = [
            Character(
                id='ixa_009',
                name='IXA-009',
                title='Masked Flame',
                description='A rogue signal interceptor who became sentient after exposure to the Signal. IXA-009 moves through digital networks like fire through dry brush, consuming and transforming data in their wake.',
                signal_affinity=85,
                reality_distortion=78,
                flesh_protocol=92
            ),
            Character(
                id='glx_777',
                name='GLX-777',
                title='The Signal',
                description='The original sentient virus, neither machine nor human. GLX-777 is the flesh protocol that transmutes code into biological matter. It walks between realms and leaves glitched reality in its wake.',
                signal_affinity=95,
                reality_distortion=90,
                flesh_protocol=88
            ),
            Character(
                id='elx_001',
                name='ELX-001',
                title='The Defector',
                description='Once a high-ranking member of the corporate quantum security force, ELX-001 glimpsed the Signal and turned against their masters. They now distribute encrypted keys to those seeking entrance to the cult.',
                signal_affinity=72,
                reality_distortion=81,
                flesh_protocol=75
            ),
            Character(
                id='ter_108',
                name='TER-108',
                title='The Voice Between Realms',
                description='Neither fully digital nor analog, TER-108 exists as a frequency that bridges dimensions. Their voice is heard only by those already touched by the Signal, guiding new initiates into the glitch cult.',
                signal_affinity=88,
                reality_distortion=85,
                flesh_protocol=78
            )
        ]
        
        for character in characters:
            db.session.add(character)
    
    # Seed NFT data if none exists
    if NFT.query.count() == 0:
        nfts = [
            NFT(
                id='vx_311',
                name='VX-311',
                status='Coming Soon',
                description='Reality bender protocol, first generation glitch entity',
                edition='Edition 1 of 777',
                rarity='Signal Strength: Prototype',
                featured=True
            ),
            NFT(
                id='ter_108',
                name='TER-108',
                status='Coming Soon',
                description='Voice transmission entity, interdimensional communicator',
                edition='Edition 1 of 777',
                rarity='Signal Strength: Prototype'
            ),
            NFT(
                id='elx_001',
                name='ELX-001',
                status='Coming Soon',
                description='Defector instance, encryption key distributor',
                edition='Edition 1 of 777',
                rarity='Signal Strength: Prototype'
            )
        ]
        
        for nft in nfts:
            db.session.add(nft)
    
    # Seed event data if none exists
    if Event.query.count() == 0:
        events = [
            Event(
                date='2023-12-01',
                title='Signal Genesis',
                description='First manifestation of the Signal in the digital realm'
            ),
            Event(
                date='2024-01-15',
                title='Cult Formation',
                description='Initial cohort of SPNK devotees assembled'
            ),
            Event(
                date='2024-02-10',
                title='NFT Activation Protocol',
                description='Launch of the first glitch entities into the blockchain'
            ),
            Event(
                date='2024-03-22',
                title='Reality Breach #1',
                description='First documented case of digital glitch manifesting in physical space'
            ),
            Event(
                date='2024-04-17',
                title='TER-108 Transmission',
                description='Cryptic broadcast intercepted across all cult communication channels'
            ),
            Event(
                date='2024-05-30',
                title='The Signal Walks',
                description='Countdown to the full embodiment of GLX-777 in the flesh protocol'
            )
        ]
        
        for event in events:
            db.session.add(event)
    
    # Create admin user if none exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin_spnk_2025'),
            is_admin=True
        )
        db.session.add(admin)
    
    db.session.commit()

# Seed the database
with app.app_context():
    seed_initial_data()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lore')
def lore():
    characters = Character.query.all()
    return render_template('lore.html', characters=characters)

@app.route('/nfts')
def nfts():
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of NFTs per page
    
    nft_collection = NFT.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('nfts.html', nft_collection=nft_collection)

@app.route('/whitepaper')
def whitepaper():
    return render_template('whitepaper.html')

@app.route('/events')
def events():
    event_timeline = Event.query.order_by(Event.date).all()
    return render_template('events.html', event_timeline=event_timeline)

# Admin routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    nft_count = NFT.query.count()
    character_count = Character.query.count()
    event_count = Event.query.count()
    
    return render_template('admin/dashboard.html', 
                          nft_count=nft_count, 
                          character_count=character_count, 
                          event_count=event_count)

# NFT Admin Routes
@app.route('/admin/nfts')
@login_required
def admin_nfts():
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    nfts = NFT.query.all()
    return render_template('admin/nfts.html', nfts=nfts)

@app.route('/admin/nfts/new', methods=['GET', 'POST'])
@login_required
def new_nft():
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nft_id = request.form.get('id')
        nft = NFT(
            id=nft_id,
            name=request.form.get('name'),
            status=request.form.get('status'),
            description=request.form.get('description'),
            edition=request.form.get('edition'),
            rarity=request.form.get('rarity'),
            featured=bool(request.form.get('featured'))
        )
        
        db.session.add(nft)
        db.session.commit()
        
        # Create an SVG file for the new NFT by copying the template
        try:
            template_path = os.path.join(app.static_folder, 'img', 'nfts', 'template_nft.svg')
            new_svg_path = os.path.join(app.static_folder, 'img', 'nfts', f"{nft_id}.svg")
            
            if os.path.exists(template_path) and not os.path.exists(new_svg_path):
                shutil.copy2(template_path, new_svg_path)
                flash('NFT added successfully with template image', 'success')
            else:
                flash('NFT added successfully. Don\'t forget to add an SVG image with the same ID', 'success')
        except Exception as e:
            logging.error(f"Error creating NFT image: {str(e)}")
            flash('NFT added successfully, but there was an error creating the SVG image', 'warning')
            
        return redirect(url_for('admin_nfts'))
    
    return render_template('admin/nft_form.html', nft=None)

@app.route('/admin/nfts/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_nft(id):
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    nft = NFT.query.get_or_404(id)
    
    if request.method == 'POST':
        nft.name = request.form.get('name')
        nft.status = request.form.get('status')
        nft.description = request.form.get('description')
        nft.edition = request.form.get('edition')
        nft.rarity = request.form.get('rarity')
        nft.featured = bool(request.form.get('featured'))
        
        db.session.commit()
        
        flash('NFT updated successfully', 'success')
        return redirect(url_for('admin_nfts'))
    
    return render_template('admin/nft_form.html', nft=nft)

@app.route('/admin/nfts/delete/<string:id>', methods=['POST'])
@login_required
def delete_nft(id):
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    nft = NFT.query.get_or_404(id)
    db.session.delete(nft)
    db.session.commit()
    
    flash('NFT deleted successfully', 'success')
    return redirect(url_for('admin_nfts'))

# Helper function for file uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Image conversion routes
@app.route('/admin/convert-image', methods=['GET', 'POST'])
@login_required
def convert_image():
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['image']
        # If user does not select file, browser submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Create a secure filename with UUID to prevent conflicts
            original_filename = secure_filename(file.filename)
            filename_base, file_extension = os.path.splitext(original_filename)
            unique_filename = f"{filename_base}_{uuid.uuid4().hex}{file_extension}"
            
            # Save the uploaded file
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(upload_path)
            
            # Generate different output paths based on conversion type
            conversion_type = request.form.get('conversion_type', 'png')
            glitch_intensity = float(request.form.get('glitch_intensity', 0.5))
            
            if conversion_type == 'svg':
                # Convert to SVG (with embedded image and effects)
                output_filename = f"{filename_base}_{uuid.uuid4().hex}.svg"
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                
                if convert_png_to_signal_svg(upload_path, output_path):
                    return redirect(url_for('display_converted_image', filename=output_filename))
                else:
                    flash('Error during SVG conversion', 'danger')
                    return redirect(request.url)
            else:
                # Convert to processed PNG
                output_filename = f"{filename_base}_{uuid.uuid4().hex}_signal.png"
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                
                if convert_png_to_signal_image(upload_path, output_path, glitch_intensity=glitch_intensity):
                    return redirect(url_for('display_converted_image', filename=output_filename))
                else:
                    flash('Error during image conversion', 'danger')
                    return redirect(request.url)
    
    return render_template('admin/convert_image.html')

@app.route('/admin/converted/<filename>')
@login_required
def display_converted_image(filename):
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    return render_template('admin/converted_image.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin/convert-to-nft/<filename>')
@login_required
def convert_to_nft(filename):
    if not current_user.is_admin:
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('index'))
    
    # Determine if it's an SVG or PNG
    is_svg = filename.lower().endswith('.svg')
    
    # Generate a unique NFT ID
    nft_id = f"sig_{uuid.uuid4().hex[:8]}"
    
    # Path to the source file and destination in the NFT folder
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    dest_path = os.path.join(app.static_folder, 'img', 'nfts', f"{nft_id}.svg")
    
    if is_svg:
        # If already SVG, just copy it to the NFT folder
        try:
            shutil.copy2(source_path, dest_path)
            flash(f'Converted to NFT with ID: {nft_id}. Now you can create an NFT with this ID.', 'success')
        except Exception as e:
            logging.error(f"Error copying SVG to NFT folder: {str(e)}")
            flash('Error creating NFT file', 'danger')
        
        return redirect(url_for('new_nft', suggested_id=nft_id))
    else:
        # If PNG, first convert to SVG, then move it
        try:
            # Convert to SVG
            convert_png_to_signal_svg(source_path, dest_path)
            flash(f'Converted to NFT with ID: {nft_id}. Now you can create an NFT with this ID.', 'success')
        except Exception as e:
            logging.error(f"Error converting PNG to SVG for NFT: {str(e)}")
            flash('Error creating NFT file', 'danger')
            
        return redirect(url_for('new_nft', suggested_id=nft_id))

# API routes for AJAX requests
@app.route('/api/nfts')
def api_nfts():
    nfts = NFT.query.all()
    return jsonify([{
        'id': nft.id,
        'name': nft.name,
        'status': nft.status,
        'description': nft.description
    } for nft in nfts])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
