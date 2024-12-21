from telethon.sync import TelegramClient
from pydub import AudioSegment
import os


API_ID = os.environ['TELEGRAM_API_ID']
API_HASH = os.environ['TELEGRAM_API_HASH']
CHANNELS = ['musicbox161', 'TidalMusicChannel', 'rock_hires_flac_wav']
MEDIA_DIR = 'media'


def format_wav_path(path, file):
    wav_path = f'{os.path.splitext(file)[0]}.wav'
    return f'{path}/{wav_path.replace(' ', '_')}'


def convert_to_wav(path, file):
    full_path = f'{path}/{file}'
    fmt_path = format_wav_path(path, file)

    # If .flac convert to .wav
    if file.endswith('.flac'):
        audio = AudioSegment.from_file(full_path, format="flac")
        audio.export(fmt_path, format="wav")

        # Delete the original file
        if os.path.exists(full_path):
            os.remove(full_path)


if __name__ == "__main__":
    client = TelegramClient('test_session', api_id=API_ID, api_hash=API_HASH)
    client.start()

    # Create media dir if not exists
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)

    for channel in CHANNELS:
        print(f'Downloading from {channel} channel...')
        export_path = f'{MEDIA_DIR}/{channel}'

        # Create dir if not exists
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        # Iterate over messages in chat
        for message in client.iter_messages(channel):
            # Skip non audio files
            if message.file.ext not in ['.flac', '.wav']:
                continue

            file_name = message.file.name
            format_path = format_wav_path(path=export_path, file=file_name)

            # Download file if not exists yet
            if not os.path.isfile(format_path):
                client.download_media(message=message, file=export_path)
                convert_to_wav(path=export_path, file=file_name)
                print(format_path)
