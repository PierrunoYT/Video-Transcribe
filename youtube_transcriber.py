import argparse
import os
import yt_dlp
import openai
from pydub import AudioSegment

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

def main():
    parser = argparse.ArgumentParser(description="Transcribe YouTube videos using OpenAI's Whisper model.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--output", default="transcript.txt", help="Output file name (default: transcript.txt)")
    args = parser.parse_args()

    # Set your OpenAI API key
    openai.api_key = "your_openai_api_key_here"

    # Download audio
    audio_path = "temp_audio.mp3"
    download_audio(args.url, audio_path)

    # Transcribe audio
    transcript = transcribe_audio(audio_path)

    # Save transcript to file
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcription saved to {args.output}")

    # Clean up temporary audio file
    os.remove(audio_path)

if __name__ == "__main__":
    main()
