from youtube_transcript_api import YouTubeTranscriptApi

def extract_captions(video_url):
    try:
        video_id = video_url.split("v=")[1]
        captions = YouTubeTranscriptApi.get_transcript(video_id)
        with open('script.txt', 'w+') as fle:
            for caption in captions:
                start_time = caption['start']
                text = caption['text']
                # print(f"{start_time}: {text}")
                fle.write(f"{start_time}: {text}\n")
            

    except Exception as e:
        print(f"Error: {e}")


if __name__=='__main__':
    # Example usage with a YouTube video URL
    video_url = "https://www.youtube.com/watch?v=cMJWC-csdK4"
    extract_captions(video_url)
