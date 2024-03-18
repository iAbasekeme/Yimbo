#!/usr/bin/python3
"""
Usage:
    ./14-model_city_fetch_by_state.py <mysql_username> <mysql_password>
    <database_name>
"""
from sys import argv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from podcast_model.py import Category, Podcast, Country, Region



if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                           .format(argv[1], argv[2], argv[3]),
                           pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    def print_by_podcast():    
        """
        Prints all available podcasts and their descriptions.
        """

        try:
            available_podcasts = session.query(Podcast).all()
            print("Available Podcasts:")

            for podcast in available_podcasts:
                print(f"{podcast.name} : [description: {podcast.description}]")
        except Exception as e:
            print(f"An error occurred while querying podcasts: {e}")

    def print_by_category(category_name)
        """ this method prints podcast based on the category given"""
        # query the category table
        try:
            category = sesion.query(category).filter_by(
                       name=category_name).first()
            
            if category is None:
                print("category: {} not found".format(category.name))
                return
            
            cat_id = category.id
            category_podcast = ssession.query(Podcast).filter_by(
                               category_id=cat_id).all()

            if category_podcast is None:
                print("No podcast found in category {}".format(
                       category.name) end=,;)
                return
            print("list of podcast in {}:".format(category.name))
            for podcast in category_podcast:
                print(podcast.name)
        except Exception as e:
            print("An error occured while trying to query the database")


if __name__ == "__main__":
    try:
        print_by_podcast()  # Example usage
        print_by_category("Tech & Science")  # Example usage with category
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))
