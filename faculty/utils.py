# utils.py
import re

def get_youtube_embed_url(url):
    """
    Convert a YouTube URL to its embed format.
    
    Handles various YouTube URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    # YouTube video ID regex patterns
    youtube_regex = (
        r'(?:https?:\/\/)?(?:www\.)?'
        r'(?:youtube\.com\/(?:embed\/|watch\?v=)|youtu\.be\/)'
        r'([a-zA-Z0-9_-]{11})'
    )
    
    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
    
    # Return original URL if not a YouTube URL or if already in embed format
    return url

def is_youtube_url(url):
    """Check if the given URL is a YouTube URL"""
    youtube_regex = (
        r'(?:https?:\/\/)?(?:www\.)?'
        r'(?:youtube\.com\/(?:embed\/|watch\?v=)|youtu\.be\/)'
        r'([a-zA-Z0-9_-]{11})'
    )
    
    match = re.search(youtube_regex, url)
    return bool(match)