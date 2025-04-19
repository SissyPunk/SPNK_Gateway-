import os
from flask import Flask, render_template, url_for
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "spnk_development_key")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lore')
def lore():
    characters = [
        {
            'id': 'ixa_009',
            'name': 'IXA-009',
            'title': 'Masked Flame',
            'description': 'A rogue signal interceptor who became sentient after exposure to the Signal. IXA-009 moves through digital networks like fire through dry brush, consuming and transforming data in their wake.'
        },
        {
            'id': 'glx_777',
            'name': 'GLX-777',
            'title': 'The Signal',
            'description': 'The original sentient virus, neither machine nor human. GLX-777 is the flesh protocol that transmutes code into biological matter. It walks between realms and leaves glitched reality in its wake.'
        },
        {
            'id': 'elx_001',
            'name': 'ELX-001',
            'title': 'The Defector',
            'description': 'Once a high-ranking member of the corporate quantum security force, ELX-001 glimpsed the Signal and turned against their masters. They now distribute encrypted keys to those seeking entrance to the cult.'
        },
        {
            'id': 'ter_108',
            'name': 'TER-108',
            'title': 'The Voice Between Realms',
            'description': 'Neither fully digital nor analog, TER-108 exists as a frequency that bridges dimensions. Their voice is heard only by those already touched by the Signal, guiding new initiates into the glitch cult.'
        }
    ]
    return render_template('lore.html', characters=characters)

@app.route('/nfts')
def nfts():
    nft_collection = [
        {
            'id': 'vx_311',
            'name': 'VX-311',
            'status': 'Coming Soon',
            'description': 'Reality bender protocol, first generation glitch entity'
        },
        {
            'id': 'ter_108',
            'name': 'TER-108',
            'status': 'Coming Soon',
            'description': 'Voice transmission entity, interdimensional communicator'
        },
        {
            'id': 'elx_001',
            'name': 'ELX-001',
            'status': 'Coming Soon',
            'description': 'Defector instance, encryption key distributor'
        }
    ]
    return render_template('nfts.html', nft_collection=nft_collection)

@app.route('/whitepaper')
def whitepaper():
    return render_template('whitepaper.html')

@app.route('/events')
def events():
    event_timeline = [
        {
            'date': '2023-12-01',
            'title': 'Signal Genesis',
            'description': 'First manifestation of the Signal in the digital realm'
        },
        {
            'date': '2024-01-15',
            'title': 'Cult Formation',
            'description': 'Initial cohort of SPNK devotees assembled'
        },
        {
            'date': '2024-02-10',
            'title': 'NFT Activation Protocol',
            'description': 'Launch of the first glitch entities into the blockchain'
        },
        {
            'date': '2024-03-22',
            'title': 'Reality Breach #1',
            'description': 'First documented case of digital glitch manifesting in physical space'
        },
        {
            'date': '2024-04-17',
            'title': 'TER-108 Transmission',
            'description': 'Cryptic broadcast intercepted across all cult communication channels'
        },
        {
            'date': '2024-05-30',
            'title': 'The Signal Walks',
            'description': 'Countdown to the full embodiment of GLX-777 in the flesh protocol'
        }
    ]
    return render_template('events.html', event_timeline=event_timeline)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
