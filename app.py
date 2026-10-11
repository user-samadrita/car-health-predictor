import base64
import datetime
import urllib.parse
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="CAR VITAL", page_icon="🍃")
score_model = joblib.load("score_model.pkl")
part_model = joblib.load("part_model.pkl")

with open("logo.png", "rb") as f:
    LOGO_B64 = base64.b64encode(f.read()).decode()

T = {
 "English": dict(
  title="CAR VITAL", age="Car age (years)",
  km="Total km driven", kms="Km since last service",
  style="Driving style", styles=["Calm", "Normal", "Aggressive"],
  traffic="Traffic where you drive", traffics=["Low", "Medium", "Heavy"],
  road="Road condition", roads=["Smooth", "Mixed", "Very rough"],
  monsoon="Driving in monsoon / rain", monsoons=["Rarely", "Sometimes", "Often"],
  button="Check my car", good="Good", attn="Needs attention", risky="Risky",
  healthy="Your car looks healthy. Keep up regular servicing.",
  check="**{part} needs checking within {km} km.**",
  cost="Cost saver", fix="Fix now", later="Ignore it, pay later",
  saves="Fixing now saves about Rs {x:,}.", why="Why this result?",
  remind="Service reminder", send="Send on WhatsApp",
  msg="Service reminder: {part} needs checking within {km} km. Car health score: {score}/100.",
  parts={"Brakes": "Brake pads", "Engine oil": "Engine oil", "Suspension": "Suspension", "Battery": "Battery"},
  factors=["Km since service", "Car age", "Total km", "Driving style", "Traffic", "Road", "Monsoon"]),
 "हिन्दी": dict(
  title="कार वाइटल", age="कार की उम्र (वर्ष)",
  km="कुल चली दूरी (किमी)", kms="पिछली सर्विस के बाद किमी",
  style="ड्राइविंग स्टाइल", styles=["शांत", "सामान्य", "तेज़"],
  traffic="ट्रैफिक", traffics=["कम", "मध्यम", "भारी"],
  road="सड़क की हालत", roads=["अच्छी", "मिली-जुली", "बहुत खराब"],
  monsoon="बारिश/मानसून में ड्राइविंग", monsoons=["कम", "कभी-कभी", "अक्सर"],
  button="मेरी कार जाँचें", good="अच्छी", attn="ध्यान दें", risky="जोखिम",
  healthy="आपकी कार ठीक है। नियमित सर्विस करवाते रहें।",
  check="**{part} की जाँच {km} किमी के अंदर करवाएँ।**",
  cost="खर्च की बचत", fix="अभी ठीक कराएँ", later="अनदेखा करें, बाद में भरें",
  saves="अभी ठीक कराने से लगभग Rs {x:,} बचेंगे।", why="यह नतीजा क्यों?",
  remind="सर्विस रिमाइंडर", send="WhatsApp पर भेजें",
  msg="सर्विस रिमाइंडर: {part} की जाँच {km} किमी के अंदर करवाएँ। कार हेल्थ स्कोर: {score}/100।",
  parts={"Brakes": "ब्रेक पैड", "Engine oil": "इंजन ऑयल", "Suspension": "सस्पेंशन", "Battery": "बैटरी"},
  factors=["सर्विस के बाद किमी", "कार की उम्र", "कुल किमी", "ड्राइविंग", "ट्रैफिक", "सड़क", "मानसून"]),
 "বাংলা": dict(
  title="কার ভাইটাল", age="গাড়ির বয়স (বছর)",
  km="মোট চালানো কিমি", kms="শেষ সার্ভিসের পর কিমি",
  style="ড্রাইভিং স্টাইল", styles=["শান্ত", "স্বাভাবিক", "দ্রুত"],
  traffic="ট্রাফিক", traffics=["কম", "মাঝারি", "বেশি"],
  road="রাস্তার অবস্থা", roads=["ভালো", "মিশ্র", "খুব খারাপ"],
  monsoon="বর্ষায় গাড়ি চালানো", monsoons=["কম", "মাঝে মাঝে", "প্রায়ই"],
  button="আমার গাড়ি পরীক্ষা করুন", good="ভালো", attn="নজর দিন", risky="ঝুঁকিপূর্ণ",
  healthy="আপনার গাড়ি ভালো আছে। নিয়মিত সার্ভিস করান।",
  check="**{part} {km} কিমির মধ্যে পরীক্ষা করান।**",
  cost="খরচ সাশ্রয়", fix="এখনই ঠিক করুন", later="অবহেলা করলে পরে খরচ",
  saves="এখন ঠিক করালে প্রায় Rs {x:,} বাঁচবে।", why="এই ফল কেন?",
  remind="সার্ভিস রিমাইন্ডার", send="WhatsApp-এ পাঠান",
  msg="সার্ভিস রিমাইন্ডার: {part} {km} কিমির মধ্যে পরীক্ষা করান। গাড়ির হেলথ স্কোর: {score}/100।",
  parts={"Brakes": "ব্রেক প্যাড", "Engine oil": "ইঞ্জিন অয়েল", "Suspension": "সাসপেনশন", "Battery": "ব্যাটারি"},
  factors=["সার্ভিসের পর কিমি", "গাড়ির বয়স", "মোট কিমি", "ড্রাইভিং", "ট্রাফিক", "রাস্তা", "বর্ষা"]),
}

# ---------- Earthy minimal styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Archivo+Black&display=swap');
html, body, [class*="css"] {
  font-family: 'Archivo Black','Noto Sans Devanagari','Noto Sans Bengali',sans-serif;
}
#MainMenu, header, footer {visibility: hidden;}
.block-container {max-width: 720px; padding-top: 2rem;}
[data-testid="stWidgetLabel"] p {
  font-weight: 800 !important; text-transform: uppercase;
  letter-spacing: 1.5px; font-size: 0.8rem !important; color: #4A3728;
}
.brand {text-align:center; margin-bottom: 18px;}
.brand h1 {
  font-family: 'Bebas Neue','Noto Serif Devanagari','Noto Serif Bengali',serif;
  font-weight: 800; letter-spacing: 5px; color: #4A3728;
  font-size: 2.8rem; margin: 10px 0 0 0; text-transform: uppercase;
}
.brand p {letter-spacing: 4px; color: #7A5C3E; font-size: 0.75rem; margin: 4px 0 0 0;}
.sec {
  display:flex; align-items:center; gap:10px; margin: 28px 0 10px 0;
  font-family: 'Bebas Neue','Noto Serif Devanagari','Noto Serif Bengali',serif;
  font-size: 1.9rem; font-weight: 800; color: #5A3E2B; letter-spacing: 2px;
  border-bottom: 2px solid rgba(139,94,60,0.35); padding-bottom: 6px;
}
.stButton > button, .stLinkButton > a {
  border-radius: 24px; background: #6B7B4C; color: #F4EFE6 !important;
  border: none; padding: 8px 28px; font-weight: 800; letter-spacing: 1.5px;
  text-transform: uppercase;
}
.stButton > button:hover, .stLinkButton > a:hover {background: #8B5E3C; color: #F4EFE6;}
</style>
""", unsafe_allow_html=True)

# Faded watermark
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"]::before {{
  content: ""; position: fixed; inset: 0;
  background: url("data:image/png;base64,{LOGO_B64}") center / 520px no-repeat;
  opacity: 0.09; pointer-events: none;
}}
</style>
""", unsafe_allow_html=True)

LOGO = f'<img src="data:image/png;base64,{LOGO_B64}" width="90" style="border-radius:50%">'
ICON_WHY = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8B5E3C" stroke-width="2" stroke-linecap="round"><path d="M5 20V12M12 20V5M19 20v-6"/></svg>'
ICON_COST = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8B5E3C" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M9 9.5h5a2 2 0 010 4H9.5M9 13.5h5.5a2 2 0 010 4H9M12 7v10"/></svg>'
ICON_BELL = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8B5E3C" stroke-width="2" stroke-linecap="round"><path d="M6 17V11a6 6 0 0112 0v6l1.5 2h-15zM10 21h4"/></svg>'

def section(icon, text):
    st.markdown(f'<div class="sec">{icon}<span>{text}</span></div>', unsafe_allow_html=True)

lang = st.radio("Language / भाषा / ভাষা", list(T.keys()), horizontal=True)
t = T[lang]
LAST = {
 "English": ("Last service date", "Last serviced {m} months ago.", "Service overdue: more than 6 months since the last service."),
 "हिन्दी": ("पिछली सर्विस की तारीख", "पिछली सर्विस {m} महीने पहले हुई थी।", "सर्विस ओवरड्यू: पिछली सर्विस को 6 महीने से ज़्यादा हो गए।"),
 "বাংলা": ("শেষ সার্ভিসের তারিখ", "শেষ সার্ভিস {m} মাস আগে হয়েছে।", "সার্ভিস বাকি: শেষ সার্ভিসের পর ৬ মাসের বেশি হয়ে গেছে।"),
}
L = LAST[lang]


costs = {"Brakes": (1500, 8000), "Engine oil": (2500, 15000),
         "Suspension": (3000, 12000), "Battery": (4500, 9000)}

st.markdown(f"""<div class="brand">{LOGO}<h1>{t['title']}</h1>
<p>AUTOMOTIVE AI · VEHICLE INTELLIGENCE</p></div>""", unsafe_allow_html=True)

car_age = st.number_input("⏳  " + t["age"], 0, 15, 5)
km_driven = st.number_input("🧭  " + t["km"], 0, 200000, 50000, step=1000)
km_since = st.number_input("🛠️  " + t["kms"], 0, 15000, 5000, step=500)
style = st.selectbox("🌬️  " + t["style"], range(3), format_func=lambda i: t["styles"][i])
traffic = st.selectbox("🚦  " + t["traffic"], range(3), format_func=lambda i: t["traffics"][i])
road = st.selectbox("🪨  " + t["road"], range(3), format_func=lambda i: t["roads"][i])
monsoon = st.selectbox("🌧️  " + t["monsoon"], range(3), format_func=lambda i: t["monsoons"][i])
today = datetime.date.today()
last_date = st.date_input("📅  " + L[0], today - datetime.timedelta(days=90), max_value=today)
months = (today - last_date).days // 30


if st.button(t["button"]):
    row = pd.DataFrame([{"car_age": car_age, "km_driven": km_driven,
                         "km_since_service": km_since, "driving_style": style,
                         "traffic": traffic, "rough_road": road}])
    score = int(score_model.predict(row)[0])
    score = max(0, score - monsoon * 4)
    part = part_model.predict(row)[0]
    pname = t["parts"][part]

    if score >= 70:
        st.success(f"{score}/100 🟢 {t['good']}")
    elif score >= 40:
        st.warning(f"{score}/100 🟡 {t['attn']}")
    else:
        st.error(f"{score}/100 🔴 {t['risky']}")



        st.caption(L[1].format(m=months))
    if months > 6:
        st.warning(L[2])
        

    impact = [km_since / 15000 * 30, car_age * 1.5, km_driven / 200000 * 20,
              style * 5, traffic * 3, road * 5, monsoon * 4]
    section(ICON_WHY, t["why"])
    st.bar_chart(pd.DataFrame({"points lost": impact}, index=t["factors"]), color="#8B5E3C")

    if score >= 70:
        st.write(t["healthy"])
    else:
        km_left = max(200, round(score * 15, -2))
        st.write(t["check"].format(part=pname, km=km_left))
        fix_now, later = costs[part]
        section(ICON_COST, t["cost"])
        c1, c2 = st.columns(2)
        c1.metric(t["fix"], f"Rs {fix_now:,}")
        c2.metric(t["later"], f"Rs {later:,}")
        st.info(t["saves"].format(x=later - fix_now))

        section(ICON_BELL, t["remind"])
        text = t["msg"].format(part=pname, km=km_left, score=score)
        st.text_area("reminder", text, label_visibility="collapsed")
        st.link_button(t["send"], "https://wa.me/?text=" + urllib.parse.quote(text))