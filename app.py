import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st  # pyright: ignore[reportMissingImports]

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

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

def generate_workout_plan(
    goal: str,
    experience: str,
    days_available: int,
    equipment: List[str],
    model: str = None,
    injuries: Optional[str] = None,
    api_key: Optional[str] = None
    
) -> str:
    """
    Generate a personalized workout plan using Groq's LLM API.

    Args:
        goal: Fitness goal (e.g., "Build muscle", "Lose fat")
        experience: Experience level ("Beginner", "Intermediate", "Advanced")
        days_available: Number of days available per week (1-7)
        equipment: List of available equipment options
        injuries: Optional string describing injuries or limitations
        api_key: Groq API key (if None, tries environment variable)
        model: Groq model to use

    Returns:
        str: The generated workout plan as markdown text

    Raises:
        Exception: If API call fails or returns an error
    """
    try:
        # Get API key from parameter or environment
        key = api_key or os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it as  GROQ_API_KEY environment variable."
            )

        # Initialize Groq client
        client = Groq(api_key=key)
        model = os.getenv("GROQ_MODEL", "gpt-oss-20b")

        # Build the prompt
        equipment_str = ", ".join(equipment) if equipment else "None specified"
        injuries_str = injuries if injuries else "None"

        prompt = f"""You are an expert fitness coach. Create a detailed weekly workout plan for a person with the following profile:

- Fitness goal: {goal}
- Experience level: {experience}
- Days available per week: {days_available}
- Equipment access: {equipment_str}
- Injuries or limitations: {injuries_str}

The plan should be safe, effective, and tailored to the individual. Include:
- A brief warm‑up and cool‑down recommendation.
- For each workout day, list exercises with sets, reps, and rest periods.
- If appropriate, suggest progressions or modifications for different levels.
- Provide a short explanation of the rationale behind the plan.

Format the response clearly with markdown (headings, bullet points, etc.)."""

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful fitness expert."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0.7,
            max_tokens=1500,
        )

        # Extract and return the response
        return chat_completion.choices[0].message.content

    except Exception as e:
        # Re-raise with a clear error message
        raise Exception(f"Failed to generate workout plan: {str(e)}")

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
        st.error("API key missing. Please enter your key above to access the tool.")
        st.stop()
    try:
        with st.spinner("🧠 Crafting your personalised workout plan..."):
            # Call the function with type hints
            plan = generate_workout_plan(
                goal=goal,
                experience=experience,
                days_available=days,
                equipment=equipment,
                injuries=injuries if injuries else None,
            )

        st.success("✅ Your workout plan is ready!")
        st.markdown(plan)

    except Exception as e:
        st.error(f"An error occurred: {e}")


# ------------- Footer -------------
st.markdown("---")
st.caption("The generated plan is for informational purposes only. Consult a professional before starting any exercise routine.")