import os
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled, NoTranscriptAvailable, VideoUnavailable

# Replace 'YOUR_API_KEY' with your actual API key.
API_KEY = "AIzaSyCon_Gl3HLa5x1wskM3u0GdK75sgwrvGSo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_top_videos(genre, max_results=500):
    """
    Get top YouTube videos for a given genre.

    :param genre: The search term for the genre.
    :param max_results: Total number of videos to fetch.
    :return: List of video details.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    video_details = []
    next_page_token = None

    while len(video_details) < max_results:
        try:
            search_response = youtube.search().list(
                q=genre,
                part="id,snippet",
                type="video",
                maxResults=min(50, max_results - len(video_details)),  # YouTube API limit for one request
                pageToken=next_page_token
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response['items']]

            video_response = youtube.videos().list(
                id=",".join(video_ids),
                part="snippet,statistics,contentDetails,recordingDetails"
            ).execute()

            for item in video_response['items']:
                video_data = {
                    "Video URL": f"https://www.youtube.com/watch?v={item['id']}",
                    "Title": item['snippet']['title'],
                    "Description": item['snippet'].get('description', ''),
                    "Channel Title": item['snippet']['channelTitle'],
                    "Keyword Tags": ", ".join(item['snippet'].get('tags', [])),
                    "YouTube Video Category": item['snippet']['categoryId'],
                    "Topic Details": ", ".join(item.get('topicDetails', {}).get('topicCategories', [])),
                    "Video Published At": item['snippet']['publishedAt'],
                    "Video Duration": item['contentDetails']['duration'],
                    "View Count": item['statistics'].get('viewCount', '0'),
                    "Comment Count": item['statistics'].get('commentCount', '0'),
                    "Captions Available": "true" if item['contentDetails'].get('caption') == 'true' else "false",
                    "Location": item.get('recordingDetails', {}).get('locationDescription', ''),
                }

                # Check and fetch captions
                if video_data["Captions Available"] == "true":
                    video_id = item['id']
                    captions = get_video_captions(video_id)
                    video_data["Caption Text"] = captions
                else:
                    video_data["Caption Text"] = ""

                video_details.append(video_data)

            next_page_token = search_response.get('nextPageToken')

            if not next_page_token:
                break

        except HttpError as e:
            print(f"An error occurred with the YouTube API: {e}")
            break

    return video_details


def get_video_captions(video_id):
    """
    Fetch captions for a YouTube video using YouTubeTranscriptApi.

    :param video_id: The ID of the video.
    :return: Captions text or an appropriate message.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        captions = " ".join([entry['text'] for entry in transcript])
        return captions
    except NoTranscriptFound:
        print(f"No transcript found for video ID: {video_id}.")
        return "No captions available."
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video ID: {video_id}.")
        return "No captions available."
    except NoTranscriptAvailable:
        print(f"No transcripts are available for video ID: {video_id}.")
        return "No captions available."
    except VideoUnavailable:
        print(f"Video is unavailable for video ID: {video_id}.")
        return "No captions available."
    except Exception as e:
        print(f"An unexpected error occurred while fetching captions for video ID {video_id}: {e}")
        return "No captions available."


def save_to_csv(data, filename="youtube_videos.csv"):
    """
    Save the video details to a CSV file.

    :param data: List of video details.
    :param filename: Name of the CSV file.
    """
    if not data:
        print("No data to save.")
        return

    headers = list(data[0].keys())

    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {filename}")


def main():
    genre = input("Enter a genre or search term: ")
    print(f"Fetching top videos for genre: {genre}")

    video_data = get_top_videos(genre)
    save_to_csv(video_data)


if __name__ == "__main__":
    main()
