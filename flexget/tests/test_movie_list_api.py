from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

from flexget.utils import json

from flexget.api import empty_response
from flexget.plugins.api.movie_list import ObjectsContainer as OC


class TestMovieListAPI(object):
    config = 'tasks: {}'

    def test_movie_list_list(self, api_client, schema_match):
        # No params
        rsp = api_client.get('/movie_list/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.return_lists, data)
        assert not errors

        assert data['movie_lists'] == []

        # Named param
        rsp = api_client.get('/movie_list/?name=name')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.return_lists, data)
        assert not errors

        payload = {'name': 'test'}

        # Create list
        rsp = api_client.json_post('/movie_list/', data=json.dumps(payload))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.list_object, data)
        assert not errors

        values = {
            'name': 'test',
            'id': 1
        }
        for field, value in values.items():
            assert data.get(field) == value

        rsp = api_client.get('/movie_list/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.return_lists, data)
        assert not errors

        for field, value in values.items():
            assert data['movie_lists'][0].get(field) == value

    def test_movie_list_list_id(self, api_client, schema_match):
        payload = {'name': 'test'}

        # Create list
        rsp = api_client.json_post('/movie_list/', data=json.dumps(payload))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.list_object, data)
        assert not errors

        values = {
            'name': 'test',
            'id': 1
        }
        for field, value in values.items():
            assert data.get(field) == value

        # Get list
        rsp = api_client.get('/movie_list/1/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.list_object, data)
        assert not errors

        values = {
            'name': 'test',
            'id': 1
        }
        for field, value in values.items():
            assert data.get(field) == value

        # Delete list
        rsp = api_client.delete('/movie_list/1/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(empty_response, data)
        assert not errors

    def test_movie_list_movies(self, api_client, schema_match):
        payload = {'name': 'name'}

        # Create list
        rsp = api_client.json_post('/movie_list/', data=json.dumps(payload))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code

        movie_data = {'movie_name': 'title'}

        # Add movie to list
        rsp = api_client.json_post('/movie_list/1/movies/', data=json.dumps(movie_data))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.movie_list_object, data)
        assert not errors

        # Get movies from list
        rsp = api_client.get('/movie_list/1/movies/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

    def test_movie_list_movies_with_identifiers(self, api_client, schema_match):
        payload = {'name': 'name'}

        # Create list
        rsp = api_client.json_post('/movie_list/', data=json.dumps(payload))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code

        identifier = {'imdb_id': 'tt1234567'}
        movie_data = {'movie_name': 'title',
                      'movie_identifiers': [identifier]}

        # Add movie to list
        rsp = api_client.json_post('/movie_list/1/movies/', data=json.dumps(movie_data))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.movie_list_object, data)
        assert not errors

        # Get movies from list
        rsp = api_client.get('/movie_list/1/movies/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code
        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.return_movies, data)
        assert not errors

        returned_identifier = data['movies'][0]['movies_list_ids'][0]
        assert returned_identifier['id_name'], returned_identifier['id_value'] == identifier.items()[0]

    def test_movie_list_movie(self, api_client, schema_match):
        payload = {'name': 'name'}

        # Create list
        rsp = api_client.json_post('/movie_list/', data=json.dumps(payload))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code

        identifier = {'imdb_id': 'tt1234567'}
        movie_data = {'movie_name': 'title',
                      'movie_identifiers': [identifier]}

        # Add movie to list
        rsp = api_client.json_post('/movie_list/1/movies/', data=json.dumps(movie_data))
        assert rsp.status_code == 201, 'Response code is %s' % rsp.status_code

        # Get specific movie from list
        rsp = api_client.get('/movie_list/1/movies/1/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.movie_list_object, data)
        assert not errors

        returned_identifier = data['movies_list_ids'][0]
        assert returned_identifier['id_name'], returned_identifier['id_value'] == identifier.items()[0]

        identifiers = [{'trakt_movie_id': '12345'}]

        # Change specific movie from list
        rsp = api_client.json_put('/movie_list/1/movies/1/', data=json.dumps(identifiers))
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.movie_list_object, data)
        assert not errors

        returned_identifier = data['movies_list_ids'][0]
        assert returned_identifier['id_name'], returned_identifier['id_value'] == identifiers[0].items()

        # Delete specific movie from list
        rsp = api_client.delete('/movie_list/1/movies/1/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(empty_response, data)
        assert not errors

        # Get non existent movie from list
        rsp = api_client.get('/movie_list/1/movies/1/')
        assert rsp.status_code == 404, 'Response code is %s' % rsp.status_code

        # Delete non existent movie from list
        rsp = api_client.delete('/movie_list/1/movies/1/')
        assert rsp.status_code == 404, 'Response code is %s' % rsp.status_code
