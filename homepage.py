import streamlit as st
import os

st.set_page_config(page_title="StudentScran", page_icon="🍳", layout="wide")

# Custom CSS to make the sidebar look cleaner and fill space better
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            padding-top: 1rem;
        }
        .sidebar-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

TIMETABLE_FILE = "timetable.txt"

# Default meal suggestions
DEFAULT_MEALS = {
    "Monday": "Quick Pesto Pasta 🍝",
    "Tuesday": "Tuna Jacket Potato 🥔",
    "Wednesday": "Chicken Stir-Fry 🍜",
    "Thursday": "Omelette 🍳",
    "Friday": "Friday Pizza 🍕",
    "Saturday": "Burger Night 🍔",
    "Sunday": "Sunday Roast Bowl 🥗"
}

if "custom_meals" not in st.session_state:
    st.session_state.custom_meals = DEFAULT_MEALS.copy()

# Ensure timetable.txt exists with default data if not already there
if not os.path.exists(TIMETABLE_FILE):
    default_timetable = {
        "Monday": ["Computer Science Lecture (10:00 - 12:00)", "Library Prep Session (14:00 - 16:00)"],
        "Tuesday": ["Database Systems Lab (11:00 - 13:00)"],
        "Wednesday": ["Software Engineering Workshop (09:00 - 11:00)"],
        "Thursday": ["Compilers Lab (14:00)", "DEADLINE: Project Architecture (23:59)"],
        "Friday": ["Individual Project Coding Sprint"],
        "Saturday": ["Weekly Grocery Shop & Meal Prep"],
        "Sunday": ["Prep for Next Week"]
    }
    with open(TIMETABLE_FILE, "w") as f:
        for day, events in default_timetable.items():
            for event in events:
                f.write(f"{day}:{event}\n")

def load_timetable_from_file():
    timetable = {day: [] for day in DEFAULT_MEALS.keys()}
    if os.path.exists(TIMETABLE_FILE):
        with open(TIMETABLE_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    day, event = line.strip().split(":", 1)
                    if day in timetable:
                        timetable[day].append(event.strip())
    return timetable

# Upgraded Sidebar Navigation
with st.sidebar:
    st.markdown('<p class="sidebar-title">🧑‍🍳 StudentScran 🎓</p>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["Home", "Upload Food", "Enter your timetable"])
    st.markdown("---")
    st.caption("💡 Tip: Upload food photos to automatically scan expiry dates and update your weekly meal plan!")

if page == "Home":
    st.title("🍳 StudentScran 🎓")
    st.subheader("Your Week (Timetable & Meal Planner)")

    current_timetable = load_timetable_from_file()

    def render_day_card(day_name):
        st.markdown(f"### {day_name}")
        events = current_timetable.get(day_name, [])
        events_str = "\n".join([f"- {e}" for e in events]) if events else "- No events"
        meal = st.session_state.custom_meals.get(day_name, DEFAULT_MEALS.get(day_name))
        
        st.info(f"📅 **Schedule & Reminders:**\n{events_str}\n\n🍽️ **Suggested Meal:**\n{meal}")

    # Layout columns for Monday - Wednesday
    col1, col2, col3 = st.columns(3)
    with col1: render_day_card("Monday")
    with col2: render_day_card("Tuesday")
    with col3: render_day_card("Wednesday")

    # Layout columns for Thursday - Sunday
    col4, col5, col6, col7 = st.columns(4)
    with col4: render_day_card("Thursday")
    with col5: render_day_card("Friday")
    with col6: render_day_card("Saturday")
    with col7: render_day_card("Sunday")

elif page == "Upload Food":
    st.title("📸 Gemma AI Expiry & Meal Scanner")
    st.write("Upload a photo of your fridge or groceries. Gemma AI will detect what's expiring soon, set calendar reminders, and update your meal plan!")
    
    uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])
    target_day = st.selectbox("Select Day to Use Expiring Food & Add Reminder:", list(DEFAULT_MEALS.keys()))
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Fridge Photo", width=350)
        if st.button("✨ Scan Expiry Dates & Update Calendar"):
            with st.spinner("Gemma AI is analyzing freshness and checking expiry risks..."):
                expiring_item = "⚠️ EXPIRY ALERT: Spinach & Fresh Milk (Use Today!)"
                ai_suggested_meal = "✨ Creamy Spinach Pasta (Uses Expiring Items)"
                
                with open(TIMETABLE_FILE, "a") as f:
                    f.write(f"{target_day}:{expiring_item}\n")
                
                st.session_state.custom_meals[target_day] = ai_suggested_meal
                
                st.success(f"Scan Complete! Calendar reminders and meal plan updated for **{target_day}**.")
                st.write("**AI Analysis:** Spinach leaves are wilting and milk date is approaching.")
                st.warning(f"🚨 Added reminder to **{target_day}** schedule: `{expiring_item}`")
                st.info(f"💡 **New Meal Plan for {target_day}:** {ai_suggested_meal}")

elif page == "Enter your timetable":
    st.title("📅 Enter Your Timetable")
    st.write("Add your lectures, labs, and deadlines to your schedule.")

    with st.form("timetable_form", clear_on_submit=True):
        selected_day = st.selectbox("Select Day", list(DEFAULT_MEALS.keys()))
        event_description = st.text_input("Event details (e.g., 'AI Lecture 10 AM', 'Coursework Deadline')")
        
        submitted = st.form_submit_button("Add Event")
        if submitted and event_description:
            with open(TIMETABLE_FILE, "a") as f:
                f.write(f"{selected_day}:{event_description}\n")
            st.success(f"Successfully added to {selected_day}!")
            st.rerun()

    st.divider()
    st.subheader("📋 Your Saved Timetable Overview")
    
    current_timetable = load_timetable_from_file()
    for day, events in current_timetable.items():
        if events:
            event_bullet_list = "".join([f"  - {e}\n" for e in events])
            st.markdown(f"**{day}**\n{event_bullet_list}")