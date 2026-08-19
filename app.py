import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st  # pyright: ignore[reportMissingImports]

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("No API key found")

client = Groq()
model = os.getenv("GROQ_MODEL", "gpt-oss-20b")

# ------------- Page configuration -------------
st.set_page_config(
    page_title="AI Personal Trainer",
    page_icon="💪",
    layout="centered",
)

st.title("💪 AI Personal Trainer")
st.markdown(
    "Tell me about your fitness goals, experience, and constraints, and I'll generate a "
    "tailored weekly workout plan."
)

# ------------- Sidebar for API key -------------
with st.sidebar:
    st.markdown("---")
    st.caption(
        "The generated plan is for informational purposes only. "
        "Consult a professional before starting any exercise routine."
    )

# ------------- Main form -------------
with st.form(key="fitness_form"):
    st.subheader("Your Profile")

    col1, col2 = st.columns(2)

    with col1:
        goal = st.selectbox(
            "🎯 Fitness Goal",
            options=["Build muscle", "Lose fat", "General fitness", "Improve endurance"],
            index=0,
        )

        experience = st.selectbox(
            "📈 Experience Level",
            options=["Beginner", "Intermediate", "Advanced"],
            index=0,
        )

    with col2:
        days = st.slider(
            "📅 Days available per week",
            min_value=1,
            max_value=7,
            value=3,
            help="How many days can you commit to working out?",
        )

        equipment = st.multiselect(
            "🛠️ Equipment Access",
            options=["No equipment", "Home dumbbells", "Full gym"],
            default=["No equipment"],
            help="Select all that apply.",
        )

    injuries = st.text_area(
        "⚠️ Injuries or limitations (optional)",
        placeholder="e.g., bad knees, no overhead pressing, lower back pain...",
        help="Any physical constraints that should be taken into account.",
    )

    # Submit button
    submitted = st.form_submit_button("🚀 Generate Workout Plan")

# ------------- Generation logic -------------
if submitted:
    if not api_key:
        st.error("Please provide a valid OpenAI API key.")
        st.stop()

    # Build the prompt
    equipment_str = ", ".join(equipment) if equipment else "None specified"
    prompt = f"""
You are an expert fitness coach. Create a detailed weekly workout plan for a person with the following profile:

- Fitness goal: {goal}
- Experience level: {experience}
- Days available per week: {days}
- Equipment access: {equipment_str}
- Injuries or limitations: {injuries if injuries else "None"}

The plan should be safe, effective, and tailored to the individual. Include:
- A brief warm‑up and cool‑down recommendation.
- For each workout day, list exercises with sets, reps, and rest periods.
- If appropriate, suggest progressions or modifications for different levels.
- Provide a short explanation of the rationale behind the plan.

Format the response clearly with markdown (headings, bullet points, etc.).
"""

    try:
        with st.spinner("🧠 Crafting your personalised workout plan..."):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful fitness expert."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            plan = response.choices[0].message.content

        st.success("✅ Your workout plan is ready!")
        st.markdown(plan)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check your API key and try again.")

# ------------- Footer -------------
st.markdown("---")
st.caption("The generated plan is for informational purposes only. Consult a professional before starting any exercise routine.")