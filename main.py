import datetime
from pytube import YouTube
import ast

# Temps for testing
LINK = "https://wwyoutube.com/watch?v=X40Tr3Q-BvE"
yt = YouTube(LINK)

# Description function
def description(yt_link) -> str:
    desc = (f"Title: {yt_link.title}"
            f"\nViews: {yt_link.views}"
            f"\nLength: {datetime.timedelta(seconds=yt_link.length)}")
    return desc


# Function to create dictionary list from fetched streams list
def extract_streams(streams, stream_type) -> list:
    extracted_data = streams.strip("[]").replace('<Stream: ', '{"').replace(">", "}").split(", ")
    list_of_streams = []
    for stream in extracted_data:
        dict_stream = ast.literal_eval(stream.replace(' ', ', "').replace('=', '":'))
        list_of_streams.append(dict_stream)
        audio_list = []
        video_list = []
    for stream in list_of_streams:
        if stream['type'] == 'video':
            video_list.append(
                f"Quality: {stream['res']}, Media Type: {stream['mime_type']}, Tag: {stream['itag']}")
        else:
            audio_list.append(f"Quality: {stream['abr']},Media Type: {stream['mime_type']}, Tag: {stream['itag']}")
    if stream_type == "audio":
        return audio_list
    if stream_type == "video":
        return video_list


# Fetch audio streams
def fetch_audio_streams(yt_link) -> list:
    fetched_streams = str(yt_link.streams.filter(only_audio=True))
    audio_list = extract_streams(fetched_streams, "audio")
    return audio_list


# Fetch video streams
def fetch_video_streams(yt_link) -> list:
    fetched_streams = str(yt_link.streams.filter(progressive=True))
    video_list = extract_streams(fetched_streams, "video")
    return video_list


# Download function
def download_stream(tag, yt_link):
    yt_stream = yt_link.streams.get_by_itag(tag)
    print("Downloading...")
    yt_stream.download()
    print("Download Complete")


def main():
    description(yt)
    # choice = input("Select the format you want to download:\n1.Audio\n2.Video")
    return

