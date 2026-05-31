import streamlit as st
from pathlib import Path

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="2026 Dünya Kupası Simülatörü", layout="wide")

# ==========================
# ASSET PATHS
# ==========================
TROPHY_PATH = ASSETS_DIR / "trophy.jpg"
WC2026_PATH = ASSETS_DIR / "worldcup2026.jpg"

# ==========================
# CUSTOM CSS
# ==========================
st.markdown("""
<style>
.stApp {background: linear-gradient(180deg, #0b1020 0%, #11182b 100%); color: #f5f7fb;}
.block-container {padding-top: 1.5rem; max-width: 1400px;}
.hero-box {background: linear-gradient(135deg, rgba(139,21,56,0.30), rgba(212,175,55,0.18)); border-radius: 24px; padding:28px; margin-bottom:22px; box-shadow:0 10px 30px rgba(0,0,0,0.25);}
.hero-title {font-size:46px; font-weight:900; color:#f5f7fb; line-height:1.1; margin-bottom:10px;}
.hero-highlight {color:#d4af37;}
.hero-subtitle {font-size:18px; color:#d7dce8; line-height:1.6; margin-bottom:18px;}
.info-chip {display:inline-block; padding:8px 14px; border-radius:999px; background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.08); margin-right:10px; margin-bottom:10px; color:#f5f7fb; font-size:14px; font-weight:600;}
.section-box {background: rgba(255,255,255,0.04); padding:18px; border-radius:18px; border:1px solid rgba(255,255,255,0.08); margin-bottom:20px; box-shadow:0 8px 24px rgba(0,0,0,0.20);}
.section-title {font-size:24px; font-weight:800; color:#d4af37; margin-bottom:10px;}
.stButton > button {background: linear-gradient(90deg, #8b1538, #d4af37); color:white; border:none; border-radius:12px; font-weight:800; padding:10px 18px;}
.stButton > button:hover {opacity:0.92; transform:translateY(-1px);}
</style>
""", unsafe_allow_html=True)

# ==========================
# HERO
# ==========================
hero_left, hero_right = st.columns([2.2,1], gap="large")
with hero_left:
    st.markdown('<div class="hero-box">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">🏆 2026 <span class="hero-highlight">World Cup</span> Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Grup aşamasını simüle et, en iyi üçüncüleri belirle, eleme turlarını ilerlet ve kendi Dünya Kupası şampiyonunu seç.</div>', unsafe_allow_html=True)
    st.markdown('<span class="info-chip">48 Takım</span>', unsafe_allow_html=True)
    st.markdown('<span class="info-chip">12 Grup</span>', unsafe_allow_html=True)
    st.markdown('<span class="info-chip">Son 32 + Final</span>', unsafe_allow_html=True)
    st.markdown('<span class="info-chip">Interactive Bracket</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with hero_right:
    if TROPHY_PATH.exists():
        st.image(str(TROPHY_PATH), use_container_width=True)
    if WC2026_PATH.exists():
        st.image(str(WC2026_PATH), use_container_width=True)

# ==========================
# GROUPS & FLAGS
# ==========================
groups = {
    "A": ["Meksika", "Güney Afrika", "Güney Kore", "Çekya"],
    "B": ["Kanada", "Bosna-Hersek", "Katar", "İsviçre"],
    "C": ["Brezilya", "Fas", "Haiti", "İskoçya"],
    "D": ["ABD", "Paraguay", "Avustralya", "Türkiye"],
    "E": ["Almanya", "Curaçao", "Fildişi Sahili", "Ekvador"],
    "F": ["Hollanda", "Japonya", "İsveç", "Tunus"],
    "G": ["Belçika", "Mısır", "İran", "Yeni Zelanda"],
    "H": ["İspanya", "Yeşil Burun Adl.", "Suudi Arabistan", "Uruguay"],
    "I": ["Fransa", "Senegal", "Irak", "Norveç"],
    "J": ["Arjantin", "Cezayir", "Avusturya", "Ürdün"],
    "K": ["Portekiz", "Dem. Kongo Cum.", "Özbekistan", "Kolombiya"],
    "L": ["İngiltere", "Hırvatistan", "Gana", "Panama"]
}

TEAM_FLAGS = {
    "Meksika": "🇲🇽","Güney Afrika": "🇿🇦","Güney Kore": "🇰🇷","Çekya": "🇨🇿",
    "Kanada": "🇨🇦","Bosna-Hersek": "🇧🇦","Katar": "🇶🇦","İsviçre": "🇨🇭",
    "Brezilya": "🇧🇷","Fas": "🇲🇦","Haiti": "🇭🇹","İskoçya": "🏴",
    "ABD": "🇺🇸","Paraguay": "🇵🇾","Avustralya": "🇦🇺","Türkiye": "🇹🇷",
    "Almanya": "🇩🇪","Curaçao": "🇨🇼","Fildişi Sahili": "🇨🇮","Ekvador": "🇪🇨",
    "Hollanda": "🇳🇱","Japonya": "🇯🇵","İsveç": "🇸🇪","Tunus": "🇹🇳",
    "Belçika": "🇧🇪","Mısır": "🇪🇬","İran": "🇮🇷","Yeni Zelanda": "🇳🇿",
    "İspanya": "🇪🇸","Yeşil Burun Adl.": "🇨🇻","Suudi Arabistan": "🇸🇦","Uruguay": "🇺🇾",
    "Fransa": "🇫🇷","Senegal": "🇸🇳","Irak": "🇮🇶","Norveç": "🇳🇴",
    "Arjantin": "🇦🇷","Cezayir": "🇩🇿","Avusturya": "🇦🇹","Ürdün": "🇯🇴",
    "Portekiz": "🇵🇹","Dem. Kongo Cum.": "🇨🇩","Özbekistan": "🇺🇿","Kolombiya": "🇨🇴",
    "İngiltere": "🏴","Hırvatistan": "🇭🇷","Gana": "🇬🇭","Panama": "🇵🇦",
}

def display_team(team):
    return f"{TEAM_FLAGS.get(team,'🏳️')} {team}"

# ==========================
# SESSION STATE
# ==========================
if "points" not in st.session_state:
    st.session_state.points = {t:0 for g in groups.values() for t in g}
    st.session_state.goals = {t:0 for g in groups.values() for t in g}

if "matches" not in st.session_state:
    st.session_state.matches = {}

# ==========================
# GRUP MAÇLARI INPUT
# ==========================
st.header("🏟️ Grup Maçları")
for g, teams in groups.items():
    st.subheader(f"Grup {g}")
    matches = [(teams[i], teams[j]) for i in range(4) for j in range(i+1,4)]
    for idx,(t1,t2) in enumerate(matches):
        col1,col2 = st.columns(2)
        s1 = col1.number_input(display_team(t1), min_value=0, step=1, key=f"{g}_{idx}_s1")
        s2 = col2.number_input(display_team(t2), min_value=0, step=1, key=f"{g}_{idx}_s2")
        st.session_state.matches[f"{g}_{idx}"] = (t1,t2,s1,s2)

# ==========================
# PUAN HESAPLAMA
# ==========================
for g, teams in groups.items():
    for t in teams:
        st.session_state.points[t] = 0
        st.session_state.goals[t] = 0
    matches = [(teams[i], teams[j]) for i in range(4) for j in range(i+1,4)]
    for idx,(t1,t2) in enumerate(matches):
        _,_,s1,s2 = st.session_state.matches[f"{g}_{idx}"]
        st.session_state.goals[t1] += s1
        st.session_state.goals[t2] += s2
        if s1>s2:
            st.session_state.points[t1] +=3
        elif s2>s1:
            st.session_state.points[t2] +=3
        else:
            st.session_state.points[t1] +=1
            st.session_state.points[t2] +=1

# ==========================
# GRUP SIRALAMALARI
# ==========================
st.header("📊 Grup Sıralamaları")
group_ranks = {}
for g, teams in groups.items():
    ranked = sorted(teams, key=lambda t: (st.session_state.points[t], st.session_state.goals[t]), reverse=True)
    group_ranks[g] = ranked
    for i,t in enumerate(ranked,start=1):
        st.write(f"{i}. {display_team(t)} | {st.session_state.points[t]} puan | {st.session_state.goals[t]} gol")

# ==========================
# EN İYİ 3.'LER
# ==========================
st.header("🥉 En İyi 3.'ler")
thirds = [group_ranks[g][2] for g in group_ranks]
best_thirds = sorted(thirds, key=lambda t: (st.session_state.points[t], st.session_state.goals[t]), reverse=True)[:8]
for i,t in enumerate(best_thirds,start=1):
    st.write(f"{i}. {display_team(t)}")

# ==========================
# ROUND OF 32
# ==========================
st.header("⚔️ Round of 32")
round32_fixtures = [
    ("A2 vs B2","A2","B2"),
    ("E1 vs "+display_team(best_thirds[0]),"E1","THIRD1"),
    ("F1 vs C2","F1","C2"),
    ("C1 vs F2","C1","F2"),
    ("I1 vs "+display_team(best_thirds[1]),"I1","THIRD2"),
    ("E2 vs I2","E2","I2"),
    ("A1 vs "+display_team(best_thirds[2]),"A1","THIRD3"),
    ("D1 vs "+display_team(best_thirds[3]),"D1","THIRD4"),
    ("G1 vs "+display_team(best_thirds[4]),"G1","THIRD5"),
    ("L1 vs "+display_team(best_thirds[5]),"L1","THIRD6"),
    ("K2 vs L2","K2","L2"),
    ("H1 vs J2","H1","J2"),
    ("B1 vs "+display_team(best_thirds[6]),"B1","THIRD7"),
    ("J1 vs H2","J1","H2"),
    ("D2 vs G2","D2","G2"),
    ("K1 vs "+display_team(best_thirds[7]),"K1","THIRD8"),
]
for i,f in enumerate(round32_fixtures,start=1):
    st.write(f"{i}. {f[0]}")
