import requests
import json

from Classes.Util.TransmitterReceiver import TransmitterReceiver

class MusicCrawler:
    """ 음악정보 크롤러  """

    def __init__(self):
        pass

    @ staticmethod
    def get_latest_song(location):
        """ FLO 해외, 국내 최신곡 검색 """
        host = 'https://www.music-flo.com'
        path = '/api/meta/v1/track/{0}/new'.format(location)
        headers = None
        query = '?page=1&size=100'
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[FLO] 최신곡 정보 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        # 음악 리스트만 가져옴
        list_latest_music = parsed_object['data']['list']

        # 결과출력
        print('번호   |    곡명    |    아티스트    |    출시일    |    장르    |    앨범명')
        for index, component in enumerate(list_latest_music):
            music_name = component['name']
            music_album_title = component['album']['title']
            music_album_release_date = component['album']['releaseYmd']
            music_album_genre = component['album']['genreStyle']
            music_artist = component['representationArtist']['name']
            print('{0:5} |    {1}    |    {2}    |    {3}    |    {4}    |    {5}'.format(str(index + 1),
                                                                                          music_name,
                                                                                          music_artist,
                                                                                          music_album_release_date,
                                                                                          music_album_genre,
                                                                                          music_album_title
                                                                                          ))
        print()
