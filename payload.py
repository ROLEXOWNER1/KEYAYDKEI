from datetime import datetime, timedelta
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import random
import string
import re
import time
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from .env
TOKEN = os.getenv('TELEGRAM_TOKEN')  # Replace with environment variable or .env file
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS').split(',')))  # Admin ID(s) from .env
USER_FILE = "users.json"
KEY_FILE = "keys.json"
CHANNELS = [
    "freerareddos",  # Public channel username
    "RARExLEAKS",    # Public channel username
    "RARECRACKS"     # Public channel username
]

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Helper function to generate inline keyboard with join buttons for all channels and "Joined" button
def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup()

    # Add a button for each group (direct URLs)
    for channel in CHANNELS:
        button = InlineKeyboardButton(f"Jᴏɪɴ 🟢", url=f"https://t.me/{channel}")
        keyboard.add(button)

    # "Joined" button to check if user is already a member of all groups
    button_check = InlineKeyboardButton("Jᴏɪɴᴇᴅ 🟢", callback_data="check_joined")
    keyboard.add(button_check)

    return keyboard

# Load data (users and keys) from JSON files
def load_data():
    users, keys = {}, {}
    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as f:
                users = json.load(f)
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, 'r') as f:
                keys = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
    return users, keys

# Save data to JSON files
def save_data(users, keys):
    try:
        with open(USER_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        with open(KEY_FILE, 'w') as f:
            json.dump(keys, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# Function to check membership using get_chat_member API
def check_membership(user_id):
    try:
        for channel in CHANNELS:
            # Check membership for each channel (prefix with @)
            member_status = bot.get_chat_member(f"@{channel}", user_id).status
            if member_status not in ["member", "administrator", "creator"]:
                return False  # User is not a member of the group
        return True  # User is a member of all groups
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False  # Return False if there is an error

# Function to generate payload (payload1 style)
def generate_payload1(size_kb):
    size_bytes = size_kb * 1024
    payload = []

    for _ in range(size_bytes):
        if random.choice([True, False]):
            payload.append(random.getrandbits(8))  # Append random byte
        else:
            payload.append(ord('"'))  # Add a double quote

    # Convert payload bytes to hex representation
    hex_payload = ''.join(f'\\\\x{byte:02x}' for byte in payload)

    # Split into eighths
    eighth_length = len(hex_payload) // 8
    lines = [hex_payload[i:i + eighth_length] for i in range(0, len(hex_payload), eighth_length)]

    # Create formatted output
    formatted_output = '\n'.join(f'"{line}"' for line in lines)

    return formatted_output

# Function to generate payload (payload2 style with 0x prefix)
def generate_payload2(size_kb):
    size_bytes = size_kb * 1024
    payload = []

    for _ in range(size_bytes):
        byte = random.getrandbits(8)  # Generate a random byte
        payload.append(f'0x{byte:02x}')  # Format the byte with 0x prefix

    # Join the payload bytes into a string and add curly braces at the start and end
    formatted_payload = '{' + ', '.join(payload) + '}'

    return formatted_payload

# Command to start the bot and check membership
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''
    Wᴇʟᴄᴏᴍᴇ, {user_name}! 🎉\n🤖 Tʜɪs Is Yᴏᴜʀ Fᴀᴛʜᴇʀ's Bᴏᴛ Sᴇʀᴠɪᴄᴇ, Pʀᴏᴠɪᴅɪɴɢ Exᴄʟᴜsɪᴠᴇ Sᴇʀᴠɪᴄᴇs!\n🚨 Fᴏʀ Assɪsᴛᴀɴᴄᴇ, Tʏᴘᴇ /help
    '''
    
    # Load users and keys data
    users, keys = load_data()

    # Check if user is a member of all groups
    if check_membership(message.chat.id):
        bot.reply_to(message, response)
    else:
        # Send message with image and join buttons for all groups
        image_url = "https://i.ibb.co/Rb9fFpG/photo-2024-12-15-14-34-45.jpg"  # Image URL
        bot.send_photo(message.chat.id, image_url, caption="  🟢 Wʜᴇɴ Yᴏᴜ Jᴏɪɴᴇᴅ Aʟʟ Cʜᴀɴɴᴇʟ Cʟɪᴄᴋ Oɴ Jᴏɪɴᴇᴅ Bᴜᴛᴛᴏɴ 🟢 ", reply_markup=get_inline_keyboard())

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''
💡 Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs:

/start - Sᴛᴀʀᴛ Tʜᴇ Bᴏᴛ Aɴᴅ Gᴇᴛ Wᴇʟᴄᴏᴍᴇ Mᴇssᴀɢᴇ 🤖
/rules - Vɪᴇᴡ Tʜᴇ Rᴜʟᴇs Oғ Tʜᴇ Bᴏᴛ 📜
/redeem <code>key</code> - Rᴇᴅᴇᴇᴍ Yᴏᴜʀ Kᴇʏ 🆙
/payload1 <code>size</code> - Gᴇɴᴇʀᴀᴛᴇ Pᴀʏʟᴏᴀᴅ Oғ Gɪᴠᴇɴ Sɪᴢᴇ Iɴ Kʙ like this = \\x74\\x6d\\x75\\
/payload2 <code>size</code> - Gᴇɴᴇʀᴀᴛᴇ Pᴀʏʟᴏᴀᴅ Oғ Gɪᴠᴇɴ Sɪᴢᴇ Iɴ Kʙ like this = 0x4e, 0xfe, 0x78
/payload3 <code>up.bin copy paste here </code> - Gᴇɴᴇʀᴀᴛᴇ Pᴀʏʟᴏᴀᴅ 
/payload4 <code> give hex file up.bin or down.bin </code> Gᴇɴᴇʀᴀᴛᴇ Pᴀʏʟᴏᴀᴅ 
/info <code> to know info </code> 
/genkey - Gᴇɴᴇʀᴀᴛᴇ A Nᴇᴡ Kᴇʏ (Aᴅᴍɪɴ Oɴʟʏ)
/feedback - Sᴇɴᴅ Yᴏᴜʀ Fᴇᴇᴅʙᴀᴄᴋ 📝
/status - Cʜᴇᴄᴋ Yᴏᴜʀ Sᴛᴀᴛᴜs ✨
/owner - Cᴏɴᴛᴀᴄᴛ Tʜᴇ Bᴏᴛ Oᴡɴᴇʀ 🧑‍💼

Fᴏʀ Mᴏʀᴇ Iɴғᴏ, Cᴏɴᴛᴀᴄᴛ @RARExxOWNER 📨
    '''
    bot.reply_to(message, help_text, parse_mode='HTML', reply_markup=get_contact_owner_keyboard())




# Callback handler for checking if the user is joined
@bot.callback_query_handler(func=lambda call: call.data == "check_joined")
def check_joined(call):
    if check_membership(call.from_user.id):
        # If the user is a member of all channels, send a confirmation message
        bot.answer_callback_query(call.id, "✔️ Yᴏᴜ Hᴀᴠᴇ Jᴏɪɴᴇᴅ Aʟʟ Gʀᴏᴜᴘs! Nᴏᴡ Yᴏᴜ Cᴀɴ Usᴇ Tʜᴇ Bᴏᴛ ✔️", show_alert=True)
        # Welcome message after successful verification
        bot.send_message(call.from_user.id, "🎉 Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs! Yᴏᴜ'ᴠᴇ Jᴏɪɴᴇᴅ Aʟʟ Tʜᴇ Cʜᴀɴɴᴇʟs. Yᴏᴜ Cᴀɴ Nᴏᴡ Usᴇ Tʜᴇ Bᴏᴛ Cᴏᴍᴍᴀɴᴅs 🎉\n👨‍💻 Usᴇ /help Tᴏ Hᴇʟᴘ Iɴ Cᴏᴍᴍᴀɴᴅs 👨‍💻")
    else:
        # If the user is not a member of all channels, ask them to join
        bot.answer_callback_query(call.id, "❌ Yᴏᴜ Nᴇᴇᴅ Tᴏ Jᴏɪɴ Aʟʟ Tʜᴇ Rᴇǫᴜɪʀᴇᴅ Gʀᴏᴜᴘs Fɪʀsᴛ ❌ ", show_alert=True)
        bot.send_message(call.from_user.id, "🐦‍🔥⃤⃟⃝🦅 Pʟᴇᴀsᴇ Jᴏɪɴ Tʜᴇ Rᴇǫᴜɪʀᴇᴅ Gʀᴏᴜᴘs Aɴᴅ Pʀᴇss Tʜᴇ Bᴜᴛᴛᴏɴ Aɢᴀɪɴ Tᴏ Cʜᴇᴄᴋ 🐦‍🔥⃤⃟⃝🦅")

@bot.message_handler(commands=['redeem'])
def redeem_key_command(message):
    user_id = str(message.chat.id)
    # Check if user is a member of all groups
    if not check_membership(message.chat.id):
        bot.reply_to(message, "❌ Yᴏᴜ Nᴇᴇᴅ Tᴏ Jᴏɪɴ Aʟʟ Gʀᴏᴜᴘs Fɪʀsᴛ. Pʟᴇᴀsᴇ Usᴇ /sᴛᴀʀᴛ Tᴏ Jᴏɪɴ Tʜᴇ Gʀᴏᴜᴘs ❌ ", reply_markup=get_contact_owner_keyboard())
        return

    command = message.text.split()
    if len(command) == 2:
        key = command[1]
        # Load data
        users, keys = load_data()
        
        if key in keys:
            expiration_date = keys[key]
            users[user_id] = expiration_date
            save_data(users, keys)
            del keys[key]  # Remove redeemed key
            save_data(users, keys)
            response = f"✅ Key redeemed successfully! Access granted until: {expiration_date}"
        else:
            response = "❌ Invalid or expired key."
    else:
        response = "🔴 Usage: /redeem <key>"

    bot.reply_to(message, response, reply_markup=get_contact_owner_keyboard())  # Only "Contact Owner" button


# Command to generate payload1 with inline keyboard
@bot.message_handler(commands=['payload1'])
def payload1_command(message):
    user_id = str(message.chat.id)
    
    # Load users and keys data
    users, keys = load_data()

    # Check if the user has redeemed a key
    if user_id not in users:
        bot.reply_to(message, "❌ Yᴏᴜ Nᴇᴇᴅ Tᴏ Rᴇᴅᴇᴇᴍ A Kᴇʏ Fɪʀsᴛ Tᴏ Aᴄᴄᴇss Tʜɪs Cᴏᴍᴍᴀɴᴅ.", reply_markup=get_contact_owner_keyboard())
        return

    # Check if user has joined the required groups
    if not check_membership(message.chat.id):
        bot.reply_to(message, "❌ Yᴏᴜ Nᴇᴇᴅ Tᴏ Jᴏɪɴ Aʟʟ Gʀᴏᴜᴘs Fɪʀsᴛ. Pʟᴇᴀsᴇ Usᴇ /sᴛᴀʀᴛ Tᴏ Jᴏɪɴ Tʜᴇ Gʀᴏᴜᴘs.", reply_markup=get_contact_owner_keyboard())
        return

    # Parse the payload size from the message
    command = message.text.split()
    if len(command) == 2:
        try:
            size_kb = int(command[1])
            if size_kb <= 0:
                bot.reply_to(message, "❌ Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ A Vᴀʟɪᴅ Pᴏsɪᴛɪᴠᴇ Iɴᴛᴇɢᴇʀ Fᴏʀ Tʜᴇ Sɪᴢᴇ Iɴ KB.", reply_markup=get_contact_owner_keyboard())
                return

            # Generate the payload
            payload = generate_payload1(size_kb)

            # Split the payload into chunks if it's too large for Telegram (max message length is 4096 characters)
            chunk_size = 4096 - len("Gᴇɴᴇʀᴀᴛᴇᴅ Pᴀʏʟᴏᴀᴅ:\n```\n")  # Adjusting for header text length
            chunks = [payload[i:i + chunk_size] for i in range(0, len(payload), chunk_size)]

            # Send each chunk of the payload
            for chunk in chunks:
                bot.reply_to(message, f'Gᴇɴᴇʀᴀᴛᴇᴅ Pᴀʏʟᴏᴀᴅ:\n```\n{chunk}\n```', parse_mode="Markdown", reply_markup=get_contact_owner_keyboard())
                
        except ValueError:
            bot.reply_to(message, "❌ Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ A Vᴀʟɪᴅ Iɴᴛᴇɢᴇʀ Sɪᴢᴇ Fᴏʀ Tʜᴇ Pᴀʏʟᴏᴀᴅ Iɴ KB (e.g., /payload1 1).", reply_markup=get_contact_owner_keyboard())
    else:
        bot.reply_to(message, "❌ Iɴᴄᴏʀʀᴇᴄᴛ Usᴀɢᴇ. Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ Tʜᴇ Pᴀʏʟᴏᴀᴅ Sɪᴢᴇ (e.g., /payload1 1).", reply_markup=get_contact_owner_keyboard())

# Command to generate payload2 with inline keyboard
@bot.message_handler(commands=['payload2'])
def payload2_command(message):
    user_id = str(message.chat.id)
    
    # Load users and keys data
    users, keys = load_data()

    # Check if the user has redeemed a key
    if user_id not in users:
        bot.reply_to(message, "❌ Yᴏᴜ Nᴇᴇᴅ Tᴏ Rᴇᴅᴇᴇᴍ A Kᴇʏ Fɪʀsᴛ Tᴏ Aᴄᴄᴇss Tʜɪs Cᴏᴍᴍᴀɴᴅ", reply_markup=get_contact_owner_keyboard())
        return

    # Check if user has joined the required groups
    if not check_membership(message.chat.id):
        bot.reply_to(message, " ❌ Yᴏᴜ Nᴇᴇᴅ Tᴏ Jᴏɪɴ Aʟʟ Gʀᴏᴜᴘs Fɪʀsᴛ. Pʟᴇᴀsᴇ Usᴇ /sᴛᴀʀᴛ Tᴏ Jᴏɪɴ Tʜᴇ Gʀᴏᴜᴘs.", reply_markup=get_contact_owner_keyboard())
        return

    # Parse the payload size from the message
    command = message.text.split()
    if len(command) == 2:
        try:
            size_kb = int(command[1])
            if size_kb <= 0:
                bot.reply_to(message, "❌ Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ A Vᴀʟɪᴅ Pᴏsɪᴛɪᴠᴇ Iɴᴛᴇɢᴇʀ Fᴏʀ Tʜᴇ Sɪᴢᴇ Iɴ KB.", reply_markup=get_contact_owner_keyboard())
                return

            # Generate the payload
            payload = generate_payload2(size_kb)

            # Split the payload into chunks if it's too large for Telegram (max message length is 4096 characters)
            chunk_size = 4096 - len("Gᴇɴᴇʀᴀᴛᴇᴅ Pᴀʏʟᴏᴀᴅ:\n```\n")  # Adjusting for header text length
            chunks = [payload[i:i + chunk_size] for i in range(0, len(payload), chunk_size)]

            # Send each chunk of the payload
            for chunk in chunks:
                bot.reply_to(message, f'Gᴇɴᴇʀᴀᴛᴇᴅ Pᴀʏʟᴏᴀᴅ:\n```\n{chunk}\n```', parse_mode="Markdown", reply_markup=get_contact_owner_keyboard())
                
        except ValueError:
            bot.reply_to(message, "❌ Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ A Vᴀʟɪᴅ Iɴᴛᴇɢᴇʀ Sɪᴢᴇ Fᴏʀ Tʜᴇ Pᴀʏʟᴏᴀᴅ Iɴ KB (e.g., /payload2 1).", reply_markup=get_contact_owner_keyboard())
    else:
        bot.reply_to(message, "❌ Iɴᴄᴏʀʀᴇᴄᴛ Usᴀɢᴇ. Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ Tʜᴇ Pᴀʏʟᴏᴀᴅ Sɪᴢᴇ (e.g., /payload2 1).", reply_markup=get_contact_owner_keyboard())


# Set of characters to choose from for the key (letters and digits only)
CHAR_SET = string.ascii_letters + string.digits  # Letters and digits (no symbols)

# Function to generate the key
def generate_key(length=11):
    return ''.join(random.choice(CHAR_SET) for _ in range(length))

# Function to add expiration in days or months
def get_expiration_date(duration, unit='days'):
    if unit == 'months':
        # Adding months (assuming 30 days per month for simplicity)
        return (datetime.now() + timedelta(days=30 * duration)).strftime("%Y-%m-%d %H:%M:%S")
    elif unit == 'days':
        # Adding days
        return (datetime.now() + timedelta(days=duration)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError(" Iɴᴠᴀʟɪᴅ Uɴɪᴛ. Pʟᴇᴀsᴇ Usᴇ 'ᴅᴀʏs' Oʀ 'ᴍᴏɴᴛʜs'.")

@bot.message_handler(commands=['genkey'])
def genkey_command(message):
    if message.chat.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Yᴏᴜ Dᴏ Nᴏᴛ Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Kᴇʏs.", reply_markup=get_contact_owner_keyboard())
        return

    # Parse the message to extract duration and unit
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise ValueError("Iɴᴄᴏʀʀᴇᴄᴛ Fᴏʀᴍᴀᴛ. Usᴇ: /genkey <ᴅᴜʀᴀᴛɪᴏɴ> <ᴜɴɪᴛ (ᴅᴀʏs/ᴍᴏɴᴛʜs)>")

        duration = int(parts[1])  # Number of days or months
        unit = parts[2].lower()  # 'day', 'days', 'month', or 'months'

        # Validate the unit
        if unit not in ['day', 'days', 'month', 'months']:
            raise ValueError("Iɴᴠᴀʟɪᴅ Uɴɪᴛ. Pʟᴇᴀsᴇ Usᴇ 'ᴅᴀʏ(s)' Oʀ 'ᴍᴏɴᴛʜ(s)'.")

        # Generate the alphanumeric key and calculate the expiration date
        key = generate_key()  # Generate the 11-character alphanumeric key
        expiration_date = get_expiration_date(duration, unit)  # Get expiration date

        # Load existing keys
        users, keys = load_data()

        # Store the key and its expiration date
        keys[key] = expiration_date
        save_data(users, keys)

        # Send the key wrapped in <pre><code> tags for HTML formatting
        bot.reply_to(
            message, 
            f"✅ Nᴇᴡ Kᴇʏ Gᴇɴᴇʀᴀᴛᴇᴅ: \n<code>{key}</code>\nExᴘɪʀᴀᴛɪᴏɴ Dᴀᴛᴇ: {expiration_date}",
            parse_mode='HTML',
            reply_markup=get_contact_owner_keyboard()  # Include inline keyboard with Contact Owner button
        )
    
    except ValueError as e:
        bot.reply_to(message, f"❌ Error: {str(e)}", reply_markup=get_contact_owner_keyboard())


# Helper function to generate inline keyboard with Contact Owner button
def get_contact_owner_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("👤 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 👤", url="https://t.me/RARExOWNER")
    keyboard.add(button1)
    return keyboard

@bot.message_handler(commands=['rules'])
def show_rules(message):
    rules_text = '''
📜 Bᴏᴛ Rᴜʟᴇs 📜

1. Jᴏɪɴ Aʟʟ Rᴇǫᴜɪʀᴇᴅ Cʜᴀɴɴᴇʟs: Yᴏᴜ Mᴜsᴛ Jᴏɪɴ Aʟʟ Rᴇǫᴜɪʀᴇᴅ Cʜᴀɴɴᴇʟs Tᴏ Aᴄᴄᴇss Tʜᴇ Bᴏᴛ Sᴇʀᴠɪᴄᴇs.

2. Rᴇsᴘᴇᴄᴛ Pʀɪᴠᴀᴄʏ: Dᴏ Nᴏᴛ Sʜᴀʀᴇ Pᴇʀsᴏɴᴀʟ Oʀ Cᴏɴғɪᴅᴇɴᴛɪᴀʟ Iɴғᴏʀᴍᴀᴛɪᴏɴ.

3. Nᴏ Sᴘᴀᴍᴍɪɴɢ: Aᴠᴏɪᴅ Sᴘᴀᴍᴍɪɴɢ Tʜᴇ Bᴏᴛ Wɪᴛʜ Cᴏᴍᴍᴀɴᴅs Oʀ Mᴇssᴀɢᴇs.

4. Bᴇ Rᴇsᴘᴇᴄᴛғᴜʟ: Tʀᴇᴀᴛ Aʟʟ Usᴇʀs Wɪᴛʜ Kɪɴᴅɴᴇss. Oғғᴇɴsɪᴠᴇ Bᴇʜᴀᴠɪᴏʀ Wɪʟʟ Nᴏᴛ Bᴇ Tᴏʟᴇʀᴀᴛᴇᴅ.

5. Rᴇᴅᴇᴇᴍɪɴɢ Kᴇʏs: Rᴇᴅᴇᴇᴍ Vᴀʟɪᴅ Kᴇʏs Tᴏ Aᴄᴄᴇss Pʀᴇᴍɪᴜᴍ Sᴇʀᴠɪᴄᴇs.

6. Gᴇɴᴇʀᴀᴛᴇᴅ Pᴀʏʟᴏᴀᴅs: Usᴇ Gᴇɴᴇʀᴀᴛᴇᴅ Pᴀʏʟᴏᴀᴅs Rᴇsᴘᴏɴsɪʙʟʏ. Nᴏ Mᴀʟɪᴄɪᴏᴜs Usᴇ Aʟʟᴏᴡᴇᴅ.

7. Aᴄᴄᴇssɪɴɢ Cᴏᴍᴍᴀɴᴅs: Sᴏᴍᴇ Cᴏᴍᴍᴀɴᴅs Aʀᴇ Rᴇsᴛʀɪᴄᴛᴇᴅ Bᴀsᴇᴅ Oɴ Kᴇʏ Rᴇᴅᴇᴍᴘᴛɪᴏɴ Aɴᴅ Gʀᴏᴜᴘ Mᴇᴍʙᴇʀsʜɪᴘ.

8. Aᴅᴍɪɴɪsᴛʀᴀᴛɪᴠᴇ Rɪɢʜᴛs: Oɴʟʏ Aᴅᴍɪɴs Cᴀɴ Gᴇɴᴇʀᴀᴛᴇ Nᴇᴡ Kᴇʏs.

9. Cᴏᴍᴘʟɪᴀɴᴄᴇ: Bʏ Usɪɴɢ Tʜɪs Bᴏᴛ, Yᴏᴜ Aɢʀᴇᴇ Tᴏ Tʜᴇsᴇ Rᴜʟᴇs. Vɪᴏʟᴀᴛɪᴏɴ Mᴀʏ Rᴇsᴜʟᴛ Iɴ Rᴇsᴛʀɪᴄᴛᴇᴅ Aᴄᴄᴇss.

Fᴏʀ Mᴏʀᴇ Iɴғᴏ, Cᴏɴᴛᴀᴄᴛ <pre><code>👑@RARExOWNER👑</code></pre>
'''

    bot.reply_to(message, rules_text, parse_mode='HTML', reply_markup=get_contact_owner_keyboard())

@bot.message_handler(commands=['owner'])
def show_owner(message):
    owner_text = '''
🧑‍💼 Bᴏᴛ Oᴡɴᴇʀ 🧑‍💼

Tʜᴇ Oᴡɴᴇʀ Oғ Tʜɪs Bᴏᴛ Is <pre><code>@RARExOWNER</code></pre>. Yᴏᴜ Cᴀɴ Cᴏɴᴛᴀᴄᴛ Tʜᴇ Oᴡɴᴇʀ Fᴏʀ Mᴏʀᴇ Iɴғᴏʀᴍᴀᴛɪᴏɴ Oʀ Sᴜᴘᴘᴏʀᴛ.

Fᴏʀ Mᴏʀᴇ Dᴇᴛᴀɪʟs, Pʟᴇᴀsᴇ Fᴇᴇʟ Fʀᴇᴇ Tᴏ Rᴇᴀᴄʜ Oᴜᴛ Dɪʀᴇᴄᴛʟʏ.

📬 Cᴏɴᴛᴀᴄᴛ Tʜᴇ Oᴡɴᴇʀ Vɪᴀ: <pre><code>@RARExOWNER</code></pre> 📨
'''

    bot.reply_to(message, owner_text, parse_mode='HTML', reply_markup=get_contact_owner_keyboard())

@bot.message_handler(commands=['status'])
def check_status(message):
    # Retrieve user's status, such as key validity or membership status
    user_id = message.from_user.id
    # Example: Assume you have a function `get_user_status` that checks key and membership
    user_status = get_user_status(user_id)
    
    # Display the status to the user
    status_text = f"Status for {message.from_user.username}:\n\n{user_status}"
    
    bot.reply_to(message, status_text)

def get_user_status(user_id):
    # Example logic: Check if the user has a valid key and if they are a member of a group
    # You can replace this with actual logic depending on your database or system
    
    # Mock data:
    user_status = "🔑 Key: Active\n💬 Group Membership: Joined\n"
    return user_status




# Payload3 command
@bot.message_handler(commands=['payload3'])
def payload3_command(message):
    user_input = message.text[len('/payload3 '):].strip()  # Get the user input after the command
    
    # If there's no input, reply with an error message
    if not user_input:
        bot.reply_to(message, "❗ Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ A Tᴇxᴛ ᴏʀ Hᴇx Sᴛʀɪɴɢ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Pᴀʏʟᴏᴀᴅ.")
        return
    
    # Check if input is a valid hex string
    if all(c in '0123456789abcdefABCDEF' for c in user_input.replace(' ', '')):  # It's hex
        payload = generate_payload3_from_hex(user_input)
    else:  # It's plain text or a string
        payload = generate_payload3_from_text(user_input)

    # Replace any instances of '\\xfffd' with random payload bytes
    payload = replace_invalid_with_random(payload)

    # Send the entire payload in one message if under the character limit
    if len(payload) <= 4096:
        bot.reply_to(message, f'Generated Payload:\n```\n{payload}\n```', parse_mode="Markdown")
    else:
        # If the payload exceeds the limit, warn the user
        bot.reply_to(message, "❗ The payload is too large to send in one message. Please reduce the size and try again.")

# Function to replace invalid byte sequences (e.g., \\xfffd) with random bytes
def replace_invalid_with_random(payload):
    # We will replace each occurrence of '\\xfffd' with random byte sequences
    return re.sub(r'\\xfffd', lambda x: f'\\\\x{random.randint(0x00, 0xFF):02x}', payload)

# Function to generate payload3 from text (converts to hex)
def generate_payload3_from_text(text):
    payload = []
    for char in text:
        try:
            # Convert each character to its byte representation
            payload.append(ord(char))
        except UnicodeEncodeError:
            # If character can't be encoded, insert random byte (from 0x00 to 0xFF)
            payload.append(random.randint(0x00, 0xFF))

    # Convert payload bytes to hex representation
    hex_payload = ''.join(f'\\\\x{byte:02x}' for byte in payload)
    
    return hex_payload

# Function to generate payload3 from hex string (validates and formats)
def generate_payload3_from_hex(hex_string):
    # Clean up the input (remove spaces, ensure it's valid hex)
    hex_string = hex_string.replace(' ', '').strip()

    # Check if the length is even, otherwise it's invalid hex
    if len(hex_string) % 2 != 0:
        raise ValueError("Invalid hex string. It should have an even number of characters.")

    # Convert hex string to bytes
    try:
        byte_payload = bytes.fromhex(hex_string)
    except ValueError:
        raise ValueError("Invalid hex string. Please provide a valid hex string.")

    # Convert payload bytes to hex representation
    hex_payload = ''.join(f'\\\\x{byte:02x}' for byte in byte_payload)
    
    return hex_payload

# Helper function to convert hex string to payload in \\xhh format
def hex_to_payload_escape(hex_string):
    try:
        # Ensure the hex string has an even number of characters
        if len(hex_string) % 2 != 0:
            raise ValueError("Hex string must have an even length.")
        
        # Convert the hex string into bytes
        payload = bytes.fromhex(hex_string)
        
        # Convert the bytes into the '\\xhh' format string
        escape_payload = ''.join(f'\\\\x{byte:02x}' for byte in payload)
        
        return escape_payload
    except ValueError as e:
        return f"Error: {e}"

# Helper function to validate file type and size
def validate_file(file):
    # Check if the file is a valid binary file (or any other validation you want)
    if file.mime_type not in ['application/octet-stream']:  # Change based on your file types
        return False, "Invalid file type. Only binary files are supported."

    # Check file size (limit is 20MB for Telegram, but you can adjust)
    if file.file_size > 20 * 1024 * 1024:  # 20MB max
        return False, "File size exceeds the maximum limit of 20MB."

    return True, None

# Store the start time when the bot starts
start_time = time.time()

def get_bot_uptime():
    """
    Returns the bot's uptime as a formatted string.
    """
    uptime_seconds = time.time() - start_time  # Calculate the uptime in seconds
    uptime_hours = uptime_seconds // 3600  # Hours
    uptime_minutes = (uptime_seconds % 3600) // 60  # Minutes
    uptime_seconds = uptime_seconds % 60  # Remaining seconds

    return f"{int(uptime_hours)}h {int(uptime_minutes)}m {int(uptime_seconds)}s"

# Example usage:
print(get_bot_uptime())  # This will print the bot's uptime in the format "Xh Ym Zs"

@bot.message_handler(commands=['info'])
def show_info(message):
    info_text = '''
    🤖 This is your Father's Bot Service!  
    🔑 Access premium services with a valid key.
    📱 Join the channels to use the bot.
    🕑 Current uptime: {uptime}
    '''
    uptime = get_bot_uptime()  # Example function to calculate bot uptime
    bot.reply_to(message, info_text.format(uptime=uptime))

# Command handler for `/payload4`
@bot.message_handler(commands=['payload4'])
def handle_payload_command(message):
    bot.reply_to(message, "Please send a binary file, and I will generate the payload for you.")

# Handler for file uploads (when the user sends a file)
@bot.message_handler(content_types=['document'])
def handle_file(message):
    # Check if the message contains a document (file)
    if message.document:
        file_id = message.document.file_id
        
        # Get the file from Telegram servers
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Download the file
        downloaded_file = bot.download_file(file_path)

        # Validate file type and size
        is_valid, error_message = validate_file(message.document)
        if not is_valid:
            bot.reply_to(message, error_message)
            return

        # Read the file content and convert it to a hex string
        hex_string = downloaded_file.hex()

        # Convert the hex string to the payload format
        payload = hex_to_payload_escape(hex_string)

        # Send the payload to the user
        bot.reply_to(message, f"Here is the payload:\n`{payload}`", parse_mode="Markdown")

        # Optionally, delete the file after processing to save space
        # os.remove(file_path)


# Error handler
@bot.message_handler(func=lambda message: True)
def handle_error(message):
    bot.reply_to(message, "Sorry, something went wrong. Please try again.")


# Main loop to run the bot
if __name__ == "__main__":
    bot.polling(non_stop=True)
