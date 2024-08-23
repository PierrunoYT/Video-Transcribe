import os
import yt_dlp
import openai
from pydub import AudioSegment
from pathlib import Path
import json

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
        'outtmpl': '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        final_filename = filename.rsplit('.', 1)[0] + '.mp3'
    
    # Rename the file to the desired output_path
    os.rename(final_filename, output_path)
    return output_path

def transcribe_audio(audio_chunks):
    full_transcript = ""
    for chunk in audio_chunks:
        with open(chunk, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        full_transcript += transcript["text"] + " "
        os.remove(chunk)  # Remove the chunk after transcription
    return full_transcript.strip()

def text_to_speech(text, output_file="tts_output.mp3"):
    client = openai.OpenAI()
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    output_path = Path(output_file)
    response.stream_to_file(output_path)
    print(f"Text-to-Speech audio saved to {output_file}")

def get_api_key():
    config_file = Path.home() / '.openai_api_key.json'
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('api_key')
    
    api_key = input("Please enter your OpenAI API key: ")
    with open(config_file, 'w') as f:
        json.dump({'api_key': api_key}, f)
    print(f"API key has been saved in {config_file}.")
    return api_key

def main():
    # Get and set OpenAI API key
    openai.api_key = get_api_key()

    # Prompt for YouTube video URL
    url = input("Please enter the YouTube video URL: ")

    # Prompt for transcript output file name
    transcript_output = input("Enter the name for the transcription file (default: transcript.txt): ") or "transcript.txt"

    # Prompt for Text-to-Speech option
    tts_enabled = input("Do you want to enable Text-to-Speech? (y/n): ").lower() == 'y'

    # If TTS is enabled, prompt for TTS output file name
    tts_output = None
    if tts_enabled:
        tts_output = input("Enter the name for the TTS audio file (default: tts_output.mp3): ") or "tts_output.mp3"

    # Download audio
    audio_path = "temp_audio.mp3"
    audio_path = download_audio(url, audio_path)

    # Split audio into chunks
    audio_chunks = split_audio(audio_path)

    # Transcribe audio chunks
    transcript = transcribe_audio(audio_chunks)

    # Save transcript to file
    with open(transcript_output, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcription has been saved to {transcript_output}.")

    # Perform Text-to-Speech if enabled
    if tts_enabled:
        text_to_speech(transcript, tts_output)

    # Clean up temporary audio file
    os.remove(audio_path)

if __name__ == "__main__":
    main()
