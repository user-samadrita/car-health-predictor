import base64
import datetime
import urllib.parse
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="CAR VITAL", page_icon="logo.png")
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
        # ---------- Nearby service centres ----------
ICON_PIN = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8B5E3C" stroke-width="2" stroke-linecap="round"><path d="M12 21s-7-6.2-7-11a7 7 0 0114 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>'
NEAR = {
 "English": ("Nearby service centres", "Your city or area", "Maruti Suzuki service centre", "Any car garage", "Search for", "Open in Google Maps", "Type your city or pincode to see service centres on the map.", "e.g. Salt Lake, Kolkata"),
 "हिन्दी": ("आस-पास के सर्विस सेंटर", "आपका शहर या इलाका", "मारुति सुज़ुकी सर्विस सेंटर", "कोई भी कार गैराज", "खोजें", "Google Maps में खोलें", "मैप पर सर्विस सेंटर देखने के लिए अपना शहर या पिनकोड लिखें।", "जैसे: सॉल्ट लेक, कोलकाता"),
 "বাংলা": ("কাছের সার্ভিস সেন্টার", "আপনার শহর বা এলাকা", "মারুতি সুজুকি সার্ভিস সেন্টার", "যেকোনো গাড়ির গ্যারেজ", "খুঁজুন", "Google Maps-এ খুলুন", "ম্যাপে সার্ভিস সেন্টার দেখতে আপনার শহর বা পিনকোড লিখুন।", "যেমন: সল্টলেক, কলকাতা"),
}
N = NEAR[lang]
section(ICON_PIN, N[0])
from streamlit_geolocation import streamlit_geolocation
LOC = {
 "English": ("Use my current location", "Click the location button below, then allow access in your browser.", "Location found. Showing centres near you.", "Waiting for location. You can also type your city below."),
 "हिन्दी": ("मेरी मौजूदा लोकेशन इस्तेमाल करें", "नीचे लोकेशन बटन दबाएँ और ब्राउज़र में अनुमति दें।", "लोकेशन मिल गई। आपके पास के सेंटर दिख रहे हैं।", "लोकेशन का इंतज़ार है। आप नीचे अपना शहर भी लिख सकते हैं।"),
 "বাংলা": ("আমার বর্তমান লোকেশন ব্যবহার করুন", "নিচের লোকেশন বোতাম চাপুন এবং ব্রাউজারে অনুমতি দিন।", "লোকেশন পাওয়া গেছে। আপনার কাছের সেন্টার দেখানো হচ্ছে।", "লোকেশনের অপেক্ষা চলছে। নিচে শহরের নামও লিখতে পারেন।"),
}
LC = LOC[lang]
coords = None
if st.toggle("📡  " + LC[0]):
    st.caption(LC[1])
    loc = streamlit_geolocation()
    if loc and loc.get("latitude") and loc.get("longitude"):
        coords = f"{loc['latitude']},{loc['longitude']}"
        st.success(LC[2])
    else:
        st.caption(LC[3])
place = st.text_input("📍  " + N[1], "", placeholder=N[7])
kind = st.radio(N[4], [N[2], N[3]], horizontal=True)
target = coords or place.strip()
if target:
    kw = "Maruti Suzuki service centre" if kind == N[2] else "car service garage"
    q = urllib.parse.quote(f"{kw} near {target}")
    st.components.v1.iframe(f"https://www.google.com/maps?q={q}&output=embed", height=380)
    st.link_button(N[5], f"https://www.google.com/maps/search/?api=1&query={q}")
else:
    st.caption(N[6])
    # ---------- Service centre list (OpenStreetMap) ----------
import math
import requests
UA = {"User-Agent": "CarVital-student-prototype/1.0"}

@st.cache_data(ttl=3600, show_spinner=False)
def geocode(q):
    r = requests.get("https://nominatim.openstreetmap.org/search",
                     params={"q": q, "format": "json", "limit": 1, "countrycodes": "in"},
                     headers=UA, timeout=15)
    r.raise_for_status()
    d = r.json()
    return (float(d[0]["lat"]), float(d[0]["lon"])) if d else None

OVERPASS = ["https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://overpass.private.coffee/api/interpreter"]

@st.cache_data(ttl=3600, show_spinner=False)
def find_centres(lat, lon, radius_m, maruti):
    ar = f"(around:{radius_m},{lat},{lon})"
    if maruti:
        body = (f'nwr["name"~"Maruti|Suzuki|Nexa|Arena",i]["shop"~"^(car|car_repair)$"]{ar};'
                f'nwr["brand"~"Maruti|Suzuki",i]["shop"~"^(car|car_repair)$"]{ar};')
    else:
        body = f'nwr["shop"="car_repair"]{ar};'
    q = f"[out:json][timeout:25];({body});out center tags 60;"
    data, last = None, None
    for url in OVERPASS:
        try:
            r = requests.post(url, data={"data": q}, headers=UA, timeout=30)
            r.raise_for_status()
            data = r.json()
            break
        except Exception as e:
            last = e
    if data is None:
        raise last
    out, seen = [], set()
    for el in data.get("elements", []):
        tg = el.get("tags", {})
        la = el.get("lat") or el.get("center", {}).get("lat")
        lo = el.get("lon") or el.get("center", {}).get("lon")
        if la is None or lo is None:
            continue
        key = (tg.get("name", ""), round(la, 4), round(lo, 4))
        if key in seen:
            continue
        seen.add(key)
        parts = [tg.get(k) for k in ("addr:housenumber", "addr:street", "addr:suburb", "addr:city", "addr:postcode")]
        addr = tg.get("addr:full") or ", ".join(p for p in parts if p)
        p1, p2 = math.radians(lat), math.radians(la)
        a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo - lon) / 2) ** 2
        dist = 6371 * 2 * math.asin(math.sqrt(a))
        out.append({"name": tg.get("name", ""), "addr": addr, "dist": dist, "lat": la, "lon": lo,
                    "phone": tg.get("phone") or tg.get("contact:phone") or "",
                    "hours": tg.get("opening_hours", "")})
    return sorted(out, key=lambda x: x["dist"])[:10]

LST = {
 "English": ("Service centres near you", "Search radius (km)", "{n} found within {r} km, nearest first",
             "No centres found here on OpenStreetMap. Try a larger radius, choose Any car garage, or use the Google map above.",
             "Directions", "Phone", "Hours", "Address not listed", "Workshop (name not listed)",
             "List from OpenStreetMap contributors. It may be incomplete, so confirm by phone before visiting.",
             "Could not reach the map data service. Check your internet and try again.",
             "Could not find that place. Try adding the city name."),
 "हिन्दी": ("आपके पास के सर्विस सेंटर", "खोज की दूरी (किमी)", "{r} किमी के अंदर {n} मिले, सबसे पास वाले पहले",
            "यहाँ OpenStreetMap पर कोई सेंटर नहीं मिला। दूरी बढ़ाएँ, कोई भी कार गैराज चुनें, या ऊपर का Google मैप देखें।",
            "रास्ता", "फ़ोन", "समय", "पता उपलब्ध नहीं", "वर्कशॉप (नाम उपलब्ध नहीं)",
            "सूची OpenStreetMap योगदानकर्ताओं से है। यह अधूरी हो सकती है, जाने से पहले फ़ोन पर पुष्टि करें।",
            "मैप डेटा सेवा तक नहीं पहुँच सके। इंटरनेट जाँचकर दोबारा कोशिश करें।",
            "वह जगह नहीं मिली। शहर का नाम जोड़कर देखें।"),
 "বাংলা": ("আপনার কাছের সার্ভিস সেন্টার", "খোঁজার দূরত্ব (কিমি)", "{r} কিমির মধ্যে {n}টি পাওয়া গেছে, কাছেরটি আগে",
           "এখানে OpenStreetMap-এ কোনো সেন্টার পাওয়া যায়নি। দূরত্ব বাড়ান, যেকোনো গাড়ির গ্যারেজ বেছে নিন, বা উপরের Google ম্যাপ দেখুন।",
           "পথ দেখুন", "ফোন", "সময়", "ঠিকানা নেই", "ওয়ার্কশপ (নাম নেই)",
           "তালিকাটি OpenStreetMap অবদানকারীদের থেকে। এটি অসম্পূর্ণ হতে পারে, যাওয়ার আগে ফোনে নিশ্চিত করুন।",
           "ম্যাপ ডেটা সেবায় পৌঁছানো যায়নি। ইন্টারনেট দেখে আবার চেষ্টা করুন।",
           "জায়গাটি পাওয়া যায়নি। শহরের নাম যোগ করে চেষ্টা করুন।"),
}
LS = LST[lang]

latlon, geo_err = None, None
if coords:
    latlon = tuple(float(v) for v in coords.split(","))
elif place.strip():
    try:
        latlon = geocode(place.strip())
        if latlon is None:
            geo_err = LS[11]
    except Exception:
        geo_err = LS[10]

if geo_err:
    st.warning(geo_err)
elif latlon:
    section(ICON_PIN, LS[0])
    rad = st.select_slider(LS[1], options=[3, 5, 10, 20], value=5)
    try:
        with st.spinner("..."):
            centres = find_centres(latlon[0], latlon[1], rad * 1000, kind == N[2])
    except Exception as e:
        centres = None
        st.warning(LS[10])
        st.caption("Details: " + str(e)[:160])
    if centres is not None:
        if not centres:
            st.info(LS[3])
        else:
            st.caption(LS[2].format(n=len(centres), r=rad))
            for cn in centres:
                with st.container(border=True):
                    st.markdown(f"**{cn['name'] or LS[8]}**  ·  {cn['dist']:.1f} km")
                    st.caption(cn["addr"] or LS[7])
                    if cn["phone"]:
                        st.write(f"{LS[5]}: {cn['phone']}")
                    if cn["hours"]:
                        st.caption(f"{LS[6]}: {cn['hours']}")
                    st.link_button(LS[4], f"https://www.google.com/maps/dir/?api=1&destination={cn['lat']},{cn['lon']}")
            st.caption(LS[9])
            # ---------- Part highlight diagram + calendar ----------
row2 = pd.DataFrame([{"car_age": car_age, "km_driven": km_driven, "km_since_service": km_since,
                      "driving_style": style, "traffic": traffic, "rough_road": road}])
score2 = max(0, int(score_model.predict(row2)[0]) - monsoon * 4)
part2 = part_model.predict(row2)[0]
pname2 = t["parts"][part2]

ICON_TARGET = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8B5E3C" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>'
ICON_CAL = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8B5E3C" stroke-width="2" stroke-linecap="round"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>'

def car_svg(part, hi):
    def c_(n, base):
        return hi if part == n else base
    def a_(n):
        return '<animate attributeName="opacity" values="1;0.45;1" dur="1.6s" repeatCount="indefinite"/>' if part == n else ""
    s = f"""<svg viewBox="0 0 200 340" width="190" xmlns="http://www.w3.org/2000/svg">
<rect x="50" y="18" width="100" height="304" rx="44" fill="#F1E8D6" stroke="#8B5E3C" stroke-width="2.5"/>
<rect x="62" y="30" width="76" height="66" rx="16" fill="{c_('Engine oil', '#E4D3BE')}" stroke="#8B5E3C" stroke-width="1.5">{a_('Engine oil')}</rect>
<rect x="68" y="38" width="26" height="16" rx="3" fill="{c_('Battery', '#D9C6AE')}" stroke="#8B5E3C" stroke-width="1.5">{a_('Battery')}</rect>
<path d="M66 110H134L142 150H58Z" fill="#D8C7A8"/>
<rect x="62" y="154" width="76" height="66" rx="8" fill="#EADCC9"/>
<path d="M60 226H140L132 254H68Z" fill="#D8C7A8"/>
<line x1="40" y1="78" x2="160" y2="78" stroke="{c_('Suspension', '#C4AA8D')}" stroke-width="6" stroke-linecap="round">{a_('Suspension')}</line>
<line x1="40" y1="262" x2="160" y2="262" stroke="{c_('Suspension', '#C4AA8D')}" stroke-width="6" stroke-linecap="round">{a_('Suspension')}</line>
<rect x="26" y="52" width="20" height="52" rx="6" fill="#4B3B2F"/>
<rect x="154" y="52" width="20" height="52" rx="6" fill="#4B3B2F"/>
<rect x="26" y="236" width="20" height="52" rx="6" fill="#4B3B2F"/>
<rect x="154" y="236" width="20" height="52" rx="6" fill="#4B3B2F"/>
<circle cx="36" cy="78" r="7" fill="{c_('Brakes', '#C4AA8D')}">{a_('Brakes')}</circle>
<circle cx="164" cy="78" r="7" fill="{c_('Brakes', '#C4AA8D')}">{a_('Brakes')}</circle>
<circle cx="36" cy="262" r="7" fill="{c_('Brakes', '#C4AA8D')}">{a_('Brakes')}</circle>
<circle cx="164" cy="262" r="7" fill="{c_('Brakes', '#C4AA8D')}">{a_('Brakes')}</circle>
</svg>"""
    return s.replace("\n", "")

HLT = {
 "English": ("Where to look", "Most at risk right now", "Based on the inputs above. Updates live.",
             {"Brakes": "Squealing, a longer stopping distance or a soft pedal are warning signs.",
              "Engine oil": "Check the oil level and colour, and the service sticker.",
              "Suspension": "Listen for knocks over bumps and watch for uneven tyre wear.",
              "Battery": "Slow cranking or dim lights can mean a weak battery."}),
 "हिन्दी": ("कहाँ देखें", "अभी सबसे ज़्यादा जोखिम", "ऊपर दी गई जानकारी के आधार पर, तुरंत बदलता है।",
            {"Brakes": "चीं-चीं की आवाज़, रुकने में ज़्यादा दूरी या नरम पेडल चेतावनी हैं।",
             "Engine oil": "ऑयल का लेवल और रंग देखें, और सर्विस स्टिकर जाँचें।",
             "Suspension": "गड्ढों पर खटखट की आवाज़ सुनें और टायर का असमान घिसाव देखें।",
             "Battery": "स्टार्ट होने में देर या मंद लाइटें कमज़ोर बैटरी का संकेत हो सकती हैं।"}),
 "বাংলা": ("কোথায় দেখবেন", "এখন সবচেয়ে ঝুঁকিতে", "উপরের তথ্য অনুযায়ী, সঙ্গে সঙ্গে বদলায়।",
           {"Brakes": "কর্কশ আওয়াজ, থামতে বেশি দূরত্ব বা নরম প্যাডেল সতর্কতার চিহ্ন।",
            "Engine oil": "অয়েলের লেভেল ও রঙ দেখুন এবং সার্ভিস স্টিকার মিলিয়ে নিন।",
            "Suspension": "গর্তে ঠকঠক আওয়াজ শুনুন এবং টায়ারের অসম ক্ষয় দেখুন।",
            "Battery": "স্টার্ট নিতে দেরি বা আলো ম্লান হলে ব্যাটারি দুর্বল হতে পারে।"}),
}
H = HLT[lang]
hi = "#98A07C" if score2 >= 70 else "#D9B77A" if score2 >= 40 else "#C98F73"
section(ICON_TARGET, H[0])
dc1, dc2 = st.columns([1, 1.3])
dc1.markdown('<div style="text-align:center">' + car_svg(part2, hi) + '</div>', unsafe_allow_html=True)
with dc2:
    st.caption(H[1].upper())
    st.subheader(pname2)
    st.write(H[3][part2])
    st.caption(H[2])

CLT = {
 "English": ("Add to calendar", "Next service date", "Download .ics file", "Add to Google Calendar",
             "Car Vital: {part} check", "Car Vital reminder: {part} needs checking. Car health score: {score}/100.",
             "Pick a date and save the reminder to your phone or computer calendar."),
 "हिन्दी": ("कैलेंडर में जोड़ें", "अगली सर्विस की तारीख", ".ics फ़ाइल डाउनलोड करें", "Google Calendar में जोड़ें",
            "Car Vital: {part} की जाँच", "Car Vital रिमाइंडर: {part} की जाँच करवाएँ। कार हेल्थ स्कोर: {score}/100।",
            "तारीख चुनें और रिमाइंडर अपने फ़ोन या कंप्यूटर के कैलेंडर में सेव करें।"),
 "বাংলা": ("ক্যালেন্ডারে যোগ করুন", "পরবর্তী সার্ভিসের তারিখ", ".ics ফাইল ডাউনলোড করুন", "Google Calendar-এ যোগ করুন",
           "Car Vital: {part} পরীক্ষা", "Car Vital রিমাইন্ডার: {part} পরীক্ষা করান। গাড়ির হেলথ স্কোর: {score}/100।",
           "তারিখ বেছে রিমাইন্ডারটি ফোন বা কম্পিউটারের ক্যালেন্ডারে সেভ করুন।"),
}
CL = CLT[lang]
st.markdown("<style>.stDownloadButton > button{border-radius:24px;background:#6B7B4C;color:#F4EFE6;border:none;padding:8px 28px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase}.stDownloadButton > button:hover{background:#8B5E3C;color:#F4EFE6}</style>", unsafe_allow_html=True)
section(ICON_CAL, CL[0])
_today = datetime.date.today()
_next = last_date + datetime.timedelta(days=180)
if _next < _today:
    _next = _today + datetime.timedelta(days=7)
next_date = st.date_input("📅  " + CL[1], _next, min_value=_today)
ev_title = CL[4].format(part=pname2)
ev_desc = CL[5].format(part=pname2, score=score2)
d1 = next_date.strftime("%Y%m%d")
d2 = (next_date + datetime.timedelta(days=1)).strftime("%Y%m%d")
def _esc(x):
    return x.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
ics = "\r\n".join(["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Car Vital//EN", "BEGIN:VEVENT",
                   "UID:carvital-" + stamp + "@carvital", "DTSTAMP:" + stamp,
                   "DTSTART;VALUE=DATE:" + d1, "DTEND;VALUE=DATE:" + d2,
                   "SUMMARY:" + _esc(ev_title), "DESCRIPTION:" + _esc(ev_desc),
                   "BEGIN:VALARM", "TRIGGER:-P1D", "ACTION:DISPLAY", "DESCRIPTION:" + _esc(ev_title), "END:VALARM",
                   "END:VEVENT", "END:VCALENDAR"])
b1, b2 = st.columns(2)
b1.download_button(CL[2], ics, file_name="car_vital_service.ics", mime="text/calendar")
b2.link_button(CL[3], "https://calendar.google.com/calendar/render?action=TEMPLATE&text="
               + urllib.parse.quote(ev_title) + "&dates=" + d1 + "/" + d2 + "&details=" + urllib.parse.quote(ev_desc))
st.caption(CL[6])
