import requests
import json


class MusicCrawler:
    """ 음악정보 크롤러  """

    def __init__(self):
        pass

    @ staticmethod
    def get_latest_song(location):
        """ FLO 해외, 국내 최신곡 검색 """
        # url생성
        url = 'https://www.music-flo.com/api/meta/v1/track/{0}/new?page=1&size=100'.format(location)

        try:
            # 요청보내고 응답 저장
            res = requests.get(url)
            # 응답의 텍스트
            res_text = res.text
            # 응답의 텍스트를 json형태로 파싱
            parsed_object = json.loads(res_text)
            # 위 두줄을 아래와 같이 사용해도 됨
            # parsed_object = res.json()
        except Exception as e:
            raise RuntimeError('FLO MUSIC 으로부터 정보를 가져오는 데에 실패했습니다.')

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
