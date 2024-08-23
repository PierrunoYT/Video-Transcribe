# YT2Text: YouTube Transcriber

This tool allows you to transcribe YouTube videos. It uses OpenAI's Whisper model for transcription.

## Features

- Download audio from YouTube videos
- Transcribe audio using OpenAI's Whisper model
- Save transcriptions to a text file
- Secure storage of OpenAI API key

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/yt2text.git
   cd yt2text
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python youtube_transcriber.py
   ```

2. Follow the prompts to:
   - Enter your OpenAI API key (only required on first run)
   - Provide a YouTube video URL
   - Specify the output file name for the transcription

3. The script will download the audio, transcribe it, and save the transcription to a file.

## Notes

- The OpenAI API key is stored securely in your home directory.
- Temporary audio files are automatically cleaned up after processing.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
