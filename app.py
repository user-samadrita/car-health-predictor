import urllib.parse
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Smart Car Health Predictor", page_icon="🚗")
score_model = joblib.load("score_model.pkl")
part_model = joblib.load("part_model.pkl")

T = {
 "English": dict(
  title="🚗 Smart Car Health Predictor", age="Car age (years)",
  km="Total km driven", kms="Km since last service",
  style="Driving style", styles=["Calm", "Normal", "Aggressive"],
  traffic="Traffic where you drive", traffics=["Low", "Medium", "Heavy"],
  road="Road condition", roads=["Smooth", "Mixed", "Very rough"],
  monsoon="Driving in monsoon / rain", monsoons=["Rarely", "Sometimes", "Often"],
  button="Check my car", good="Good", attn="Needs attention", risky="Risky",
  healthy="Your car looks healthy. Keep up regular servicing.",
  check="**{part} needs checking within {km} km.**",
  cost="💰 Cost saver", fix="Fix now", later="Ignore it, pay later",
  saves="Fixing now saves about Rs {x:,}.", why="📊 Why this result?",
  remind="📲 Service reminder", send="Send on WhatsApp",
  msg="Service reminder: {part} needs checking within {km} km. Car health score: {score}/100.",
  parts={"Brakes": "Brake pads", "Engine oil": "Engine oil", "Suspension": "Suspension", "Battery": "Battery"},
  factors=["Km since service", "Car age", "Total km", "Driving style", "Traffic", "Road", "Monsoon"]),
 "हिन्दी": dict(
  title="🚗 स्मार्ट कार हेल्थ प्रेडिक्टर", age="कार की उम्र (वर्ष)",
  km="कुल चली दूरी (किमी)", kms="पिछली सर्विस के बाद किमी",
  style="ड्राइविंग स्टाइल", styles=["शांत", "सामान्य", "तेज़"],
  traffic="ट्रैफिक", traffics=["कम", "मध्यम", "भारी"],
  road="सड़क की हालत", roads=["अच्छी", "मिली-जुली", "बहुत खराब"],
  monsoon="बारिश/मानसून में ड्राइविंग", monsoons=["कम", "कभी-कभी", "अक्सर"],
  button="मेरी कार जाँचें", good="अच्छी", attn="ध्यान दें", risky="जोखिम",
  healthy="आपकी कार ठीक है। नियमित सर्विस करवाते रहें।",
  check="**{part} की जाँच {km} किमी के अंदर करवाएँ।**",
  cost="💰 खर्च की बचत", fix="अभी ठीक कराएँ", later="अनदेखा करें, बाद में भरें",
  saves="अभी ठीक कराने से लगभग Rs {x:,} बचेंगे।", why="📊 यह नतीजा क्यों?",
  remind="📲 सर्विस रिमाइंडर", send="WhatsApp पर भेजें",
  msg="सर्विस रिमाइंडर: {part} की जाँच {km} किमी के अंदर करवाएँ। कार हेल्थ स्कोर: {score}/100।",
  parts={"Brakes": "ब्रेक पैड", "Engine oil": "इंजन ऑयल", "Suspension": "सस्पेंशन", "Battery": "बैटरी"},
  factors=["सर्विस के बाद किमी", "कार की उम्र", "कुल किमी", "ड्राइविंग", "ट्रैफिक", "सड़क", "मानसून"]),
 "বাংলা": dict(
  title="🚗 স্মার্ট কার হেলথ প্রেডিক্টর", age="গাড়ির বয়স (বছর)",
  km="মোট চালানো কিমি", kms="শেষ সার্ভিসের পর কিমি",
  style="ড্রাইভিং স্টাইল", styles=["শান্ত", "স্বাভাবিক", "দ্রুত"],
  traffic="ট্রাফিক", traffics=["কম", "মাঝারি", "বেশি"],
  road="রাস্তার অবস্থা", roads=["ভালো", "মিশ্র", "খুব খারাপ"],
  monsoon="বর্ষায় গাড়ি চালানো", monsoons=["কম", "মাঝে মাঝে", "প্রায়ই"],
  button="আমার গাড়ি পরীক্ষা করুন", good="ভালো", attn="নজর দিন", risky="ঝুঁকিপূর্ণ",
  healthy="আপনার গাড়ি ভালো আছে। নিয়মিত সার্ভিস করান।",
  check="**{part} {km} কিমির মধ্যে পরীক্ষা করান।**",
  cost="💰 খরচ সাশ্রয়", fix="এখনই ঠিক করুন", later="অবহেলা করলে পরে খরচ",
  saves="এখন ঠিক করালে প্রায় Rs {x:,} বাঁচবে।", why="📊 এই ফল কেন?",
  remind="📲 সার্ভিস রিমাইন্ডার", send="WhatsApp-এ পাঠান",
  msg="সার্ভিস রিমাইন্ডার: {part} {km} কিমির মধ্যে পরীক্ষা করান। গাড়ির হেলথ স্কোর: {score}/100।",
  parts={"Brakes": "ব্রেক প্যাড", "Engine oil": "ইঞ্জিন অয়েল", "Suspension": "সাসপেনশন", "Battery": "ব্যাটারি"},
  factors=["সার্ভিসের পর কিমি", "গাড়ির বয়স", "মোট কিমি", "ড্রাইভিং", "ট্রাফিক", "রাস্তা", "বর্ষা"]),
}

lang = st.radio("Language / भाषा / ভাষা", list(T.keys()), horizontal=True)
t = T[lang]

costs = {"Brakes": (1500, 8000), "Engine oil": (2500, 15000),
         "Suspension": (3000, 12000), "Battery": (4500, 9000)}

st.title(t["title"])
car_age = st.number_input(t["age"], 0, 15, 5)
km_driven = st.number_input(t["km"], 0, 200000, 50000, step=1000)
km_since = st.number_input(t["kms"], 0, 15000, 5000, step=500)
style = st.selectbox(t["style"], range(3), format_func=lambda i: t["styles"][i])
traffic = st.selectbox(t["traffic"], range(3), format_func=lambda i: t["traffics"][i])
road = st.selectbox(t["road"], range(3), format_func=lambda i: t["roads"][i])
monsoon = st.selectbox(t["monsoon"], range(3), format_func=lambda i: t["monsoons"][i])

if st.button(t["button"]):
    row = pd.DataFrame([{"car_age": car_age, "km_driven": km_driven,
                         "km_since_service": km_since, "driving_style": style,
                         "traffic": traffic, "rough_road": road}])
    score = int(score_model.predict(row)[0])
    score = max(0, score - monsoon * 4)   # monsoon wear adjustment
    part = part_model.predict(row)[0]
    pname = t["parts"][part]

    if score >= 70:
        st.success(f"{score}/100 🟢 {t['good']}")
    elif score >= 40:
        st.warning(f"{score}/100 🟡 {t['attn']}")
    else:
        st.error(f"{score}/100 🔴 {t['risky']}")

    # Why chart: how many points each factor took off
    impact = [km_since / 15000 * 30, car_age * 1.5, km_driven / 200000 * 20,
              style * 5, traffic * 3, road * 5, monsoon * 4]
    st.subheader(t["why"])
    st.bar_chart(pd.DataFrame({"points lost": impact}, index=t["factors"]))

    if score >= 70:
        st.write(t["healthy"])
    else:
        km_left = max(200, round(score * 15, -2))
        st.write(t["check"].format(part=pname, km=km_left))
        fix_now, later = costs[part]
        st.subheader(t["cost"])
        c1, c2 = st.columns(2)
        c1.metric(t["fix"], f"Rs {fix_now:,}")
        c2.metric(t["later"], f"Rs {later:,}")
        st.info(t["saves"].format(x=later - fix_now))

        st.subheader(t["remind"])
        text = t["msg"].format(part=pname, km=km_left, score=score)
        st.text_area("", text)
        st.link_button(t["send"], "https://wa.me/?text=" + urllib.parse.quote(text))
        