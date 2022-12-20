from django.db import connection


def search_tracks(search='', page=1):
    offset = (page - 1) * 10
    limit = 10
    query = f'''
    SELECT uri FROM
    ((SELECT t.uri, t.popularity FROM
    (SELECT name, uri, popularity FROM backend_api_track WHERE name LIKE "{search}%") t,
    (SELECT track_id, artist_id FROM backend_api_track_artists) ta
    WHERE ta.track_id = t.uri)
    UNION ALL
    (SELECT ta.track_id, t.popularity FROM
    (SELECT name, uri FROM backend_api_artist WHERE name LIKE "{search}%") a,
    backend_api_track t,
    (SELECT track_id, artist_id FROM backend_api_track_artists) ta
    WHERE ta.artist_id = a.uri AND t.uri = ta.track_id)) t
    ORDER BY popularity DESC LIMIT {limit} OFFSET {offset};
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        similar_URIs = cursor.fetchall()
    
    return [x[0] for x in similar_URIs]