import os
import telebot
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual token
bot = telebot.TeleBot('6189969696:AAHPywUm9GNur1b7jYCFjUueWlKyGd14iLc')

# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    """Send a welcome message when the /start command is issued."""
    bot.reply_to(message, 'Hi! I can download and compress video files for you. Just send me any video file in MP4 or MKV format and I will compress it for you.')

# Define a handler for file downloads
@bot.message_handler(content_types=['document'])
def download_file(message):
    """Download and compress a video file sent by the user."""
    chat_id = message.chat.id
    file_name = message.document.file_name
    file_type = file_name.split('.')[-1]
    allowed_types = ['mp4', 'mkv'] # Only allow MP4 and MKV files
    if file_type not in allowed_types:
        bot.reply_to(message, 'Sorry, I can only compress MP4 and MKV files.')
    else:
        # Download the file
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, 'downloads', str(chat_id), file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)

        # Compress the file
        compressed_file_name = file_name.split('.')[0] + '_compressed.mp4'
        compressed_file_path = os.path.join(base_path, 'downloads', str(chat_id), compressed_file_name)
        cmd = f'ffmpeg -i "{file_path}" -vcodec libx264 -crf 28 "{compressed_file_path}"'
        os.system(cmd)

        # Send the compressed file back to the user
        with open(compressed_file_path, 'rb') as f:
            bot.send_document(chat_id, f, caption=f'Compressed file: {compressed_file_name}')

        # Cleanup
        os.remove(file_path)
        os.remove(compressed_file_path)

        bot.reply_to(message, 'File compression complete.')

# Start the bot
bot.run(host='0.0.0.0', port=80)
