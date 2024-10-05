from openai import OpenAI
import os
import uuid
from datetime import datetime
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals

SAMPLE_TEXT = """Text of voiceover here."""

if __name__ == "__main__":
    # Create the outputs directory if it doesn't exist
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Create a timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir)

    # Generate a unique ID
    unique_id = str(uuid.uuid4())[:8]

    # Define file paths with unique IDs
    audio_file_name = os.path.join(output_dir, f"audio_tts_{unique_id}.wav")
    video_file_name = os.path.join(output_dir, f"rendered_video_{unique_id}.mp4")
    script_file_name = os.path.join(output_dir, f"script_{unique_id}.txt")

    # Save the script to a file
    with open(script_file_name, "w") as script_file:
        script_file.write(SAMPLE_TEXT)
    VIDEO_SERVER = "pexel"

    response = SAMPLE_TEXT
    print("script: {}".format(response))

    asyncio.run(generate_audio(response, audio_file_name))

    timed_captions = generate_timed_captions(audio_file_name)
    print(timed_captions)

    search_terms = getVideoSearchQueriesTimed(response, timed_captions)
    print(search_terms)

    background_video_urls = None
    if search_terms is not None:
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
        print(background_video_urls)
    else:
        print("No background video")

    background_video_urls = merge_empty_intervals(background_video_urls)

    if background_video_urls is not None:
        video = get_output_media(audio_file_name, timed_captions, background_video_urls, VIDEO_SERVER, video_file_name)
        print(video)
    else:
        print("No video")
