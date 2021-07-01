# A video player class #

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random

class VideoPlayer:

    # A class used to represent a Video Player #

    def __init__(self):
        self.playing = [] # [Video1, Video2]
        self.paused = [] # [Video1, Video2]
        self.flagged = {} # {Video : Reason}
        self._video_library = VideoLibrary()
        self.all_videos = self._video_library.get_all_videos()
        self._video_playlist = Playlist()

    def number_of_videos(self) -> None:

        # Returns number of videos.

        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self) -> None:

        # Returns all videos.

        print("Here's a list of all available videos:")
        for _ in sorted(self.all_videos, key=lambda _: _.title, reverse=False): # Sorts in order by title property.
            print(f"{_.title} ({_.video_id}) [{' '.join(_.tags)}] - FLAGGED (reason: {self.flagged[_.video_id]})") if _.video_id in self.flagged.keys() else print(f"{_.title} ({_.video_id}) [{' '.join(_.tags)}]")

    def play_video(self, video_id: str) -> None:
        
        # Plays the respective video. 
        # Args: video_id: The video_id to be played.

        (video_exists, video_title) = self._video_playlist.check_video_exists(video_id)

        if video_id not in self.playing and video_exists is True:
            if video_id in self.flagged.keys():
                print(f"Cannot play video: Video is currently flagged (reason: {self.flagged[video_id]})")
            else:
                if len(self.playing) > 0:
                    self.stop_video()
                    print(f"Playing video: {video_title}")
                    self.playing.append(video_title)
                elif len(self.paused) > 0:
                    self.stop_video()
                    print(f"Playing video: {video_title}")
                    self.playing.append(video_title)
                else:
                    print(f"Playing video: {video_title}")
                    self.playing.append(video_title)
        elif video_id in self.playing:
            self.stop_video(video_title)
        elif video_exists is False:
            print("Cannot play video: Video does not exist")

    def stop_video(self) -> None:

        # Stops the currently playing video, if any.

        if len(self.playing) > 0:
            print(f"Stopping video: {self.playing[0]}")
            self.playing = [] # Empties playing array.
        elif len(self.paused) > 0:
            print(f"Stopping video: {self.paused[0]}")
            self.paused = [] # Empties paused array.
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self) -> None:

        # Plays a random video from the video library.

        unflagged_videos = self.all_videos
        
        for _ in self.all_videos:
            if _.video_id in self.flagged.keys():
                unflagged_videos.remove(_)

        if len(unflagged_videos) == 0:
            print("No videos available")
        else:
            random_choice = random.choice(unflagged_videos)
            self.play_video(random_choice.video_id)

    def pause_video(self) -> None:

        # Pauses the current video.

        if len(self.playing) == 0:
            if len(self.paused) > 0:
                print(f"Video already paused: {self.paused[0]}")
            else:
                print("Cannot pause video: No video is currently playing")
        else:
            print(f"Pausing video: {self.playing[0]}")
            self.paused.append(self.playing[0])
            self.playing = []

    def continue_video(self) -> None:

        # Resumes playing the current video.

        if len(self.paused) == 0:
            if len(self.playing) == 0:
                print("Cannot continue video: No video is currently playing")
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print(f"Continuing video: {self.paused[0]}")
            self.playing.append(self.paused[0])
            self.paused = [] # Empties paused array.

    def show_playing(self):

        # Displays video currently playing.

        if len(self.playing) > 0:
            for _ in self.all_videos:
                if self.playing[0] in _.title:
                    print(f"Currently playing: {_.title} ({_.video_id}) [{' '.join(_.tags)}] ")
        elif len(self.paused) > 0:
            for _ in self.all_videos:
                if self.paused[0] in _.title:
                    print(f"Currently playing: {_.title} ({_.video_id}) [{' '.join(_.tags)}] - PAUSED")
        else:
            print("No video is currrently playing")

    def create_playlist(self, playlist_name: str) -> None:

        # Creates a playlist with a given name.
        # Args: playlist_name: The playlist name.

        self._video_playlist.create_playlist(playlist_name)

    def add_to_playlist(self, playlist_name: str, video_id: str) -> None:

        # Adds a video to a playlist with a given name.
        # Args: playlist_name: The playlist name, video_id: The video_id to be added.
        
        if video_id in self.flagged.keys():
            self._video_playlist.add_to_playlist(playlist_name, video_id, True, self.flagged[video_id])
        else:
            self._video_playlist.add_to_playlist(playlist_name, video_id, False)

    def show_all_playlists(self) -> None:

        # Display all playlists.

        self._video_playlist.show_all_playlists()

    def show_playlist(self, playlist_name: str) -> None:

        # Display all videos in a playlist with a given name.
        # Args: playlist_name: The playlist name.

        self._video_playlist.show_playlist(playlist_name, self.flagged)

    def remove_from_playlist(self, playlist_name: str, video_id: str) -> None:
        
        # Removes a video to a playlist with a given name.
        # Args: playlist_name: The playlist name, video_id: The video_id to be removed.
        
        self._video_playlist.remove_from_playlist(playlist_name, video_id)

    def clear_playlist(self, playlist_name: str) -> None:
        
        # Removes all videos from a playlist with a given name.
        # Args: playlist_name: The playlist name.
        
        self._video_playlist.clear_playlist(playlist_name)

    def delete_playlist(self, playlist_name: str) -> None:

        # Deletes a playlist with a given name.
        # Args: playlist_name: The playlist name.

        self._video_playlist.delete_playlist(playlist_name)

    def search_videos(self, search_term: str) -> None:
        
        # Display all the videos whose titles contain the search_term.
        # Args: search_term: The query to be used in search.
        
        search_results = []
        count_to_id = {}
        count = 1

        for _ in self.all_videos:
            if search_term.lower() in str(_.title).lower():
                if _.video_id in self.flagged.keys():
                    pass
                else:
                    count_to_id[count] = _.video_id
                    search_results.append(f"{count}) {_.title} ({_.video_id}) [{' '.join(_.tags)}]")
                    count += 1
                    pass
            else:
                pass

        if len(search_results) == 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for result in search_results:
                print(result)

            answer = input("Would you like to play any of the above? If yes, specify the number of the video. \nIf your answer is not a valid number, we will assume it's a no.\n")
            try:
                if int(answer) <= count:
                    self.play_video(count_to_id[int(answer)])
            except ValueError:
                print("Nope!")

    def search_videos_tag(self, video_tag: str) -> None:
        
        # Display all videos whose tags contains the provided tag.
        # Args: video_tag: The video tag to be used in search.
        
        search_results = []
        count_to_id = {}
        count = 1

        if video_tag.startswith("#"):
            for _ in self.all_videos:
                if video_tag.lower() in str(_.tags).lower():
                    count_to_id[count] = _.video_id
                    search_results.append(f"{count}) {_.title} ({_.video_id}) [{' '.join(_.tags)}]")
                    count += 1
                    pass
                else:
                    pass
        else:
            pass

        if len(search_results) == 0:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for result in search_results:
                print(result)

            answer = input("Would you like to play any of the above? If yes, specify the number of the video. \nIf your answer is not a valid number, we will assume it's a no.\n")
            try:
                if int(answer) <= count:
                    self.play_video(count_to_id[int(answer)])
            except ValueError:
                print("Nope!")

    def flag_video(self, video_id: str, flag_reason="") -> None:
        
        # Mark a video as flagged.
        # Args: video_id: The video_id to be flagged, flag_reason: Reason for flagging the video.
        
        (video_exists, video_title) = self._video_playlist.check_video_exists(video_id)

        if video_exists is True:
            if video_id in self.flagged.keys():
                print("Cannot flag video: Video is already flagged")
            else:
                if flag_reason == "":
                    if video_title in self.playing or video_title in self.paused:
                        self.stop_video()
                        print(f"Successfully flagged video: {video_title} (reason: Not supplied)")
                    else:
                        self.flagged[video_id] = "Not supplied"
                        print(f"Successfully flagged video: {video_title} (reason: Not supplied)")
                else:
                    self.stop_video()
                    self.flagged[video_id] = flag_reason
                    print(f"Successfully flagged video: {video_title} (reason: {flag_reason})")
        else: 
            print(f"Cannot flag video: Video does not exist")


    def allow_video(self, video_id: str) -> None:

        # Removes a flag from a video.
        # Args: video_id: The video_id to be allowed again.
        
        (video_exists, video_title) = self._video_playlist.check_video_exists(video_id)

        if video_exists is True:
            if video_id in self.flagged.keys():
                del self.flagged[video_id]
                print(f"Successfully removed flag from video: {video_title}")
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")