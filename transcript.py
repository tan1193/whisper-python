import whisper
import yt_dlp
import os
import time  # For performance tracking

def download_audio_from_youtube(youtube_url, output_path="youtube_audio"):
    """Download audio from YouTube video"""
    start_time = time.time()  # Start timer
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': False
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        title = info.get('title', 'youtube_video')
    
    output_file = f"{output_path}.wav"
    
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"Download complete in {elapsed_time:.2f} seconds")
    
    return output_file, title

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def transcribe_audio(audio_file, output_name, model_name="turbo"):
    """Transcribe audio file using Whisper"""
    overall_start_time = time.time()  # Start overall timer
    
    print(f"Loading Whisper model '{model_name}'...")
    model_load_start = time.time()
    model = whisper.load_model(model_name)
    model_load_time = time.time() - model_load_start
    print(f"Whisper model loaded in {model_load_time:.2f} seconds")
    
    transcription_start = time.time()
    print(f"Transcribing {audio_file}...")
    result = model.transcribe(audio_file)
    transcription_time = time.time() - transcription_start
    print(f"Transcription completed in {transcription_time:.2f} seconds")
    
    # Save the result to a text file with timestamps
    output_file = f"{output_name}_transcript.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # Write the full text first
        f.write("--- TRANSCRIPT WITH TIMESTAMPS ---\n\n")
        f.write(f"Full transcript: {result['text']}\n\n")
        f.write("--- SEGMENTS WITH TIMESTAMPS ---\n\n")
        
        # Write each segment with its timestamp
        for segment in result["segments"]:
            start_time_str = format_timestamp(segment["start"])
            end_time_str = format_timestamp(segment["end"])
            text = segment["text"].strip()
            
            f.write(f"[{start_time_str} --> {end_time_str}] {text}\n")
    
    total_time = time.time() - overall_start_time
    print(f"Transcript with timestamps saved to {output_file}")
    print(f"Total processing time: {total_time:.2f} seconds")
    
    # Return a summary of timing information along with the transcript
    timing_info = {
        "model_loading": model_load_time,
        "transcription": transcription_time,
        "total_time": total_time
    }
    
    return result["text"], timing_info

def main():
    overall_start_time = time.time()  # Start overall timer
    
    source_type = input("Enter 'file' for local file or 'youtube' for YouTube link: ").strip().lower()
    
    if source_type == 'file':
        file_name = input("Enter the name of the audio/video file: ")
        output_name = os.path.splitext(file_name)[0]
        
        try:
            result, timing_info = transcribe_audio(file_name, output_name)
        except Exception as e:
            print(f"Error: {str(e)}")
            return
        
    elif source_type == 'youtube':
        youtube_url = input("Enter the YouTube URL: ")
        print("Downloading audio from YouTube...")
        download_start = time.time()
        audio_file, video_title = download_audio_from_youtube(youtube_url)
        download_time = time.time() - download_start
        
        # Clean video title for filename
        output_name = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in video_title)
        output_name = output_name[:50]  # Limit length
        
        result, timing_info = transcribe_audio(audio_file, output_name)
        timing_info["download"] = download_time
        
        # Clean up downloaded file
        try:
            os.remove(audio_file)
            print(f"Removed temporary audio file: {audio_file}")
        except:
            pass
    else:
        print("Invalid source type. Please enter 'file' or 'youtube'.")
        return
    
    total_time = time.time() - overall_start_time
    print("\n--- PERFORMANCE SUMMARY ---")
    print(f"Total execution time: {total_time:.2f} seconds")
    
    # Print detailed timing information
    if source_type == 'youtube':
        print(f"YouTube download: {timing_info['download']:.2f} seconds")

    print(f"Model loading: {timing_info['model_loading']:.2f} seconds")
    print(f"Transcription: {timing_info['transcription']:.2f} seconds")

if __name__ == "__main__":
    main()