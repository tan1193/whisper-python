# Whisper Transcription Tool

A Python-based utility for generating accurate audio transcriptions from YouTube videos and local audio/video files using OpenAI's Whisper speech recognition model.

## Features

- Transcribe audio from YouTube videos or local files
- Download audio from YouTube videos using yt-dlp
- Convert non-WAV audio files to compatible format using FFmpeg
- Generate timestamps for each segment of transcription
- Performance tracking and timing information
- Clean output formatting

## Prerequisites

- Python 3.7+
- FFmpeg installed on your system

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/whisper-python.git
cd whisper-python
```
2. Install whisper and yt-dlp:
```bash
pip install git+
pip install yt-dlp
```
3. Install FFmpeg:
   - For Windows, download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH.
   - For macOS, use Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - For Linux, use your package manager:
     ```bash
     sudo apt-get install ffmpeg
     ```

## Usage

```bash 
python transcript.py
```
You will be prompted to enter the URL of a YouTube video or the path to a local audio/video file. The script will handle the rest, including downloading
the audio, converting it if necessary, and generating the transcription.
## Example

```bash
python transcript.py
```
Enter the URL of the YouTube video or the path to the local audio/video file: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
The script will download the audio, convert it if necessary, and generate the transcription with timestamps.
## Output
The output will be saved in a text file named `transcription.txt` in the same directory as the script. The transcription will include timestamps for each segment, making it easy to follow along with the audio.
## Performance Tracking
The script tracks the time taken for each step of the process, including downloading the audio, converting it, and generating the transcription. This information is printed to the console for your reference.