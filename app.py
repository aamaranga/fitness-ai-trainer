# ============================================
# STEP 1: IMPORT ALL REQUIRED LIBRARIES
# ============================================
import os
import time
import random
from typing import List, Optional
from dotenv import load_dotenv
from groq import Groq
import streamlit as st


# ============================================
# STEP 2: LOAD ENVIRONMENT VARIABLES
# ============================================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


# ============================================
# STEP 3: CONFIGURE THE STREAMLIT PAGE
# ============================================
st.set_page_config(
    page_title="PrecisionFit",
    page_icon="🏋️",
    layout="centered",
)


# ============================================
# STEP 4: CUSTOM CSS - BEAUTIFUL BACKGROUND & STYLING
# ============================================
st.markdown("""
    <style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }
    
    /* Make text white on dark background */
    .stApp, .stMarkdown, .stText, .stTitle, .stSubheader {
        color: #ffffff !important;
    }
    
    /* Style the form container - targets Streamlit's actual form */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Style input fields */
    .stSelectbox, .stSlider, .stMultiSelect, .stTextArea {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    /* Style labels */
    .stSelectbox label, .stSlider label, .stMultiSelect label, .stTextArea label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    /* Style the submit button */
    .stButton button {
        background: linear-gradient(45deg, #FF6B35, #FF3D00) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6) !important;
    }
    
    /* Style success messages */
    .stSuccess {
        background: rgba(40, 167, 69, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(40, 167, 69, 0.3) !important;
        color: #98fb98 !important;
        border-radius: 15px !important;
    }
    
    /* Style error messages */
    .stError {
        background: rgba(220, 53, 69, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(220, 53, 69, 0.3) !important;
        color: #ffb3b3 !important;
        border-radius: 15px !important;
    }
    
    /* Style info messages */
    .stInfo {
        background: rgba(0, 123, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 123, 255, 0.3) !important;
        color: #b3d9ff !important;
        border-radius: 15px !important;
    }
    
    /* Style warning messages */
    .stWarning {
        background: rgba(255, 193, 7, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        color: #ffe28c !important;
        border-radius: 15px !important;
    }
    
    /* Style the generated plan container */
    .plan-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #e0e0e0;
        margin: 1rem 0;
        width: 100% !important;
        max-width: 100% !important;
        overflow-wrap: break-word;
    }
    
    /* Ensure columns fill properly */
    .row-widget.stColumns {
        width: 100% !important;
    }
    
    /* Remove extra spacing in form */
    div[data-testid="stForm"] > div:first-child {
        padding: 0 !important;
    }
    
    /* Style the footer */
    .footer {
        color: rgba(255, 255, 255, 0.5) !important;
        text-align: center;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================
# STEP 5: DISPLAY HEADER WITH WELCOME
# ============================================
st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 style="font-size: 3.5rem; font-weight: bold; background: linear-gradient(45deg, #FF6B35, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🏋️ PrecisionFit
        </h1>
        <p style="color: #b0b0b0; font-size: 1.2rem; margin-top: -0.5rem;">
            Tailored just for you
        </p>
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
            <p style="color: #d0d0d0; margin: 0; font-size: 1.1rem;">
                👋 <strong style="color: #FF6B35;">Welcome!</strong> I'm your personal AI fitness coach. 
                Fill in the form below, and I'll create a workout plan just for you.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)


# ============================================
# STEP 6: CORE FUNCTION - GENERATE WORKOUT PLAN
# ============================================
def generate_workout_plan(
    goal: str,
    experience: str,
    days_available: int,
    equipment: List[str],
    injuries: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Generates a personalized workout plan using Groq's AI.
    Includes error handling for common issues.
    """
    try:
        # --------------------------------------------
        # Step 6a: Get the API key
        # --------------------------------------------
        key = api_key or os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

        # --------------------------------------------
        # Step 6b: Initialize the Groq client
        # --------------------------------------------
        client = Groq(api_key=key)
        model = model or os.getenv("GROQ_MODEL", "llama3-70b-8192")

        # --------------------------------------------
        # Step 6c: Build the prompt
        # --------------------------------------------
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

Format the response clearly with markdown (headings, bullet points, emojis, etc.)."""

        # --------------------------------------------
        # Step 6d: Call the Groq API with retry for rate limits
        # --------------------------------------------
        max_retries = 3
        for attempt in range(max_retries):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful fitness expert."},
                        {"role": "user", "content": prompt}
                    ],
                    model=model,
                    temperature=0.6,
                    max_tokens=1000,
                )
                break  # Success - exit retry loop
                
            except Exception as api_error:
                # If it's a rate limit and we have more retries, wait and try again
                if "rate_limit" in str(api_error).lower() and attempt < max_retries - 1:
                    time.sleep(2)  # Wait 2 seconds before retry
                    continue
                else:
                    raise  # Re-raise if not rate limit or out of retries

        # --------------------------------------------
        # Step 6e: Return the generated plan
        # --------------------------------------------
        return chat_completion.choices[0].message.content

    except Exception as e:
        # Check for specific error types to give better messages
        error_msg = str(e).lower()
        
        if "rate_limit" in error_msg or "too many" in error_msg:
            raise Exception("RateLimitExceeded")
        elif "api_key" in error_msg or "authentication" in error_msg:
            raise Exception("InvalidAPIKey")
        else:
            # Keep the original error but make it cleaner
            raise Exception(f"GenerationError: {str(e)}")


# ============================================
# STEP 7: CREATE THE USER INPUT FORM
# ============================================
with st.form(key="fitness_form"):
    st.subheader("✨ Tell Us About Yourself")
    st.caption("We'll create a customized plan based on your unique needs")

    # --------------------------------------------
    # Step 7a: Two columns for better layout
    # --------------------------------------------
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

    # --------------------------------------------
    # Step 7b: Full width inputs
    # --------------------------------------------
    injuries = st.text_area(
        "⚠️ Injuries or limitations (optional)",
        placeholder="e.g., bad knees, no overhead pressing, lower back pain...",
        help="Any physical constraints that should be taken into account.",
    )

    # --------------------------------------------
    # Step 7c: Submit button
    # --------------------------------------------
    submitted = st.form_submit_button("⛓️‍💥 Generate Workout Plan")


# ============================================
# STEP 8: WHAT HAPPENS WHEN USER CLICKS SUBMIT
# ============================================
if submitted:
    # --------------------------------------------
    # Step 8a: Validate only fields that could be empty
    # --------------------------------------------
    if not equipment:
        st.error("⚠️ Please select at least one equipment option")
        st.stop()

    # --------------------------------------------
    # Step 8b: Check for API key
    # --------------------------------------------
    if not api_key:
        st.info(
            "🔑 **Welcome! Let's Get Started**\n\n"
            "To create your workout plan, we just need one quick setup:\n\n"
            "1. Create a `.env` file in your project folder\n"
            "2. Add: `GROQ_API_KEY=your_key_here`\n"
            "3. Restart the app\n\n"
            "🆓 **Don't have a key?** Get one free at [Groq Console](https://console.groq.com)"
        )
        st.stop()

    # --------------------------------------------
    # Step 8c: Generate the plan
    # --------------------------------------------
    try:
        with st.spinner("🧠 Crafting your personalised workout plan..."):
            plan = generate_workout_plan(
                goal=goal,
                experience=experience,
                days_available=days,
                equipment=equipment,
                injuries=injuries if injuries else None,
            )

        # Display the plan with celebration
        st.markdown("---")
        st.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 15px; margin: 1rem 0;">
                <p style="color: #FFD700; font-size: 1.2rem; margin: 0;">
                    🎉 Your {goal} Plan is Ready!
                </p>
                <p style="color: #b0b0b0; margin: 0.5rem 0 0 0;">
                    📊 Level: {experience} | 📅 Days/Week: {days} | 🛠️ Equipment: {', '.join(equipment)}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        # Display the plan in a nice container
        # st.markdown('<div class="plan-container">', unsafe_allow_html=True)
        st.markdown(plan)
        # st.markdown('</div>', unsafe_allow_html=True)

        st.success("✅ Plan ready! Time to get to work! 💪")

    except Exception as e:
        # --------------------------------------------
        # Step 8d: Handle errors with friendly messages
        # --------------------------------------------
        error_str = str(e).lower()

        if "rate_limit" in error_str or "too many" in error_str:
            st.warning("⏳ **Our AI coach is taking a quick break!**\n\nWait 30 seconds and try again. ☕")

        elif "api_key" in error_str or "authentication" in error_str:
            st.info(
                "🔑 **Setup Needed**\n\n"
                "Check your `.env` file and make sure `GROQ_API_KEY` is correct.\n\n"
                "🔗 Get a free key: [Groq Console](https://console.groq.com)"
            )

        else:
            st.error(f"⚠️ **Oops!** Something went wrong.\n\nDetails: {e}")


# ============================================
# STEP 9: FOOTER
# ============================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: rgba(255, 255, 255, 0.4); padding: 1rem 0;">
        <p style="margin: 0;">🏋️ PrecisionFit - Built for your fitness journey</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">
            ⚠️ Always consult your doctor before starting any new exercise program
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================
# STEP 10: MOTIVATIONAL QUOTE
# ============================================
if not submitted:  # Only show when no plan is generated
    quotes = [
        "💪 The only bad workout is the one that didn't happen.",
        "🔥 Success starts with showing up.",
        "🌟 Your fitness is 100% mental. Your body won't go where your mind doesn't push it.",
        "🏋️ The pain you feel today will be the strength you feel tomorrow.",
        "⚡ Don't stop when you're tired. Stop when you're done.",
        "💫 Every champion was once a beginner.",
        "🎯 Consistency beats intensity every time.",
        "✨ Small daily improvements lead to stunning results."
    ]
    st.markdown("---")
    st.markdown(f"*{random.choice(quotes)}*")