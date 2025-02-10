import streamlit as st
import sqlite3

def get_connection():
    conn = sqlite3.connect('game.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_connection()
c = conn.cursor()

# 모든 플레이어의 데이터 조회
c.execute("SELECT * FROM players")
rows = c.fetchall()

st.title("최종 결과 확인")
if not rows:
    st.error("아직 플레이어 데이터가 없습니다.")
    st.stop()

results = []
for row in rows:
    # 각 플레이어별로 3개 단어의 카운트 중 최대값을 승점으로 산정
    counts = [row["count1"], row["count2"], row["count3"]]
    max_count = max(counts)
    results.append((row["player_id"], row["name"], max_count))
    st.write(f"{row['player_id']} ({row['name']}) - 최고 단어 카운트: {max_count}")

# 최고 점수를 가진 플레이어를 승자로 결정
if results:
    winner = max(results, key=lambda x: x[2])
    st.success(f"승자: {winner[1]} (플레이어: {winner[0]}) - {winner[2]}회")
