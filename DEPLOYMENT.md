# Getting Your Live Link (Deployment Guide)

You successfully connected the **Nexus AI Healthcare System** to your live Firebase database! However, the application currently runs on your local computer (`localhost:8501`).

To get a **live link** that you can share on your portfolio, LinkedIn, or with recruiters, you need to deploy the application. The easiest and completely free method is using **Streamlit Community Cloud**.

Here is how you do it in 5 minutes:

## Step 1: Upload the Project to GitHub
1. Go to [GitHub](https://github.com/) and create a new repository (name it `ai-healthcare-system`).
2. Upload this entire `AI_Healthcare_System` folder to that repository.
   *(Make sure `app.py` and `requirements.txt` are in the main folder of the repo).*

## Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New App"**.
3. Select the `ai-healthcare-system` repository you just created.
4. Set the **Main file path** to `app.py`.
5. Click **"Deploy"**.

## Step 3: Get Your Live Link
Streamlit will read your `requirements.txt`, install Pyrebase4 and the Machine Learning models, and spin up a server.
Once it finishes baking (takes about 2-3 minutes), it will generate a live link like:
`https://ai-healthcare-system.streamlit.app`

That is it! Your application is now live, securely connected to your Firebase backend, and ready to impress!
