# YouTube Audio Transcription with Whisper

This project provides a Python script that downloads audio from YouTube videos and automatically transcribes the content into text using Whisper, a speech recognition model developed by OpenAI. The transcription process is accompanied by a progress bar for user feedback.

## Features

- Download audio from any YouTube video using `yt-dlp`.
- Transcribe the downloaded audio using Whisper's speech-to-text capabilities.
- Automatically format the transcription with line breaks after each sentence.
- Track the transcription progress with a progress bar.

## Prerequisites

Before using this project, ensure that you have:

- Python 3.x installed on your machine.
- The necessary dependencies installed by running:
  ```bash
  pip install -r requirements.txt
  ```
  Dependencies include:
  - `yt-dlp` for downloading YouTube videos.
  - `whisper` for audio transcription.
  - `tqdm` for displaying the progress bar.

- `ffmpeg` installed and available in your system's PATH. You can download it [here](https://ffmpeg.org/download.html).

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Sithey/Youtube-Transcription.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Youtube-Transcription
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `ffmpeg` is installed and properly configured in your system's PATH. You can follow [this guide](https://ffmpeg.org/download.html) to install it.

## Usage

1. Run the script and enter the URL of the YouTube video you wish to transcribe:
   ```bash
   python main.py
   ```

2. When prompted, enter the YouTube video URL:
   ```bash
   Enter the YouTube video URL: https://www.youtube.com/watch?v=example
   ```

3. The script will download the audio, transcribe it, and save the transcription in a `.txt` file in a folder named after the video ID.

## Example

```bash
python main.py
Enter the YouTube video URL: https://www.youtube.com/watch?v=ah4tVdktIeE
```

This will download the audio, transcribe it, and save the text in a folder called `ah4tVdktIeE` as `transcription.txt`.

## Project Structure

```
/your-repo-name
  ├── main.py                 # The main script for downloading and transcribing
  ├── requirements.txt         # List of dependencies
  ├── README.md                # Project documentation
  └── <video-id>/              # Folder containing audio and transcription files for each video
        ├── audio.mp3          # Downloaded audio file
        └── transcription.txt  # Transcribed text file
```

## License

This project is licensed under the [MIT License](LICENSE).
