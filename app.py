import streamlit as st import random

st.set_page_config(layout="centered", page_title="Baccarat Predictor")

st.title("Grok vs. Baccarat (Web Version)")

--- SESSION STATE INIT ---

if 'bankroll' not in st.session_state: st.session_state.bankroll = 0.0 st.session_state.base_bet = 0.0 st.session_state.sequence = [] st.session_state.pending_bet = None st.session_state.strategy = 'T3' st.session_state.t3_level = 1 st.session_state.t3_results = []

--- INPUTS ---

st.sidebar.header("Settings") st.session_state.bankroll = st.sidebar.number_input("Bankroll ($)", min_value=0.0, value=st.session_state.bankroll) st.session_state.base_bet = st.sidebar.number_input("Base Bet ($)", min_value=0.0, value=st.session_state.base_bet) st.session_state.strategy = st.sidebar.selectbox("Strategy", ["T3", "Flatbet"], index=["T3", "Flatbet"].index(st.session_state.strategy))

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
advice = "Need at least 9 entries"
if pred:
    if st.session_state.strategy == 'Flatbet':
        bet_amount = st.session_state.base_bet
    else:
        bet_amount = st.session_state.base_bet * st.session_state.t3_level
    if bet_amount <= st.session_state.bankroll:
        st.session_state.pending_bet = (bet_amount, pred)
        advice = f"Next Bet: ${bet_amount:.0f} on {pred} ({conf:.0f}%)"
    else:
        advice = "Insufficient bankroll"
return advice

--- DISPLAY ---

st.subheader("Current Sequence") sequence = st.session_state.sequence[-20:] or ["None"] st.code(", ".join(sequence))

--- RESULT BUTTONS ---

col1, col2 = st.columns(2) with col1: if st.button("Player (P)"): advice = place_result("P") with col2: if st.button("Banker (B)"): advice = place_result("B")

--- STATUS ---

st.markdown(f"Bankroll: ${st.session_state.bankroll:.2f}") st.markdown(f"Base Bet: ${st.session_state.base_bet:.2f}") st.markdown(f"Strategy: {st.session_state.strategy}, T3 L{st.session_state.t3_level}") if st.session_state.pending_bet: bet_amount, bet_side = st.session_state.pending_bet st.success(f"Pending Bet: ${bet_amount:.0f} on {bet_side}") else: st.info("No pending bet")

