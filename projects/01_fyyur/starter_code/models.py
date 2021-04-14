#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)

    # Added missing fields
    # DONE

    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website_link = db.Column(db.String(120), nullable=True)
    looking_for_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=False, default='Please update your talent seeking description here.')
    shows = db.relationship('Show', backref='venue', lazy=True)

    def details(self):
        return{
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website_link,
            'facebook_link': self.facebook_link,
            'looking_for_talent': self.looking_for_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link
        }

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)

    # Added missing fields
    # DONE

    website_link = db.Column(db.String(120), nullable=True)
    looking_for_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=False, default='Please update your venue seeking description here.')

    shows = db.relationship('Show', backref='artist', lazy=True)

    def details(self):
        return{
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state':self.state,
            'phone': self.phone,
            'website': self.website_link,
            'facebook_link': self.facebook_link,
            'looking_for_venue': self.looking_for_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link
        }

# TODO: implement any missing fields, as a database migration using Flask-Migrate
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# DONE

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))

    def details(self):
        return{
        'venue_id': self.venue_id,
        'venue_name': self.venue.name,
        'artist_id': self.artist_id,
        'artist_name': self.artist.name,
        'artist_image': self.artist.image_link,
        'start_time': str(self.start_time)
        }
    def artist_show(self):
        return {
        'artist_id': self.artist_id,
        'artist_name': self.artist.name,
        'artist_image_link': self.artist.image_link,
        'start_time': str(self.start_time)
        }
    def venue_show(self):
        return {
        'venue_id': self.venue_id,
        'venue_name': self.venue.name,
        'venue_image_link': self.venue.image_link,
        'start_time': str(self.start_time)
        }
