import argparse
import os
import yt_dlp
import openai
from pydub import AudioSegment

MAX_CHUNK_SIZE = 25 * 1024 * 1024  # 25 MB in bytes

def split_audio(audio_path, chunk_size=MAX_CHUNK_SIZE):
    audio = AudioSegment.from_mp3(audio_path)
    chunks = []
    duration = len(audio)
    chunk_length = (chunk_size / (audio.frame_rate * audio.sample_width * audio.channels)) * 1000  # in milliseconds

    for i in range(0, duration, int(chunk_length)):
        chunk = audio[i:i + int(chunk_length)]
        chunk_path = f"chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)

    return chunks

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

def transcribe_audio(audio_chunks):
    full_transcript = ""
    for chunk in audio_chunks:
        with open(chunk, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        full_transcript += transcript["text"] + " "
        os.remove(chunk)  # Remove the chunk after transcription
    return full_transcript.strip()

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

    # Split audio into chunks
    audio_chunks = split_audio(audio_path)

    # Transcribe audio chunks
    transcript = transcribe_audio(audio_chunks)

    # Save transcript to file
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcription saved to {args.output}")

    # Clean up temporary audio file
    os.remove(audio_path)

if __name__ == "__main__":
    main()
