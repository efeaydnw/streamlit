import streamlit as st

st.set_page_config(page_title="2026 Dünya Kupası Simülatörü", layout="wide")

st.title("🏆 2026 Dünya Kupası Simülatörü")
st.write("Skorları gir, turnuvayı hesapla, sonra eleme turlarında kazananları tur tur seç.")

# ======================================================
# GRUPLAR
# ======================================================

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

# ======================================================
# FIFA RANKING DEFAULTS
# küçük sayı daha iyi
# ======================================================

FIFA_RANKS = {
    "Fransa": 1,
    "İspanya": 2,
    "Arjantin": 3,
    "İngiltere": 4,
    "Portekiz": 5,
    "Brezilya": 6,
    "Hollanda": 7,
    "Fas": 8,
    "Belçika": 9,
    "Almanya": 10,
    "Hırvatistan": 11,
    "Kolombiya": 13,
    "Senegal": 14,
    "Meksika": 15,
    "ABD": 16,
    "Uruguay": 17,
    "Japonya": 18,
    "İsviçre": 19,
    "İran": 21,
    "Türkiye": 22,
    "Ekvador": 23,
    "Avusturya": 24,
    "Güney Kore": 25,
    "Avustralya": 27,
    "Cezayir": 28,
    "Mısır": 29,
    "Kanada": 30,
    "Norveç": 31,
    "Panama": 33,
    "Fildişi Sahili": 34,
    "İsveç": 38,
    "Paraguay": 40,
    "Çekya": 41,
    "İskoçya": 43,
    "Tunus": 44,
    "Dem. Kongo Cum.": 46,
    "Özbekistan": 50,
    "Katar": 55,
    "Irak": 57,
    "Güney Afrika": 60,
    "Suudi Arabistan": 61,
    "Ürdün": 63,
    "Bosna-Hersek": 65,
    "Yeşil Burun Adl.": 69,
    "Gana": 74,
    "Curaçao": 82,
    "Haiti": 83,
    "Yeni Zelanda": 85,
}

# ======================================================
# STATE
# ======================================================

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "discipline" not in st.session_state:
    st.session_state.discipline = {}

if "fair_play_needed_teams" not in st.session_state:
    st.session_state.fair_play_needed_teams = []

if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "stats" not in st.session_state:
    st.session_state.stats = {}

if "group_rankings" not in st.session_state:
    st.session_state.group_rankings = {}

if "best_thirds" not in st.session_state:
    st.session_state.best_thirds = []

if "round32_matches" not in st.session_state:
    st.session_state.round32_matches = []

if "winners" not in st.session_state:
    st.session_state.winners = {}

if "losers" not in st.session_state:
    st.session_state.losers = {}

# ======================================================
# RESET
# ======================================================

col_reset1, col_reset2 = st.columns(2)

with col_reset1:
    if st.button("🔄 Tüm Turnuvayı Sıfırla"):
        st.session_state.clear()
        st.rerun()

with col_reset2:
    if st.button("♻️ Sadece Eleme Seçimlerini Sıfırla"):
        st.session_state.winners = {}
        st.session_state.losers = {}
        st.rerun()

# ======================================================
# YARDIMCI FONKSİYONLAR
# ======================================================

def group_matches(teams):
    return [
        (teams[0], teams[1]),
        (teams[0], teams[2]),
        (teams[0], teams[3]),
        (teams[1], teams[2]),
        (teams[1], teams[3]),
        (teams[2], teams[3]),
    ]


def fair_play_score(team):
    d = st.session_state.discipline.get(team, {})

    yellow = d.get("yellow", 0)
    second_yellow_red = d.get("second_yellow_red", 0)
    straight_red = d.get("straight_red", 0)
    yellow_and_straight_red = d.get("yellow_and_straight_red", 0)

    return (
        -1 * yellow
        -3 * second_yellow_red
        -4 * straight_red
        -5 * yellow_and_straight_red
    )


def latest_rank_value(team):
    return FIFA_RANKS.get(team, 999)


def previous_rank_value(team):
    return FIFA_RANKS.get(team, 999)


def calculate_group_stats():
    stats = {}

    for g, teams in groups.items():
        for t in teams:
            stats[t] = {
                "team": t,
                "group": g,
                "points": 0,
                "gf": 0,
                "ga": 0,
                "gd": 0,
                "fair_play": fair_play_score(t),
                "latest_rank": latest_rank_value(t),
                "previous_rank": previous_rank_value(t)
            }

    match_results = []

    for (g, t1, t2), (s1, s2) in st.session_state.scores.items():
        stats[t1]["gf"] += s1
        stats[t1]["ga"] += s2
        stats[t2]["gf"] += s2
        stats[t2]["ga"] += s1

        if s1 > s2:
            stats[t1]["points"] += 3
        elif s2 > s1:
            stats[t2]["points"] += 3
        else:
            stats[t1]["points"] += 1
            stats[t2]["points"] += 1

        match_results.append({
            "group": g,
            "team1": t1,
            "team2": t2,
            "score1": s1,
            "score2": s2
        })

    for t in stats:
        stats[t]["gd"] = stats[t]["gf"] - stats[t]["ga"]

    return stats, match_results


def head_to_head_values(team, tied_teams, match_results):
    pts = 0
    gf = 0
    ga = 0

    for m in match_results:
        t1 = m["team1"]
        t2 = m["team2"]
        s1 = m["score1"]
        s2 = m["score2"]

        if t1 in tied_teams and t2 in tied_teams:
            if team == t1:
                gf += s1
                ga += s2

                if s1 > s2:
                    pts += 3
                elif s1 == s2:
                    pts += 1

            elif team == t2:
                gf += s2
                ga += s1

                if s2 > s1:
                    pts += 3
                elif s1 == s2:
                    pts += 1

    return pts, gf - ga, gf


def pre_fair_play_key(team, tied_teams, stats, match_results):
    h2h_pts, h2h_gd, h2h_gf = head_to_head_values(team, tied_teams, match_results)

    return (
        h2h_pts,
        h2h_gd,
        h2h_gf,
        stats[team]["gd"],
        stats[team]["gf"]
    )


def register_fair_play_needed_only_for_real_ties(tied_teams, stats, match_results):
    buckets = {}

    for team in tied_teams:
        key = pre_fair_play_key(team, tied_teams, stats, match_results)

        if key not in buckets:
            buckets[key] = []

        buckets[key].append(team)

    for bucket_teams in buckets.values():
        if len(bucket_teams) > 1:
            for team in bucket_teams:
                if team not in st.session_state.fair_play_needed_teams:
                    st.session_state.fair_play_needed_teams.append(team)


def register_best_third_fair_play_ties(third_rows):
    buckets = {}

    for row in third_rows:
        key = (
            row["points"],
            row["gd"],
            row["gf"]
        )

        if key not in buckets:
            buckets[key] = []

        buckets[key].append(row["team"])

    for bucket_teams in buckets.values():
        if len(bucket_teams) > 1:
            for team in bucket_teams:
                if team not in st.session_state.fair_play_needed_teams:
                    st.session_state.fair_play_needed_teams.append(team)


def rank_group(g, teams, stats, match_results):
    point_groups = {}

    for t in teams:
        p = stats[t]["points"]
        if p not in point_groups:
            point_groups[p] = []
        point_groups[p].append(t)

    ranked = []

    for pts in sorted(point_groups.keys(), reverse=True):
        tied = point_groups[pts]

        if len(tied) == 1:
            ranked.extend(tied)
        else:
            register_fair_play_needed_only_for_real_ties(tied, stats, match_results)

            tied_sorted = sorted(
                tied,
                key=lambda t: (
                    head_to_head_values(t, tied, match_results)[0],
                    head_to_head_values(t, tied, match_results)[1],
                    head_to_head_values(t, tied, match_results)[2],
                    stats[t]["gd"],
                    stats[t]["gf"],
                    stats[t]["fair_play"],
                    -stats[t]["latest_rank"],
                    -stats[t]["previous_rank"]
                ),
                reverse=True
            )

            ranked.extend(tied_sorted)

    return ranked


def calculate_tournament():
    stats, match_results = calculate_group_stats()

    group_rankings = {}
    third_rows = []

    for g, teams in groups.items():
        ranked = rank_group(g, teams, stats, match_results)
        group_rankings[g] = ranked

        third_team = ranked[2]

        third_rows.append({
            "team": third_team,
            "group": g,
            "points": stats[third_team]["points"],
            "gd": stats[third_team]["gd"],
            "gf": stats[third_team]["gf"],
            "fair_play": stats[third_team]["fair_play"],
            "latest_rank": stats[third_team]["latest_rank"],
            "previous_rank": stats[third_team]["previous_rank"]
        })

    register_best_third_fair_play_ties(third_rows)

    best_thirds = sorted(
        third_rows,
        key=lambda x: (
            x["points"],
            x["gd"],
            x["gf"],
            x["fair_play"],
            -x["latest_rank"],
            -x["previous_rank"]
        ),
        reverse=True
    )[:8]

    return stats, group_rankings, best_thirds


def resolve_slot(slot, group_rankings):
    group = slot[0]
    pos = int(slot[1]) - 1
    return group_rankings[group][pos]


def resolve_third_slot(pool, best_thirds, used_third_groups):
    eligible = []

    for row in best_thirds:
        if row["group"] in pool and row["group"] not in used_third_groups:
            eligible.append(row)

    if not eligible:
        for row in best_thirds:
            if row["group"] not in used_third_groups:
                eligible.append(row)

    if not eligible:
        return "3. Takım Bulunamadı"

    chosen = eligible[0]
    used_third_groups.add(chosen["group"])
    return chosen["team"]


def build_round32(group_rankings, best_thirds):
    used_third_groups = set()

    raw_fixtures = [
        {"id": 73, "date": "28 Haziran", "city": "Inglewood", "a": "A2", "b": "B2"},
        {"id": 74, "date": "29 Haziran", "city": "Foxborough", "a": "E1", "third_pool": ["A", "B", "C", "D", "F"]},
        {"id": 75, "date": "29 Haziran", "city": "Guadalupe", "a": "F1", "b": "C2"},
        {"id": 76, "date": "29 Haziran", "city": "Houston", "a": "C1", "b": "F2"},
        {"id": 77, "date": "30 Haziran", "city": "East Rutherford", "a": "I1", "third_pool": ["C", "D", "F", "G", "H"]},
        {"id": 78, "date": "30 Haziran", "city": "Arlington", "a": "E2", "b": "I2"},
        {"id": 79, "date": "30 Haziran", "city": "Mexico City", "a": "A1", "third_pool": ["C", "E", "F", "H", "I"]},
        {"id": 80, "date": "1 Temmuz", "city": "Santa Clara", "a": "D1", "third_pool": ["B", "E", "F", "I", "J"]},
        {"id": 81, "date": "1 Temmuz", "city": "Seattle", "a": "G1", "third_pool": ["A", "E", "H", "I", "J"]},
        {"id": 82, "date": "1 Temmuz", "city": "Atlanta", "a": "L1", "third_pool": ["E", "H", "I", "J", "K"]},
        {"id": 83, "date": "2 Temmuz", "city": "Toronto", "a": "K2", "b": "L2"},
        {"id": 84, "date": "2 Temmuz", "city": "Inglewood", "a": "H1", "b": "J2"},
        {"id": 85, "date": "2 Temmuz", "city": "Vancouver", "a": "B1", "third_pool": ["E", "F", "G", "I", "J"]},
        {"id": 86, "date": "3 Temmuz", "city": "Miami Gardens", "a": "J1", "b": "H2"},
        {"id": 87, "date": "3 Temmuz", "city": "Arlington", "a": "D2", "b": "G2"},
        {"id": 88, "date": "3 Temmuz", "city": "Kansas City", "a": "K1", "third_pool": ["D", "E", "I", "J", "L"]},
    ]

    matches = []

    for f in raw_fixtures:
        team1 = resolve_slot(f["a"], group_rankings)

        if "b" in f:
            team2 = resolve_slot(f["b"], group_rankings)
        else:
            team2 = resolve_third_slot(f["third_pool"], best_thirds, used_third_groups)

        matches.append({
            "id": f["id"],
            "date": f["date"],
            "city": f["city"],
            "team1": team1,
            "team2": team2
        })

    return matches


def get_winner(match_id):
    return st.session_state.winners.get(match_id)


def get_loser(match_id):
    return st.session_state.losers.get(match_id)


def render_stage(stage_title, matches, save_key):
    st.header(stage_title)

    selections = {}

    cols = st.columns(2)

    for idx, match in enumerate(matches):
        with cols[idx % 2]:
            match_id = match["id"]
            team1 = match["team1"]
            team2 = match["team2"]

            with st.container(border=True):
                st.write(f"**Maç {match_id}** | {match.get('date', '')} | {match.get('city', '')}")
                st.write(f"### {team1} vs {team2}")

                current = st.session_state.winners.get(match_id)

                options = [team1, team2]
                default_index = options.index(current) if current in options else 0

                choice = st.radio(
                    "Kazananı seç",
                    options,
                    index=default_index,
                    key=f"radio_{save_key}_{match_id}",
                    horizontal=True
                )

                selections[match_id] = {
                    "choice": choice,
                    "team1": team1,
                    "team2": team2
                }

                if current:
                    st.success(f"Kazanan: {current}")

    if st.button(f"✅ {stage_title} kazananlarını kaydet", key=f"save_stage_{save_key}"):
        for match_id, data in selections.items():
            choice = data["choice"]
            team1 = data["team1"]
            team2 = data["team2"]

            st.session_state.winners[match_id] = choice
            st.session_state.losers[match_id] = team2 if choice == team1 else team1

        st.rerun()


def make_match(match_id, date, city, source1, source2):
    team1 = get_winner(source1)
    team2 = get_winner(source2)

    if not team1 or not team2:
        return None

    return {
        "id": match_id,
        "date": date,
        "city": city,
        "team1": team1,
        "team2": team2
    }

# ======================================================
# SKOR GİRİŞİ
# ======================================================

st.header("⚽ Grup Maç Skorları")

with st.expander("Grup maçlarını aç / kapat", expanded=True):
    for g, teams in groups.items():
        st.subheader(f"Grup {g}")

        for i, (t1, t2) in enumerate(group_matches(teams)):
            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                s1 = st.number_input(
                    t1,
                    min_value=0,
                    step=1,
                    key=f"score_{g}_{i}_{t1}"
                )

            with col2:
                st.write("—")

            with col3:
                s2 = st.number_input(
                    t2,
                    min_value=0,
                    step=1,
                    key=f"score_{g}_{i}_{t2}"
                )

            st.session_state.scores[(g, t1, t2)] = (s1, s2)

# ======================================================
# FAIR PLAY INPUT - SADECE GERÇEKTEN GEREKİRSE
# ======================================================

if st.session_state.fair_play_needed_teams:
    st.header("🟨 Fair Play Gerekli")

    st.warning(
        "Eşitlik sadece aşağıdaki takımlar için fair play kriterine kaldı. "
        "Kart sayılarını girip turnuvayı tekrar hesapla."
    )

    with st.expander("Fair Play kart sayılarını gir", expanded=True):
        for team in st.session_state.fair_play_needed_teams:
            st.write(f"**{team}**")

            c1, c2, c3, c4 = st.columns(4)

            yellow = c1.number_input(
                "Sarı",
                min_value=0,
                step=1,
                key=f"yellow_{team}"
            )

            second_yellow_red = c2.number_input(
                "2. sarı kırmızı",
                min_value=0,
                step=1,
                key=f"second_yellow_red_{team}"
            )

            straight_red = c3.number_input(
                "Direkt kırmızı",
                min_value=0,
                step=1,
                key=f"straight_red_{team}"
            )

            yellow_and_straight_red = c4.number_input(
                "Sarı + direkt kırmızı",
                min_value=0,
                step=1,
                key=f"yellow_straight_{team}"
            )

            st.session_state.discipline[team] = {
                "yellow": yellow,
                "second_yellow_red": second_yellow_red,
                "straight_red": straight_red,
                "yellow_and_straight_red": yellow_and_straight_red
            }

# ======================================================
# HESAPLA
# ======================================================

if st.button("🏆 Turnuvayı Hesapla ve Round of 32 Oluştur"):
    st.session_state.fair_play_needed_teams = []

    stats, group_rankings, best_thirds = calculate_tournament()
    round32_matches = build_round32(group_rankings, best_thirds)

    st.session_state.stats = stats
    st.session_state.group_rankings = group_rankings
    st.session_state.best_thirds = best_thirds
    st.session_state.round32_matches = round32_matches
    st.session_state.winners = {}
    st.session_state.losers = {}
    st.session_state.calculated = True
    st.rerun()

# ======================================================
# SONUÇLAR
# ======================================================

if st.session_state.calculated:
    stats = st.session_state.stats
    group_rankings = st.session_state.group_rankings
    best_thirds = st.session_state.best_thirds
    round32_matches = st.session_state.round32_matches

    st.header("📊 Grup Sıralamaları")

    for g, ranked in group_rankings.items():
        with st.expander(f"Grup {g}", expanded=False):
            for i, t in enumerate(ranked, 1):
                row = stats[t]
                st.write(
                    f"{i}. {t} | "
                    f"{row['points']} puan | "
                    f"AG: {row['gf']} | "
                    f"YG: {row['ga']} | "
                    f"AV: {row['gd']} | "
                    f"Fair Play: {row['fair_play']} | "
                    f"FIFA Rank: {row['latest_rank']}"
                )

    st.header("🥉 En İyi 8 Üçüncü")

    for i, row in enumerate(best_thirds, 1):
        st.write(
            f"{i}. {row['team']} "
            f"(Grup {row['group']}) | "
            f"{row['points']} puan | "
            f"AV: {row['gd']} | "
            f"AG: {row['gf']} | "
            f"Fair Play: {row['fair_play']} | "
            f"FIFA Rank: {row['latest_rank']}"
        )

    st.divider()

    # ======================================================
    # ROUND OF 32
    # ======================================================

    render_stage("⚔️ Son 32 Turu", round32_matches, "r32")

    # ======================================================
    # ROUND OF 16
    # ======================================================

    r16_plan = [
        (89, "4 Temmuz", "Houston", 73, 75),
        (90, "4 Temmuz", "Philadelphia", 74, 77),
        (91, "5 Temmuz", "East Rutherford", 76, 78),
        (92, "5 Temmuz", "Mexico City", 79, 80),
        (93, "6 Temmuz", "Seattle", 81, 82),
        (94, "6 Temmuz", "Arlington", 83, 84),
        (95, "7 Temmuz", "Vancouver", 85, 87),
        (96, "7 Temmuz", "Atlanta", 86, 88),
    ]

    r16_matches = []
    for mid, date, city, s1, s2 in r16_plan:
        m = make_match(mid, date, city, s1, s2)
        if m:
            r16_matches.append(m)

    if r16_matches:
        render_stage("🏅 Son 16 Turu", r16_matches, "r16")

    # ======================================================
    # QUARTER FINALS
    # ======================================================

    qf_plan = [
        (97, "9 Temmuz", "Foxborough", 89, 90),
        (98, "10 Temmuz", "Inglewood", 93, 94),
        (99, "11 Temmuz", "Miami Gardens", 91, 92),
        (100, "11 Temmuz", "Kansas City", 95, 96),
    ]

    qf_matches = []
    for mid, date, city, s1, s2 in qf_plan:
        m = make_match(mid, date, city, s1, s2)
        if m:
            qf_matches.append(m)

    if qf_matches:
        render_stage("🥉 Çeyrek Finaller", qf_matches, "qf")

    # ======================================================
    # SEMI FINALS
    # ======================================================

    sf_plan = [
        (101, "14 Temmuz", "Arlington", 97, 98),
        (102, "15 Temmuz", "Atlanta", 99, 100),
    ]

    sf_matches = []
    for mid, date, city, s1, s2 in sf_plan:
        m = make_match(mid, date, city, s1, s2)
        if m:
            sf_matches.append(m)

    if sf_matches:
        render_stage("🥈 Yarı Finaller", sf_matches, "sf")

    # ======================================================
    # THIRD PLACE
    # ======================================================

    third_place_ready = get_loser(101) and get_loser(102)

    if third_place_ready:
        third_place_match = {
            "id": 103,
            "date": "18 Temmuz",
            "city": "Miami Gardens",
            "team1": get_loser(101),
            "team2": get_loser(102)
        }

        render_stage("🎖️ Üçüncülük Maçı", [third_place_match], "third_place")

    # ======================================================
    # FINAL
    # ======================================================

    final_ready = get_winner(101) and get_winner(102)

    if final_ready:
        final_match = {
            "id": 104,
            "date": "19 Temmuz",
            "city": "East Rutherford",
            "team1": get_winner(101),
            "team2": get_winner(102)
        }

        render_stage("🥇 Final", [final_match], "final")

    if get_winner(104):
        st.balloons()
        st.success(f"🏆 ŞAMPİYON: {get_winner(104)}")

else:
    st.info("Önce grup skorlarını girip **Turnuvayı Hesapla** butonuna bas.")