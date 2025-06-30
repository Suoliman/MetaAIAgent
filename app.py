import streamlit as st
from openai import OpenAI
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)


# تحميل البيانات من Google Sheets
def load_data():
    import json
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1OqveZqh87SHps1GNyr-lyZGNj0ogPDx0O1LLk0BLG-0/edit").worksheet("MetaAds")
    data = pd.DataFrame(sheet.get_all_records())
    return data



# واجهة Streamlit
st.set_page_config(page_title="Meta Ads AI", layout="centered")
st.title("🤖 ذكاء إعلاني - Meta Ads")

user_input = st.text_input("اسأل عن حملاتك الإعلانية:")

if user_input:
    df = load_data()
    sample = df[['Campaign Name', 'Impressions', 'Clicks', 'CTR', 'CPC', 'CPM', 'Spend']].tail(10).to_string(index=False)

    prompt = f"""
    هذه بيانات من حملات Meta Ads:\n{sample}

    الآن، أجب على هذا السؤال بناءً على البيانات فقط:
    {user_input}

    جاوب بشكل احترافي، بالعربية، وقدم تحليل واضح.
    """

    res = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    st.write("### ✅ الرد من الذكاء الاصطناعي:")
    st.success(res.choices[0].message.content)
