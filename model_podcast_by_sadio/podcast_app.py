#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify, redirect, flash, url_for
from podcast_model.podcast_methods import PodcastMethods
from radio_model.radio_methods import RadioMethods



# database part
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from podcast_model.model import Base, Country, Region, Category, Podcast
from music_model.music_model import Genre, Music


from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = '/home/elpastore/ALX-program/portifolio_project/original/Yimbo/model_podcast/static/music'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['SECRET_KEY'] = '80ab528d4604e4d073b613216f6a0822'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Connection to the database
engine = create_engine('mysql+mysqldb://root:elpastore@localhost:3306/podcast_radio_database')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#DBSession = engine.connect()

@app.route('/test')
def test():
    return render_template('base.html')

@app.route('/extend')
def extend():
    return render_template('test_2.html')


@app.route('/add_genre', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'POST':
        new_genre = Genre(name=request.form['genre'])
        session.add(new_genre)
        session.commit()
        flash("Genre added successfully")
        return redirect('/add_genre')
    return render_template('add_genre.html')

def allowed_file(filename):
    """
    method to check if the file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/add_music', methods=['GET', 'POST'])
def handle_music():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files or 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        picture = request.files['picture']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or picture.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check if the file is allowed
        if file and allowed_file(file.filename) and allowed_file(picture.filename):
            music_filename = secure_filename(file.filename)
            picture_filename = secure_filename(picture.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], music_filename))
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
            
            # Add song to database
            new_song = Music(title=request.form['title'], artist_name=request.form['artist'], duration=request.form['duration'], genre_id=request.form['genre_id'],music_file=music_filename, picture=picture_filename)
            session.add(new_song)
            session.commit()
            flash("File Uploaded Successfully")
            return redirect('/add_music')  # Redirect after successful upload

    return render_template('add_music.html')

@app.route('/music')
def music():
    """
    route for the music page display all genre of music
    """
    genres = session.query(Genre).all()
    our_musics = session.query(Music).all()
    return render_template('music_page.html', genres=genres,our_musics=our_musics)

@app.route('/all_music')
def all_music():
    """
    display all music in the database
    """
    our_musics = session.query(Music).all()
    return render_template('music.html', our_musics=our_musics)


@app.route('/player/<int:id>', methods=['GET','POST'])
def player(id):
    """
    display the music player with a specific music
    """
    music = session.query(Music).filter_by(id=id).first()
    musics = session.query(Music).all()
    return render_template('spotify_player.html', music=music, musics=musics)


@app.route('/music_by_genre/<int:genre_id>')
def get_music_by_genre(genre_id):
    """
    display list of music of the specified genre
    """
    # Query all music objects with the specified genre_id
    genre = session.query(Genre).filter(Genre.id==genre_id).first()
    musics = session.query(Music).filter_by(genre_id=genre_id).all()
    return render_template('index_2.html', genre=genre, musics=musics)


podcast_method = PodcastMethods()
radio_method = RadioMethods()


@app.route("/sort_category", methods=["GET", "POST"], strict_slashes=False)
def sort_category():
    """ retrieve the category name and get all podcasts belonging
        to that group
    """ 

    # retrive the request
    group_names = request.args.get("category")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachCategory(group_names)
    pic_names = podcast_method.get_imageFile_name("/home/elpastore/ALX-program/portifolio_project/Yimbo/model_podcast/static/pics") # use the full path of the server
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)
    
    # Render the template and pass the category and table names as context variables
    return render_template("new.html", group_names=group_names,
                           podcast_info=podcast_info)


@app.route("/sort_region", methods=["GET", "POST"], strict_slashes=False)
def sort_region():
    """ retrieve the region name and get all podcasts belonging
        to that group
    """
    group_names = request.args.get("region")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachRegion(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/model_podcast/static/pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    return render_template("new.html",
                           group_names=group_names,
                           podcast_info=podcast_info)


@app.route("/sort_country", methods=["GET", "POST"], strict_slashes=False)
def sort_country():
    """ retrieve the country name and get all podcasts belonging
        to that group
    """
    
    # retrive the request
    group_names = request.args.get("country")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachCountry(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/model_podcast/static/pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    # Render the template and pass the category and table names as context variables
    return render_template("new.html",
                           group_names=group_names,
                           podcast_info=podcast_info,
                           )


@app.route("/user_radio", methods=["GET", "POST"], strict_slashes=False)
def user_radio():
    """This method defins the route to handle all radio streamings"""
    table_names = podcast_method.get_table_name()
    country_names = podcast_method.country_names()
    region_names = podcast_method.region_names()
    return render_template("podcast_page.html",
                               table_names=table_names,
                               country_names=country_names,
                               region_names=region_names)


@app.route("/sort_radioByRegion", methods=["GET", "POST"], strict_slashes=False)
def sort_radioByRegion():
    """ retrieve the region name and get all podcasts belonging
        to that group
    """
    group_names = request.args.get("region")
    table_names = request.args.get("table_names")
    category_info = radio_method.get_radioInEachRegion(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/model_podcast/static/r_pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    radio_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    return render_template("new.html",
                           group_names=group_names,
                           radio_info=radio_info)


@app.route("/sort_RadioByCountry", methods=["GET", "POST"], strict_slashes=False)
def sort_RadioByCountry():
    """ retrieve the country name and get all podcasts belonging
        to that group
    """
    # retrive the request
    group_names = request.args.get("country")
    table_names = request.args.get("table_names")
    category_info = radio_method.get_radioInEachCountry(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/model_podcast/static/r_pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    radio_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    # Render the template and pass the category and table names as context variables
    return render_template("new.html",
                           group_names=group_names,
                           radio_info=radio_info,
                           )


@app.route("/home", methods=["GET", "POST"], strict_slashes=False)
def home():
    """This method defins the route to handle all radio streamings"""
    radio_country= "South Africa"
    podcast_country = "Kenya"
    podcast_kenya = podcast_method.display_sixpodcast(podcast_country)
    radio_sa = radio_method.display_sixradio(radio_country)
    return render_template("landing_page.html", podcast_kenya=podcast_kenya,
                           radio_sa=radio_sa)


@app.route("/", methods=["GET", "POST"], strict_slashes=False)
def podcast():
    category_names = podcast_method.category_names()
    table_names = podcast_method.get_table_name()
    country_names = podcast_method.country_names()
    region_names = podcast_method.region_names()

    return render_template("podcast_page.html",
                           category_names=category_names,
                           table_names=table_names,
                           country_names=country_names,
                           region_names=region_names)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
