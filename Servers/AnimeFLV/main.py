import cfscrape
from flask import request
from flask_restplus import Resource, Namespace, fields, abort
from Servers.AnimeFLV.scraper import getList, scrapeEpisodeList, scrapeEpisode, scrapeGenre, scrapeGenreList, scrapeFeed, scrapeLastAnimeAdded

cfscraper = cfscrape.create_scraper(delay=10)

animeflv_api = Namespace('AnimeFLV', description='AnimeFLV API')

search_model = animeflv_api.model('Search AnimeFLV', {
    'value': fields.String,
    'page': fields.Integer
})
episodes_list_model = animeflv_api.model('Episodes List AnimeFLV', {
    'last_id': fields.Integer,
    'slug': fields.String,
    'page': fields.Integer
})
watch_episode_model = animeflv_api.model('Watch Episode AnimeFLV', {
    'id_episode': fields.Integer,
    'slug': fields.String,
    'no_episode': fields.Integer
})
genre_model = animeflv_api.model('Genre search AnimeFLV', {
    'type': fields.String,
    'page': fields.Integer
})


@animeflv_api.route('/')
class Home(Resource):
    @animeflv_api.doc(description='Index endpoint',
                      responses={200: 'Server is OK'})
    def get(self):
        return {'server': 'AnimeFLV'}


@animeflv_api.route('/search')
class Search(Resource):
    @animeflv_api.expect(search_model)
    @animeflv_api.doc(description='Search for an anime in AnimeFLV',
                      responses={
                          200: 'Request was successful',
                          400: 'Bad request',
                          500: 'Internal server error'
                      },
                      params={
                        'value': 'String to search in AnimeFLV',
                        'page': 'Current page'
                      })
    def post(self):
        params = request.get_json()
        anime_name = params['value'].lower()
        page = params['page']
        if not anime_name or not page:
            abort(400, 'Bad request')
        try:
            anime_list = getList()
            directory = [anime for anime in anime_list if anime_name in anime['title'].lower()]
            page-=1
            length = len(directory)
            start_range = page * 24
            end_range = start_range + 24 if start_range + 24 < length else length
            filtered_anime = [directory[i] for i in range(start_range, end_range)]
            return filtered_anime
        except:
            abort(500, 'Something ocurred while searching the anime')


@animeflv_api.route('/episodes')
class Episodes(Resource):
    @animeflv_api.expect(episodes_list_model)
    @animeflv_api.doc(description='Search an anime episodes list',
                      responses={
                        200: 'Request was successful',
                        400: 'Bad request',
                        500: 'Internal server error'
                      },
                      params={
                        'last_id': 'Anime last Id',
                        'slug': 'Anime name used in AnimeFLV endpoint',
                        'page': 'Current page'
                      })
    def post(self):
        params = request.get_json()
        last_id = params['last_id']
        slug = params['slug']
        page = params['page']
        if not slug or not last_id or not page:
            abort(400, 'Bad request')
        try:
            episodes = scrapeEpisodeList(last_id, slug)
            page-=1
            length = len(episodes)
            start_range = page * 24
            end_range = start_range + 24 if start_range + 24 < length else length
            results = [episodes[i] for i in range(start_range, end_range)]
            return results
        except:
            abort(500, 'Something ocurred while retrieving the episodes list')


@animeflv_api.route('/watch')
class Watch(Resource):
    @animeflv_api.expect(watch_episode_model)
    @animeflv_api.doc(description='Get episode streaming options', 
                      responses={
                          200: 'Request was successful',
                          400: 'Bad request',
                          500: 'Internal server error'
                      }, params={
                          'id_episode': 'Episode id',
                          'slug': 'Anime name used in AnimeFLV endpoint',
                          'no_episode': 'Eposide number'
                      })
    def post(self):
        params = request.get_json()
        id_episode = params['id_episode']
        slug = params['slug']
        no_episode = params['no_episode']
        if not id_episode or not slug or not no_episode:
            abort(400, 'Bad request')
        try:
            return scrapeEpisode(id_episode, slug, no_episode)
        except:
            abort(500, 'Something ocurred while retrieving streaming options')


@animeflv_api.route('/genre')
class Genre(Resource):
    @animeflv_api.expect(genre_model)
    @animeflv_api.doc(description='Get animes related with specific genre', 
                      responses={
                          200: 'Request was successful',
                          400: 'Bad request',
                          500: 'Internal server error'
                      }, params={
                          'type': 'Genre type',
                          'page': 'Current page'
                      })
    def post(self):
        params = request.get_json()
        genre_type = params['type']
        page = params['page']
        if not genre_type or not page:
            abort(400, 'Bad request')
        try:
            return scrapeGenre(genre_type, page)
        except:
            abort(500, 'Something ocurred while retrieving animes')


@animeflv_api.route('/genre/list')
class GenreList(Resource):
    @animeflv_api.doc(description='Get genre list', 
                      responses={
                          200: 'Request was successful',
                          400: 'Bad request',
                          500: 'Internal server error'
                      })
    def get(self):
        try:
            return scrapeGenreList()
        except:
            abort(500, 'Something ocurred while retrieving genre list')


@animeflv_api.route('/feed')
class Feed(Resource):
    @animeflv_api.doc(description='Get today feed', responses={
                          200: 'Request was successful',
                          400: 'Bad request',
                          500: 'Internal server error'
                      })
    def get(self):
        try:
            return scrapeFeed()
        except:
            abort(500, 'Something ocurred while retrieving today feed')


@animeflv_api.route('/last')
class LastAnimeAdded(Resource):
    @animeflv_api.doc(description='Get last anime added', responses={
                          200: 'Request was successful',
                          400: 'Bad request',
                          500: 'Internal server error'
                      })
    def get(self):
        try:
            return scrapeLastAnimeAdded()
        except:
            abort(500, 'Something ocurred while retrieving last anime added')