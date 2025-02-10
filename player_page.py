import streamlit as st
import sqlite3

# 데이터베이스 연결 함수
def get_connection():
    conn = sqlite3.connect("game.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# DB 연결 및 테이블 생성 (없으면 생성)
conn = get_connection()
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS players (
        player_id TEXT PRIMARY KEY,
        name TEXT,
        target TEXT,
        word1 TEXT,
        word2 TEXT,
        word3 TEXT,
        count1 INTEGER,
        count2 INTEGER,
        count3 INTEGER
    )
    """
)
conn.commit()

# URL 쿼리 파라미터에서 player 값을 읽음 (st.query_params 사용)
query_params = st.query_params
if "player" not in query_params:
    st.error("URL에 쿼리 파라미터로 player를 지정해주세요. 예: ?player=one")
    st.stop()

# st.query_params는 문자열을 반환합니다.
player_id = query_params["player"]

# 허용된 플레이어: one, stella, riley, master
if player_id not in ["one", "stella", "riley", "master"]:
    st.error("올바른 player 값이 아닙니다. (one, stella, riley, master 중 하나)")
    st.stop()

# DB에서 해당 player의 레코드가 있는지 확인 (없으면 새로 생성)
c.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
row = c.fetchone()
if row is None:
    c.execute(
        "INSERT INTO players (player_id, name, target, word1, word2, word3, count1, count2, count3) VALUES (?, '', '', '', '', '', 0, 0, 0)",
        (player_id,),
    )
    conn.commit()
    c.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
    row = c.fetchone()

st.title(f"{player_id} 전용 페이지")
st.write("다른 플레이어의 정보는 보이지 않습니다. 본인의 정보를 입력하세요.")

# ── 1) 정보 입력 폼 ──
with st.form("player_form"):
    name = st.text_input("이름", value=row["name"])
    target = st.text_input("선택한 사람", value=row["target"])
    word1 = st.text_input("단어 1", value=row["word1"])
    word2 = st.text_input("단어 2", value=row["word2"])
    word3 = st.text_input("단어 3", value=row["word3"])
    submitted = st.form_submit_button("저장")
    if submitted:
        c.execute(
            """
            UPDATE players
            SET name = ?, target = ?, word1 = ?, word2 = ?, word3 = ?
            WHERE player_id = ?
            """,
            (name, target, word1, word2, word3, player_id),
        )
        conn.commit()
        st.success("정보가 저장되었습니다.")
        st.rerun()

# ── 2) 단어 카운트 ──
# 최신 DB 데이터를 다시 읽어옴
c.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
row = c.fetchone()

st.write("### 단어 카운트")
col1, col2, col3 = st.columns(3)
if row["word1"]:
    with col1:
        if st.button(f"{row['word1']} +", key=f"{player_id}_btn1"):
            new_count = row["count1"] + 1
            c.execute("UPDATE players SET count1 = ? WHERE player_id = ?", (new_count, player_id))
            conn.commit()
            st.rerun()
        st.write("카운트:", row["count1"])
if row["word2"]:
    with col2:
        if st.button(f"{row['word2']} +", key=f"{player_id}_btn2"):
            new_count = row["count2"] + 1
            c.execute("UPDATE players SET count2 = ? WHERE player_id = ?", (new_count, player_id))
            conn.commit()
            st.rerun()
        st.write("카운트:", row["count2"])
if row["word3"]:
    with col3:
        if st.button(f"{row['word3']} +", key=f"{player_id}_btn3"):
            new_count = row["count3"] + 1
            c.execute("UPDATE players SET count3 = ? WHERE player_id = ?", (new_count, player_id))
            conn.commit()
            st.rerun()
        st.write("카운트:", row["count3"])

# ── 마스터 전용: 최종 결과 페이지 링크 ──
if player_id == "master":
    st.markdown(
        """
        <a href="/?player=master&page=final_result" target="_self">
            <button style="
                font-size:20px;
                padding:10px 20px;
                background-color:#008CBA;
                color:white;
                border:none;
                border-radius:5px;
                cursor:pointer;">
                최종 결과 확인하기
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )
