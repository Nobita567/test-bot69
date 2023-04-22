import time
from telethon.sync import TelegramClient, events

# Replace the values below with your own API key, API hash, and string session code
api_id = 123456
api_hash = 'abcdef1234567890'
session_string = 'your-session-string-here'

client = TelegramClient(session_string, api_id, api_hash)

# Add your messages here
messages = ['Message 1', 'Message 2', 'Message 3']

# Set the time interval between messages (in seconds)
message_interval = 300  # 5 minutes

# Set the time interval for changing profile image and name (in seconds)
profile_interval = 3600  # 1 hour

# Add your profile image and name file paths here
profile_images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
profile_names = ['Name 1', 'Name 2', 'Name 3']

# Set the initial profile image and name
current_profile_image = profile_images[0]
current_profile_name = profile_names[0]

@client.on(events.NewMessage(chats=client.get_me(), incoming=True))
async def auto_reply(event):
    # Delay the reply by 5 seconds
    time.sleep(5)
    await event.reply('Thanks for your message! I will get back to you shortly.')

async def change_profile():
    # Cycle through the profile images and names
    global current_profile_image, current_profile_name
    current_profile_image = profile_images[(profile_images.index(current_profile_image) + 1) % len(profile_images)]
    current_profile_name = profile_names[(profile_names.index(current_profile_name) + 1) % len(profile_names)]
    await client(UpdateProfileRequest(
        first_name=current_profile_name,
        photo=InputPhoto(file=await client.upload_file(current_profile_image))
    ))

async def send_messages():
    # Cycle through the messages and send them to a specific group
    chat_id = -123456789  # Replace with your own group chat ID
    for message in messages:
        await client.send_message(chat_id, message)
        time.sleep(message_interval)

async def main():
    await client.start()
    # Run the auto-reply function in the background
    client.loop.create_task(auto_reply())
    while True:
        # Change the profile every hour
        await change_profile()
        # Send messages to the group every 5 minutes
        await send_messages()
        time.sleep(profile_interval)

if __name__ == '__main__':
    client.loop.run_until_complete(main())
