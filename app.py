import streamlit as st

#Functions
def calculate_score(sleep, screen_leisure, screen_work, exercise, stress):
    sleep_score = max(0, 40 - abs(sleep-9)*5)

    if screen_leisure <= 6:
        screen_score = 30
    else:
        screen_score = max(0,30-(screen_leisure - 6)*5)

    exercise_score = min(20, (exercise / 30)*20)

    stress_score = (6-stress) * 2

    total_score = sleep_score + screen_score + exercise_score + stress_score
    return total_score

def get_recommendations(sleep, screen_leisure, screen_work, exercise, stress):
    recs = []

    # Sleep
    if sleep < 6:
        recs.append("You're not getting enough sleep. Try to aim for 7-9 hours.")
    elif sleep > 9:
        recs.append("You're oversleeping. Too much sleep can also cause fatigue.")

    # Screen time
    total_screen = screen_leisure + screen_work
    if screen_leisure > 6:
        recs.append("Your leisure screen time is high. Try scheduling no-screen breaks.")
    if total_screen > 10:
        recs.append("You're spending long hours on screens. Use the 20-20-20 rule: every 20 minutes, look 20 feet away for 20 seconds.")

    # Exercise
    if exercise < 30:
        recs.append("You're below the recommended 30 minutes of activity. Consider a short walk or stretch.")

    # Stress
    if stress > 3:
        recs.append("Your stress is elevated. Try deep breathing or a short break from screens.")

    if not recs:
        recs.append("Great balance! Keep maintaining your habits.")

    return recs

def interpret_score(total_score):
    if total_score >= 80:
        return "Balanced ✅", "green"
    elif total_score >= 50:
        return "At Risk ⚠️", "orange"
    else:
        return "High Risk ❌", "red"

#Inputs
st.title("Digital Balance Score")

sleep = st.number_input("Hours slept last night", min_value=0, max_value=24, value=7)
screen_leisure = st.number_input("Hours on social media/leisure screens", min_value=0, max_value=24, value=2)
screen_work = st.number_input("Hours on work screens", min_value=0, max_value=24, value=4)
exercise = st.number_input("Minutes of exercise today", min_value=0, max_value=300, value=30)
stress = st.slider("Rate your stress level (1=low, 5=high)", 1, 5, 3)

#Calculate
total_score = calculate_score(sleep, screen_leisure, screen_work, exercise, stress)
risk, color = interpret_score(total_score)

#Display
st.metric("Your Digital Balance Score", f"{total_score}/100")
st.markdown(f"**Risk Level:** <span style='color:{color}'>{risk}</span>", unsafe_allow_html=True)

st.subheader("Recommendations")
for r in get_recommendations(sleep, screen_leisure, screen_work, exercise, stress):
    st.write(f"- {r}")
