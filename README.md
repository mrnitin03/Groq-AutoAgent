# DigitalNagari-Groq-AutoAgent

Production-grade Python automation using Groq AI and Telegraph API.

## Setup Guide

### 1. Get Groq API Key
- Sign up at [Groq Console](https://console.groq.com/).
- Create an API key and copy it.

### 2. Get Telegraph Token
- Run the generator locally: `python groq_token_generator.py`.
- Copy the token from `telegraph_token.txt`.

### 3. GitHub Configuration
1. Go to your Repository **Settings** > **Secrets and variables** > **Actions**.
2. Create `GROQ_API_KEY` (Paste Groq key).
3. Create `TELEGRAPH_TOKEN` (Paste Telegraph token).
4. Go to **Settings** > **Actions** > **General**.
5. Set **Workflow permissions** to `Read and write permissions`.

### 4. Running
- The bot runs automatically every 6 hours.
- To run manually: Go to **Actions** tab > Select Workflow > **Run workflow**.
