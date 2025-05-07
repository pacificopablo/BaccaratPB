import streamlit as st import random

st.set_page_config(layout="centered", page_title="MANG BACCARAT GROUP")

st.title("MANG BACCARAT GROUP")

--- SESSION STATE INIT ---

if 'bankroll' not in st.session_state: st.session_state.bankroll = 0.0 st.session_state.base_bet = 0.0 st.session_state.sequence = [] st.session_state.pending_bet = None st.session_state.strategy = 'T3' st.session_state.t3_level = 1 st.session_state.t3_results = [] st.session_state.advice = ""

--- MAIN INPUTS ---

st.subheader("Setup") with st.form("setup_form"): bankroll = st.number_input("Enter Bankroll ($)", min_value=0.0, value=st.session_state.bankroll, step=10.0, key="bankroll_input") base_bet = st.number_input("Enter Base Bet ($)", min_value=0.0, value=st.session_state.base_bet, step=1.0, key="basebet_input") strategy = st.selectbox("Choose Strategy", ["T3", "Flatbet"], index=["T3", "Flatbet"].index(st.session_state.strategy), key="strategy_input") start_clicked = st.form_submit_button("Start Session")

if start_clicked: st.session_state.bankroll = bankroll st.session_state.base_bet = base_bet st.session_state.strategy = strategy st.session_state.sequence = [] st.session_state.pending_bet = None st.session_state.t3_level = 1 st.session_state.t3_results = [] st.session_state.advice = "" st.success("Session started!")

--- FUNCTIONS ---

def analyze_pattern(seq): last_9 = seq[-9:] flips = sum(1 for i in range(1, 9) if last_9[i] != last_9[i - 1]) repeats = 8 - flips rule1 = 'P' if flips > repeats else last_9[-1]

seg1 = last_9[0:3]
seg3 = last_9[6:9]
rule2 = seg1[0] if seg3 == seg1 else ('P' if last_9[-1] == 'B' else 'B')

last5 = last_9[-5:]
is_alternating = all(last5[i] != last5[i + 1] for i in range(4))
rule3 = ('P' if last_9[-1] == 'B' else 'B') if is_alternating else last_9[-1]

predictions = [rule1, rule2, rule3]
final = max(set(predictions), key=predictions.count)
confidence = predictions.count(final) / 3 * 100
return final, confidence

def predict_next(): if len(st.session_state.sequence) < 9: return None, 0 return analyze_pattern(st.session_state.sequence)

def place_result(result): bet_amount = 0 if st.session_state.pending_bet: bet_amount, selection = st.session_state.pending_bet if result == selection: if selection == 'B': st.session_state.bankroll += bet_amount * 0.95 else: st.session_state.bankroll += bet_amount st.session_state.t3_results.append('W') else: st.session_state.bankroll -= bet_amount st.session_state.t3_results.append('L')

if len(st.session_state.t3_results) == 3:
        w = st.session_state.t3_results.count('W')
        l = st.session_state.t3_results.count('L')
        if w == 3:
            st.session_state.t3_level = max(1, st.session_state.t3_level - 2)
        elif w == 2:
            st.session_state.t3_level = max(1, st.session_state.t3_level - 1)
        elif l == 2:
            st.session_state.t3_level += 1
        elif l == 3:
            st.session_state.t3_level += 2
        st.session_state.t3_results = []

    st.session_state.pending_bet = None

st.session_state.sequence.append(result)

pred, conf = predict_next()
if pred:
    if st.session_state.strategy == 'Flatbet':
        bet_amount = st.session_state.base_bet
    else:
        bet_amount = st.session_state.base_bet * st.session_state.t3_level
    if bet_amount <= st.session_state.bankroll:
        st.session_state.pending_bet = (bet_amount, pred)
        st.session_state.advice = f"Next Bet: ${bet_amount:.0f} on {pred} ({conf:.0f}%)"
    else:
        st.session_state.advice = "Insufficient bankroll"
else:
    st.session_state.advice = "Need at least 9 entries"

--- DISPLAY ---

st.subheader("Current Sequence") latest_sequence = st.session_state.sequence[-20:] if 'sequence' in st.session_state else [] st.text(", ".join(latest_sequence or ["None"]))

st.subheader("Enter Result") col1, col2 = st.columns(2) with col1: if st.button("Player (P)"): place_result("P") with col2: if st.button("Banker (B)"): place_result("B")

--- STATUS ---

st.subheader("Status") st.markdown(f"Bankroll: ${st.session_state.bankroll:.2f}") st.markdown(f"Base Bet: ${st.session_state.base_bet:.2f}") st.markdown(f"Strategy: {st.session_state.strategy} | T3 Level: {st.session_state.t3_level}") if st.session_state.pending_bet: amount, side = st.session_state.pending_bet st.success(f"Pending Bet: ${amount:.0f} on {side}") else: st.info("No pending bet yet.") st.write(st.session_state.advice)

