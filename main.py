import os
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import logging
from models import db, Character, NFT, Event, User

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "spnk_development_key")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
        nft = NFT(
            id=request.form.get('id'),
            name=request.form.get('name'),
            status=request.form.get('status'),
            description=request.form.get('description'),
            edition=request.form.get('edition'),
            rarity=request.form.get('rarity'),
            featured=bool(request.form.get('featured'))
        )
        
        db.session.add(nft)
        db.session.commit()
        
        flash('NFT added successfully', 'success')
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
