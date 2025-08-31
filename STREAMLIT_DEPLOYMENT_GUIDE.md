#  Complete Guide: Upload to Streamlit Cloud

## Prerequisites

### 1. Install Git
Download and install Git from: https://git-scm.com/download/win
- Run the installer
- Use default settings
- Restart your terminal after installation

### 2. Create GitHub Account
- Go to https://github.com
- Sign up for a free account
- Verify your email

### 3. Install Python (if not already installed)
- Download from https://python.org
- Make sure to check "Add Python to PATH" during installation

## Step-by-Step Deployment

### Step 1: Initialize Git Repository
```bash
# Navigate to your project directory
cd "D:\Cursor\argentine-adr-portfolio"

# Initialize Git repository
git init

# Add all files to Git
git add .

# Make initial commit
git commit -m "Initial Argentine ADR Portfolio Analysis"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name it: `argentine-adr-portfolio`
4. Make it Public
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### Step 3: Connect and Push to GitHub
```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/argentine-adr-portfolio.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the details:
   - Repository: `YOUR_USERNAME/argentine-adr-portfolio`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy"

## Alternative: Manual Upload

If you prefer not to use Git, you can:

### Option 1: GitHub Web Interface
1. Go to your GitHub repository
2. Click "Add file"  "Upload files"
3. Drag and drop all project files
4. Commit the changes

### Option 2: GitHub Desktop
1. Download GitHub Desktop: https://desktop.github.com
2. Clone your repository
3. Copy project files to the repository folder
4. Commit and push through GitHub Desktop

## Project Files Structure
Your project should have these files:
```
argentine-adr-portfolio/
 app.py                 # Main application
 requirements.txt       # Dependencies
 README.md             # Documentation
 DEPLOYMENT.md         # This guide
 .gitignore           # Git ignore file
 .streamlit/
    config.toml      # Streamlit configuration
 data/
    __init__.py
 components/
    __init__.py
 utils/
    __init__.py
 assets/
```

## Troubleshooting

### Common Issues:
1. **Git not found**: Install Git from git-scm.com
2. **Python not found**: Install Python and add to PATH
3. **Authentication error**: Use GitHub token or SSH keys
4. **Deployment fails**: Check requirements.txt and app.py syntax

### Streamlit Cloud Issues:
1. **App not loading**: Check the logs in Streamlit Cloud
2. **Dependencies missing**: Verify requirements.txt
3. **Import errors**: Check all imports in app.py

## Success Indicators
 Repository created on GitHub
 Code pushed successfully
 Streamlit Cloud deployment started
 App accessible via public URL
 All features working (load ADRs, analysis tabs)

## Support
- GitHub Help: https://help.github.com
- Streamlit Documentation: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io

Your app will be available at: https://YOUR_USERNAME-argentine-adr-portfolio-app-XXXX.streamlit.app
