import streamlit as st
from datetime import datetime, timedelta
import requests
import jwt
import json

# --- Zoom API Setup ---
API_KEY = "YOUR_ZOOM_API_KEY"
API_SECRET = "YOUR_ZOOM_API_SECRET"
USER_ID = "your_zoom_email@example.com"

# Generate JWT Token
def generate_jwt_token():
    payload = {
        'iss': API_KEY,
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    token = jwt.encode(payload, API_SECRET, algorithm='HS256')
    return token

# Create Zoom Meeting with fixed password
def create_zoom_meeting(start_time):
    token = generate_jwt_token()
    headers = {
        'authorization': f"Bearer {token}",
        'content-type': "application/json"
    }

    meeting_details = {
        "topic": "Miracle Morning Meeting",
        "type": 2,
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration": 90,
        "password": "1234",
        "settings": {
            "join_before_host": True,
            "mute_upon_entry": True
        }
    }

    response = requests.post(
        f"https://api.zoom.us/v2/users/{USER_ID}/meetings",
        headers=headers,
        data=json.dumps(meeting_details)
    )

    if response.status_code == 201:
        return response.json()
    else:
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Miracle Morning Zoom Link Generator", page_icon="🌄")
st.title("🌄 Miracle Morning Zoom Link Generator")

st.markdown("""
Generate your daily Zoom meeting link with a fixed password and prepare your WhatsApp message.
""")

# Date Selection
default_date = datetime.now() + timedelta(days=1)
meeting_date = st.date_input("Select Meeting Date", value=default_date.date())

if st.button("Generate Zoom Link & Message"):
    meeting_start_time = datetime.combine(meeting_date, datetime.strptime("04:30", "%H:%M").time())
    meeting_data = create_zoom_meeting(meeting_start_time)

    if meeting_data:
        zoom_link = meeting_data['join_url']
        meeting_id = meeting_data['id']

        message = f"""
✳✳✳✳✳✳✳✳✳✳

⭕ Welcome  to  Miracle morning🙏

👉 Sit straight & screen at eye level  

🔔 {meeting_date.strftime('%B %d - %Y %A')}

💥 Miracle Morning Happy Families - Exclusive for MM Clients
-------------------------------------------------
⭕ Join Zoom Meeting👇
{zoom_link}

Meeting ID: {meeting_id}
Passcode: 1234
--------------------------------------------------

⏰ Login from 4:40am

💰 Daily 4.45am - 5:00am SCB & Money Prayer

Live Session from 5:00am
➖➖➖➖➖➖➖➖➖
👉 Reply 👍R once you received this link

✳✳✳✳✳✳✳✳✳✳
"""
        st.success("✅ Zoom Meeting Created Successfully!")
        st.text_area("Here is your WhatsApp Message:", value=message, height=300)
    else:
        st.error("❌ Failed to create Zoom meeting. Please check API credentials.")