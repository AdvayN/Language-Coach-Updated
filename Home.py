import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Master Your Pronunciation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🎯Master Your Pronunciation")
st.subheader("AI-Powered Pronunciation Assessment Through Audio Tests")

# Introduction section
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Welcome to Master Your Pronunciation! 👋
    
    Perfect your pronunciation with our advanced audio-based testing system. 
    Whether you're learning a new language or refining your accent, Master Your Pronunciation provides 
    instant, accurate feedback to help you speak with confidence.
    
    #### 🎤 How It Works
    
    1. **Choose Your Test** - Select from various pronunciation exercises
    2. **Upload Your Audio** - Speak clearly into your microphone
    3. **Get Instant Feedback** - Receive detailed analysis and improvement tips
    """)

with col2:
    st.info("""
    **✨ Key Features**
    
    ✓ Real-time pronunciation analysis
    
    ✓ Detailed feedback
    
    """)

# Getting Started section
st.markdown("---")
st.markdown("### 🚀 Getting Started")

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("""
    #### 📝 Step 1: Prepare
    - Ensure your microphone is working
    - Find a quiet environment
    - Choose your test level
    """)

with col4:
    st.markdown("""
    #### 🎙️ Step 2: Record
    - Read the provided text
    - Speak naturally and clearly
    - Take your time
    """)

with col5:
    st.markdown("""
    #### 📊 Step 3: Review
    - Check your pronunciation score
    - Review detailed feedback
    - Practice problem areas
    """)

# Call to action
st.markdown("---")
st.success("👈 **Ready to begin?** Go to Start Test page from the sidebar to start improving your pronunciation!")

# Additional information
st.markdown("---")
st.markdown("### 💡 Why Pronunciation Matters")
st.markdown("""
Clear pronunciation is essential for effective communication. Whether you're:
- **Learning a new language** - Build confidence in speaking
- **Preparing for interviews** - Make a strong first impression
- **Improving accent** - Enhance clarity and understanding
- **Professional development** - Communicate more effectively at work

Master Your Pronunciation helps you achieve your pronunciation goals with precision and ease.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>© 2025 Pronunciation Excellence | Powered by AI</p>  
</div>
""", unsafe_allow_html=True)