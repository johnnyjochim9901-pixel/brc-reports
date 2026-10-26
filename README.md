# BRC Work Reports - Streamlit App

A web-based tool for generating BRC HOURS and INSPECTIONS reports from CSV files.

## Features

- 📊 **Two Report Types**: BRC HOURS and INSPECTIONS
- 🎯 **Drag & Drop**: Easy file upload interface
- 📥 **Instant Download**: Get your formatted report in seconds
- 🌐 **Web-Based**: No installation needed for users
- 📱 **Works Anywhere**: Desktop, tablet, or mobile

## Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to: `http://localhost:8501`

## Deploy to Streamlit Cloud (FREE)

### Step 1: Create GitHub Repository

1. Go to https://github.com and create a new repository (e.g., "brc-reports")
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "Sign up" (use your GitHub account)
3. Click "New app"
4. Select your GitHub repository
5. Main file path: `app.py`
6. Click "Deploy"

That's it! Your app will be live at: `https://yourapp.streamlit.app`

### Step 3: Share with Colleagues

Send them the URL - they can:
1. Visit the link
2. Upload their CSV file
3. Choose report type
4. Download the result

No installation or setup needed!

## Report Details

### BRC HOURS Report
- Sorts by repair date
- Separates Vernon from other entries
- Calculates daily totals for labor and materials
- Shows grand totals

### INSPECTIONS Report
- Groups by date and ProdLine
- Blank ProdLine defaults to "LPG"
- Shows daily hours and totals per ProdLine
- Includes day summaries

## Support

For issues or questions, contact: [your-email@company.com]
