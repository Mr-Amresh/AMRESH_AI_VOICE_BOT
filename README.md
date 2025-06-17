# Amresh Voice Bot

Hey there! I’m Amresh Kumar Yadav, and this is my interactive voice bot built with Streamlit. It lets you ask questions via voice or text, and I’ll respond with insights from my 3+ years as a Generative AI Specialist at ITC Infotech. Ready to deploy this to Streamlit Community Cloud? Let’s get it live in a few simple steps!

## Prerequisites
Before we dive in, make sure you have:
- A GitHub account (to host the code).
- A Streamlit Community Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io) using your GitHub credentials).
- A Groq API key (grab one from [console.groq.com](https://console.groq.com) and store it securely).

## Setup Instructions
1. **Clone or Fork This Repo**
   - Fork this repository to your GitHub account or clone it locally with:
     ```bash
     git clone https://github.com/yourusername/amresh-voice-bot.git
     ```
   - Replace `yourusername` with your GitHub username.

2. **Set Up a Virtual Environment (Optional, for Local Testing)**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Add Your Groq API Key**
   - Create a `.env` file in the project root (don’t commit this to GitHub!):
     ```bash
     echo "GROQ_API_KEY=your_groq_api_key" > .env
     ```
   - Replace `your_groq_api_key` with your actual Groq API key.

4. **Test Locally**
   - Run the app locally to make sure everything’s working:
     ```bash
     streamlit run app.py
     ```
   - Open your browser to `http://localhost:8501` and try the voice or text input.

5. **Push to GitHub**
   - Ensure all files (`app.py`, `requirements.txt`, `packages.txt`) are in your repository.
   - Commit and push to GitHub:
     ```bash
     git add .
     git commit -m "Initial commit for Amresh Voice Bot"
     git push origin main
     ```

## Deploying to Streamlit Community Cloud
1. **Log In to Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
   - Authorize Streamlit to access your public repositories (or private ones if needed).

2. **Create a New App**
   - Click **New App** on the Streamlit dashboard.
   - Select your repository (e.g., `yourusername/amresh-voice-bot`).
   - Choose the branch (e.g., `main`).
   - Set the main file path to `app.py`.
   - Click **Deploy**.

3. **Wait for Deployment**
   - Streamlit will pull your code, install dependencies from `requirements.txt`, and set up `espeak` from `packages.txt`.
   - Once deployed, you’ll get a unique URL (e.g., `https://your-app-name.streamlit.app`).

## Notes
- **Voice Input**: The speech recognition uses your browser’s microphone, so ensure it’s enabled. Text-to-speech (`pyttsx3`) may not work on Streamlit Cloud due to server limitations, but text responses will always display.
-
