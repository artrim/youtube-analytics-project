import isodate

from datetime import timedelta

from src.service import Service


class PlayList(Service):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlist_videos = self.get_service().playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title']
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()

    @property
    def total_duration(self):
        total_duration = timedelta(hours=0, minutes=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        like_count = 0
        url = ''
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > like_count:
                like_count = int(video['statistics']['likeCount'])
                url = f"https://youtu.be/{video['id']}"

        return url
