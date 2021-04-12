#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from forms import *
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
# DONE - see config info in config.py file


migrate = Migrate(app, db)

db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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
            'image_link': self.image_link,

        }

# TODO: implement any missing fields, as a database migration using Flask-Migrate
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
      date = dateutil.parser.parse(value)
  else:
      date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  venues = Venue.query.order_by('city').all()
  venue_state_and_city = ''
  data = []

  #loop through venues to check for upcoming shows, city, states and venue information

  for venue in venues:
  # filter upcoming shows given that the show start time is greater than the current time
  # print(venue)
    upcoming_shows = Show.query.filter(Show.start_time > current_time, Show.venue_id == venue.id).all()
    if venue_state_and_city == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name":venue.name,
        "num_upcoming_shows": len(upcoming_shows) # a count of the number of shows
      })
    else:
      venue_state_and_city = venue.city + venue.state

      data.append({
        "city":venue.city,
        "state":venue.state,
        "venues": [{
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows": len(upcoming_shows)
        }]
      })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "Hop" should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term=request.form.get('search_term', '')
  current_time = datetime.utcnow()
  venues = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  response={
    "count": len(venues),
    "data":[]
  }
  for venue in venues:
    response['data'].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(Venue.query.join(Show).filter(venue.id == Show.venue_id,Show.start_time > current_time).all()),
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  current_time = datetime.utcnow()
  venue_query = Venue.query.filter_by(id=venue_id).all()
  data = list(map(Venue.details, venue_query))[0]
  past_shows = Show.query.join(Venue).join(Artist).filter(venue_id == Show.venue_id,Show.start_time <= current_time).all()
  upcoming_shows = Show.query.join(Venue).join(Artist).filter(venue_id == Show.venue_id,Show.start_time > current_time).all()
  data['past_shows'] = list(map(Show.artist_show, past_shows))
  data['upcoming_shows'] = list(map(Show.artist_show, upcoming_shows))
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  print(data)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  #flash(form.errors)
  #flash(request.form['seeking_talent'])
  # if request.method == "POST" and form.validate():

  try:
    new_venue = Venue(
        name=request.form.get('name'),
        address=request.form.get('address'),
        city=request.form.get('city'),
        state=request.form.get('state'),
        phone=request.form.get('phone'),
        genres=request.form.getlist('genres'),
        image_link=request.form.get('image_link'),
        facebook_link=request.form.get('facebook_link'),
        seeking_description=request.form.get('seeking_description'),
        looking_for_talent=request.form.get('looking_for_talent') == 'True',
        website_link=request.form.get('website_link')
    )
    #Venue.insert(new_venue)
    db.session.add(new_venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as error:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    #see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash(error)
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue with id' + venue_id + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue with id' + venue_id + ' could not be deleted.')
  finally:
    db.session.close()
    #return jsonify({ 'success': True })

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # DONE

  data = Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term=request.form.get('search_term', '')
  current_time = datetime.utcnow()
  artists = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  response={
      "count": len(artists),
      "data":[]
    }
  for artist in artists:
    response['data'].append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": len(Artist.query.join(Show).filter(artist.id == Show.artist_id, Show.start_time > current_time).all())
    })
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  current_time = datetime.utcnow()
  artist_query = Artist.query.filter_by(id=artist_id).all()
  data = list(map(Artist.details, artist_query))[0]
  past_shows = Show.query.join(Venue).join(Artist).filter(artist_id == Show.artist_id,Show.start_time <= current_time).all()
  upcoming_shows = Show.query.join(Venue).join(Artist).filter(artist_id == Show.artist_id,Show.start_time > current_time).all()
  data['past_shows'] = list(map(Show.venue_show, past_shows))
  data['upcoming_shows'] = list(map(Show.venue_show, upcoming_shows))
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  ----------------------------------------------------------------
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.filter_by(id=artist_id).all()[0]

  form = ArtistForm(
    name=artist.name,
    city=artist.city,
    state=artist.state,
    genres=artist.genres,
    phone=artist.phone,
    facebook_link=artist.facebook_link,
    website_link=artist.website_link,
    image_link=artist.image_link,
    looking_for_venue=artist.looking_for_venue,
    seeking_description=artist.seeking_description
  )

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    artist = Artist.query.filter_by(id=artist_id).all()[0]

    artist.name=request.form.get('name')
    artist.city=request.form.get('city')
    artist.state=request.form.get('state')
    artist.phone=request.form.get('phone')
    artist.genres=request.form.getlist('genres')
    artist.facebook_link=request.form.get('facebook_link')
    artist.website_link=request.form.get('website_link')
    artist.image_link=request.form.get('image_link')
    artist.looking_for_venue=request.form.get('looking_for_venue') == 'True'
    artist.seeking_description=request.form.get('seeking_description')

    db.session.commit()
  except:
    db.session.rollback()
    flash('An error occurred. Artist could not be updated')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  venue = Venue.query.filter_by(id=venue_id).all()[0]

  form = VenueForm(
    name=venue.name,
    city=venue.city,
    state=venue.state,
    address=venue.address,
    phone=venue.phone,
    genres=venue.genres,
    facebook_link=venue.facebook_link,
    website_link=venue.website_link,
    image_link=venue.image_link,
    looking_for_talent=venue.looking_for_talent,
    seeking_description=venue.seeking_description
  )

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  try:
    venue = Venue.query.filter_by(id=venue_id).all()[0]

    venue.name=request.form.get('name')
    venue.city=request.form.get('city')
    venue.state=request.form.get('state')
    venue.address=request.form.get('address')
    venue.phone=request.form.get('phone')
    venue.genres=request.form.getlist('genres')
    venue.facebook_link=request.form.get('facebook_link')
    venue.website_link=request.form.get('website_link')
    venue.image_link=request.form.get('image_link')
    if request.form.get('looking_for_talent.checked'):
        venue.looking_for_talent = 'True'
    else:
        venue.looking_for_talent = 'False'

#    venue.looking_for_talent=request.form.get('looking_for_talent') == 'True'
    venue.seeking_description=request.form.get('seeking_description')

    print (venue)
    db.session.commit()
  except:
    db.session.rollback()
    flash('An error occurred. Venue could not be updated')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success

  error = False

  try:
    new_artist = Artist(
      name=request.form.get('name'),
      city=request.form.get('city'),
      state=request.form.get('state'),
      phone=request.form.get('phone'),
      genres=request.form.getlist('genres'),
      facebook_link=request.form.get('facebook_link'),
      image_link=request.form.get('image_link'),
      website_link=request.form.get('website_link'),
      looking_for_venue=request.form.get('looking_for_venue') == 'True',
      seeking_description=request.form.get('seeking_description')
    )

    db.session.add(new_artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()

  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  shows = Show.query.order_by(db.desc(Show.start_time))

  data = []

  for show in shows:
    data.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm(request.form)
  flash(form.errors)
  if form.validate():
    try:
      new_show = Show(
                start_time=form.start_time.data,
                venue_id=form.venue_id.data,
                artist_id=form.artist_id.data
            )
      db.session.add(new_show)
      db.session.commit()

      # on successful db insert, flash success
      flash('Show was successfully listed!')

    except Exception as error:
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. The show could not be listed.')
      db.session.rollback()
      flash(error)

    finally:
      db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
