import time
from telethon.sync import TelegramClient, events

# Replace the values below with your own API key, API hash, and string session code
api_id = 24639866
api_hash = 'd04ab3fca3e8b8bd2477d8dd1b3e2c97'
session_string = '1BVtsOJIBu7ZVVXLiiHN5w6n0efhnc8EVc6zGyOf2ygYCuTZUrWzS_-AVzH0OBExFKZFXynfLLoR2WbzDKWuNZLo835A6P9Mb-_7398tH_zwdPD0vln8uyRYounP2tBFpqOTQIlypakazCHLhNQ2J5pZBOlPLZP_XBfweiu4GkQCrRXer5aB9UmlZ4uiJRSYnPEaaaFH0Bu9sdznB2PztbU0o9IFq6taMmXpVsTi16gt7vIM1kBi2LcJVHvMlR_tjKdP6LG_MUjV7SBwU3DSEB8y-5g1pIGxM38t8bNyppJ1cBfZIIeiIh_3BDPtnhXF_Xk3UKtI0ocXT8N5lZnqVv4MdyFNaKy0='

client = TelegramClient(session_string, api_id, api_hash)

# Add your messages here
messages = ['Hello everyone', 'Hello everyone \nHello everyone', 'Hello everyone \nHello everyone \nHello everyone']

# Set the time interval between messages (in seconds)
message_interval = 20  # 20 seconds

# Set the time interval for changing profile image and name (in seconds)
profile_interval = 60  # 1 minutes

# Add your profile image and name file paths here
profile_images = ['https://telegra.ph/file/0c3c9cb1028a50724968a.jpg', 'https://telegra.ph/file/6c7285e9fa075393b375b.jpg', 'https://telegra.ph/file/5854d74e7e74213151140.jpg']
profile_names = ['Anjali', 'Pooja', 'Rani']

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
    chat_id = -1001633934133  # Replace with your own group chat ID
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
