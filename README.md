# AI Feedback System

A dual-dashboard application for collecting and analyzing user feedback using Python, Streamlit, and Google Gemini.

## Components

1.  **User Dashboard**: Public-facing form for feedback ratings and reviews. Interactive AI response.
2.  **Admin Dashboard**: Internal-facing analytics and list view of submissions with AI-generated summaries and recommendations.

## Setup Locally

1.  **Clone the repository** (or navigate to the folder).
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Key**:
    - Create a `.env` file in the root directory.
    - Add your Gemini API Key: `GEMINI_API_KEY=AIzaSy...`
4.  **Run the App**:
    ```bash
    streamlit run User_Dashboard.py
    ```
5.  **Access**:
    - User Dashboard: `http://localhost:8501/`
    - Admin Dashboard: Click "Admin Dashboard" in the sidebar or go to `http://localhost:8501/Admin_Dashboard`

## Deployment Architecture

### Why PostgreSQL + Separate Deployments?
- **PostgreSQL**: Enables both dashboards to share the same database (SQLite can't do this across instances)
- **Separate Deployments**: Independent apps allow different access levels and better scalability

### Deployment Stack
- **Database**: PostgreSQL (Render.com or Railway.app - free tier)
- **User Dashboard**: Streamlit Cloud (public URL)
- **Admin Dashboard**: Streamlit Cloud (separate app, keep URL private)
- **LLM**: Google Gemini API

## Live Deployment

**User Dashboard**: https://fyndtask2-brjhm3ynnooy8eidvwixg5.streamlit.app/

**Admin Dashboard**: https://fyndtask2-qesk8gauyybwew2kgtqn9g.streamlit.app/

## Deployment on Streamlit Community Cloud

### Step 1: Set Up PostgreSQL Database
1. Visit [Render.com](https://render.com) or [Railway.app](https://railway.app)
2. Create a new PostgreSQL database (free tier available)
3. Copy the connection string (DATABASE_URL)
4. Keep this safe - you'll add it to Streamlit secrets

### Step 2: Push Code to GitHub
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Step 3: Deploy User Dashboard
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click **New App**
3. Select your repository
4. Set **Main file path** to `User_Dashboard.py`
5. Click **Advanced Settings** → Add Secrets:
   - `GEMINI_API_KEY` = your_actual_api_key
   - `DATABASE_URL` = postgresql://user:password@host/dbname
6. Click **Deploy** → Wait 2-3 minutes

### Step 4: Deploy Admin Dashboard (Separate App)
1. Click **New App** again
2. Select same repository
3. Set **Main file path** to `pages/Admin_Dashboard.py`
4. Add same Secrets (both apps must connect to same database)
5. Click **Deploy**

### Final URLs
Once deployed, you'll have:
- **User Dashboard**: https://fyndtask2-brjhm3ynnooy8eidvwixg5.streamlit.app/ (share publicly)
- **Admin Dashboard**: https://fyndtask2-qesk8gauyybwew2kgtqn9g.streamlit.app/ (keep private)

## Project Structure
- `User_Dashboard.py`: Main entry point (User UI).
- `pages/Admin_Dashboard.py`: Admin UI.
- `src/database.py`: SQLite handler.
- `src/llm.py`: Google Gemini handler.
- `feedback.db`: Local SQLite database (Not synced to git by default, but will be created on runtime). *Note: For persistent cloud storage, consider connecting to Google Sheets or a cloud DB, as Streamlit Cloud is ephemeral.*
