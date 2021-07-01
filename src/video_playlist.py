# A video playlist class #

from .video_library import VideoLibrary

class Playlist:

    # A class used to represent a Playlist # 

    def __init__(self):
        self.playlists = {} # {Playlist : [Video1, Video2]}
        self.playlist_names = [] # [Playlist1, Playlist2]
        self._video_library = VideoLibrary()
        self.all_videos = self._video_library.get_all_videos()

    def check_video_exists(self, video_id: str) -> tuple:

        # Validates the existence of a video.
        # Args: video_id: The video_id to be validated.

        video_exists = True
        video_title = ''
        for _ in self.all_videos:
            if video_id in _.video_id:
                video_title = _.title
                video_exists = True
                break
            else:
                video_exists = False
                pass
        return (video_exists, video_title)

    def create_playlist(self, playlist_name: str) -> None:

        # Creates a playlist.
        # Args: playlist_name: The playlist to be created.

        if playlist_name.lower() in ({k.lower(): k for k, v in self.playlists.items()}):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists[playlist_name] = []
            print(f"Successfully created new playlist: {playlist_name}")
            
    def add_to_playlist(self, playlist_name: str, video_id: str, flagged: bool, reason=None) -> None:

        # Adds a video to an existing playlist.
        # Args: playlist_name: The playlist to be added to, video_id: The video to be added, 
        #       flagged: A boolean to identify if the video is flagged, reason: The reasoning for flagging, if applicable.

        if str(playlist_name).lower() not in ({k.lower(): k for k, v in self.playlists.items()}):
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            answer = input(f"Would you like to create a playlist with the name {playlist_name}? ")
            if answer.lower() == "y":
                self.create_playlist(playlist_name)
            else:
                pass
        else:
            (video_exists, video_title) = self.check_video_exists(video_id)
            if video_exists is True:
                if flagged is True:
                    print(f"Cannot add video to playlist: Video is currently flagged (reason: {reason})")
                else:
                    if video_id in self.playlists[playlist_name]:
                        print(f"Cannot add video to {playlist_name}: Video already added")
                    else:
                        self.playlists[playlist_name].append(video_id)
                        print(f"Added video to {playlist_name}: {video_title}")
            else:
                 print(f"Cannot add video to {playlist_name}: Video does not exist")

    def show_all_playlists(self) -> None:

        # Shows all existing playlists, if any.

        if len(self.playlists.keys()) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for _ in self.playlists.keys():#
                if len(self.playlists[_]) == 0 or len(self.playlists[_]) > 1:
                    print(f"{_} ({len(self.playlists[_])} items)")
                else:
                    print(f"{_} ({len(self.playlists[_])} item)")

    def show_playlist(self, playlist: str, flagged: dict) -> None:

        # Validates the existence of a video.
        # Args: video_id: The video_id to be validated.

        if str(playlist).lower() not in ({k.lower(): k for k, v in self.playlists.items()}):
            print(f"Cannot show playlist {playlist}: Playlist does not exist")
            answer = input(f"Would you like to create a playlist with the name {playlist}? ")
            if answer.lower() == "y":
                self.create_playlist(playlist)
            else:
                pass
        else:
            print(f"Showing playlist: {playlist}")
            if len(self.playlists[playlist]) == 0:
                print(" No videos here yet")
            else:
                for video_id in self.playlists[playlist]:
                    for _ in self.all_videos:
                        if video_id in _.video_id:
                            if video_id in flagged.keys():
                                print(f" {_.title} ({_.video_id}) [{' '.join(_.tags)}] - FLAGGED (reason: {flagged[video_id]})")
                            else:
                                print(f" {_.title} ({_.video_id}) [{' '.join(_.tags)}]")

    def remove_from_playlist(self, playlist_name: str, video_id: str) -> None:

        # Removes a video from a selected playlist.
        # Args: playlist_name: The playlist to remove video from, video_id: The video_id to be removed.

        if str(playlist_name).lower() not in ({k.lower(): k for k, v in self.playlists.items()}):
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            answer = input(f"Would you like to create a playlist with the name {playlist_name}? ")
            if answer.lower() == "y":
                self.create_playlist(playlist_name)
            else:
                pass
        else:
            (video_exists, video_title) = self.check_video_exists(video_id) 
            if video_exists is True:
                if video_id in self.playlists[playlist_name]:
                    self.playlists[playlist_name].remove(video_id)
                    print(f"Removed video from {playlist_name}: {video_title}")
                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                 print(f"Cannot remove video from {playlist_name}: Video does not exist")

    def clear_playlist(self, playlist_name: str) -> None:

        # Clears a playlist of all its videos.
        # Args: playlist_name: The playlist to be cleared.

        if str(playlist_name).lower() not in ({k.lower(): k for k, v in self.playlists.items()}):
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            answer = input(f"Would you like to create a playlist with the name {playlist_name}? ")
            if answer.lower() == "y":
                self.create_playlist(playlist_name)
            else:
                pass
        else:
            self.playlists[playlist_name] = [] # Empties video array stored in playlist key
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name: str) -> None:

        # Removes a playlist.
        # Args: playlist_name: The playlist to be removed. 

        if str(playlist_name).lower() not in ({k.lower(): k for k, v in self.playlists.items()}):
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            answer = input(f"Would you like to create a playlist with the name {playlist_name}? ")
            if answer.lower() == "y":
                self.create_playlist(playlist_name)
            else:
                pass
        else:
            del self.playlists[playlist_name]
            print(f"Deleted playlist: {playlist_name}")