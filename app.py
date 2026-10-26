import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="BRC Work Reports",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #C8853F;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #8A8A80;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">BRC Work Reports</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Generate professional reports from your CSV data</div>', unsafe_allow_html=True)

# Report type selection
report_type = st.radio(
    "Select Report Type",
    ["BRC HOURS Report", "INSPECTIONS Report"],
    horizontal=True
)

# File upload
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=['csv'],
    help="Drag and drop or click to browse"
)

def generate_brc_hours_report(df):
    """Generate BRC HOURS report"""
    output = io.StringIO()

    # Group by Repair Date
    df['Repair Date'] = pd.to_datetime(df['Repair Date'], errors='coerce')
    df = df.dropna(subset=['Complete Date'])
    df = df.sort_values('Repair Date')

    # Process daily data
    daily_data = {}

    for _, row in df.iterrows():
        repair_date = row['Repair Date'].strftime('%Y-%m-%d') if pd.notna(row['Repair Date']) else 'No Date'

        if repair_date not in daily_data:
            daily_data[repair_date] = {
                'vernon': [],
                'other': [],
                'vernon_total_hours': 0,
                'vernon_labor': 0,
                'vernon_material': 0,
                'other_total_hours': 0,
                'other_labor': 0,
                'other_material': 0
            }

        # Calculate totals
        sell_hours = float(row.get('Sell Hours', 0) or 0)
        quantity = float(row.get('Quantity', 0) or 0)
        total_hours = sell_hours * quantity
        labor = float(row.get('Labor Quote $', 0) or 0)
        material = float(row.get('Material Quote $', 0) or 0)

        entry = {
            'Location': row.get('Location', ''),
            'Car Mark': row.get('Car Mark', ''),
            'Car Number': row.get('Car Number', ''),
            'Requested By': row.get('Requested By', ''),
            'Job Description': row.get('Job Description', ''),
            'Sell Hours': sell_hours,
            'Quantity': quantity,
            'total_hours': total_hours,
            'Labor Quote $': labor,
            'Material Quote $': material
        }

        # Separate Vernon from others
        requested_by = str(row.get('Requested By', '')).strip().lower()
        if 'vernon' in requested_by:
            daily_data[repair_date]['vernon'].append(entry)
            daily_data[repair_date]['vernon_total_hours'] += total_hours
            daily_data[repair_date]['vernon_labor'] += labor
            daily_data[repair_date]['vernon_material'] += material
        else:
            daily_data[repair_date]['other'].append(entry)
            daily_data[repair_date]['other_total_hours'] += total_hours
            daily_data[repair_date]['other_labor'] += labor
            daily_data[repair_date]['other_material'] += material

    # Write report
    output.write("BRC HOURS REPORT\n")
    output.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("=" * 50 + "\n\n")

    for date in sorted(daily_data.keys()):
        day_data = daily_data[date]
        output.write(f"DATE: {date}\n\n")

        # Vernon entries
        if day_data['vernon']:
            output.write("VERNON ENTRIES\n")
            output.write("Location,Car Mark,Car Number,Requested By,Job Description,Sell Hours,Quantity,Total Sell Hours,Labor Quote $,Material Quote $\n")

            for entry in day_data['vernon']:
                output.write(f"{entry['Location']},{entry['Car Mark']},{entry['Car Number']},{entry['Requested By']},{entry['Job Description']},{entry['Sell Hours']},{entry['Quantity']},{entry['total_hours']:.2f},{entry['Labor Quote $']},{entry['Material Quote $']}\n")

            output.write("\n")
            output.write(f"VERNON DAY TOTALS:,,,,,,,{day_data['vernon_total_hours']:.2f},{day_data['vernon_labor']:.2f},{day_data['vernon_material']:.2f}\n\n")

        # Other entries
        if day_data['other']:
            output.write("OTHER ENTRIES\n")
            output.write("Location,Car Mark,Car Number,Requested By,Job Description,Sell Hours,Quantity,Total Sell Hours,Labor Quote $,Material Quote $\n")

            for entry in day_data['other']:
                output.write(f"{entry['Location']},{entry['Car Mark']},{entry['Car Number']},{entry['Requested By']},{entry['Job Description']},{entry['Sell Hours']},{entry['Quantity']},{entry['total_hours']:.2f},{entry['Labor Quote $']},{entry['Material Quote $']}\n")

            output.write("\n")
            output.write(f"OTHER DAY TOTALS:,,,,,,,{day_data['other_total_hours']:.2f},{day_data['other_labor']:.2f},{day_data['other_material']:.2f}\n\n")

        # Day summary
        total_hours = day_data['vernon_total_hours'] + day_data['other_total_hours']
        total_labor = day_data['vernon_labor'] + day_data['other_labor']
        total_material = day_data['vernon_material'] + day_data['other_material']

        output.write("DAY SUMMARY:\n")
        output.write(f"Total Sell Hours (All):,{total_hours:.2f}\n")
        output.write(f"Total Labor Quote (All):,{total_labor:.2f}\n")
        output.write(f"Total Material Quote (All):,{total_material:.2f}\n\n")
        output.write("=" * 50 + "\n\n")

    return output.getvalue()


def generate_inspections_report(df):
    """Generate INSPECTIONS report"""
    output = io.StringIO()

    # Parse dates and group by date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.sort_values('Date')

    # Replace blank ProdLine with LPG
    df['ProdLine'] = df['ProdLine'].fillna('LPG')
    df.loc[df['ProdLine'].str.strip() == '', 'ProdLine'] = 'LPG'

    # Group data
    daily_data = {}

    for _, row in df.iterrows():
        date = row['Date'].strftime('%Y-%m-%d')
        prodline = row['ProdLine']

        if date not in daily_data:
            daily_data[date] = {}

        if prodline not in daily_data[date]:
            daily_data[date][prodline] = []

        daily_data[date][prodline].append({
            'Location': row.get('Location', ''),
            'Mark': row.get('Mark', ''),
            'Number': row.get('Number', ''),
            'CusNumber': row.get('CusNumber', ''),
            'CusContract': row.get('CusContract', ''),
            'Hours': float(row.get('Hours', 0) or 0),
            'Total': float(row.get('Total', 0) or 0),
            'Currency': row.get('Currency', '')
        })

    # Write report
    output.write("INSPECTIONS REPORT\n")
    output.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("=" * 50 + "\n\n")

    for date in sorted(daily_data.keys()):
        output.write(f"DATE: {date}\n\n")

        date_total_hours = 0
        date_total_amount = 0

        for prodline in sorted(daily_data[date].keys()):
            entries = daily_data[date][prodline]

            output.write(f"PRODLINE: {prodline}\n")
            output.write("Location,Mark,Number,CusNumber,CusContract,Hours,Total,Currency\n")

            prodline_hours = 0
            prodline_total = 0

            for entry in entries:
                output.write(f"{entry['Location']},{entry['Mark']},{entry['Number']},{entry['CusNumber']},{entry['CusContract']},{entry['Hours']:.2f},{entry['Total']:.2f},{entry['Currency']}\n")
                prodline_hours += entry['Hours']
                prodline_total += entry['Total']

            output.write("\n")
            output.write(f"{prodline} TOTALS:,,,,,{prodline_hours:.2f},{prodline_total:.2f},\n\n")

            date_total_hours += prodline_hours
            date_total_amount += prodline_total

        # Day totals
        output.write("DAY TOTALS:\n")
        output.write(f"Total Hours:,{date_total_hours:.2f}\n")
        output.write(f"Total Amount:,{date_total_amount:.2f}\n\n")
        output.write("=" * 50 + "\n\n")

    return output.getvalue()


if uploaded_file is not None:
    try:
        # Read the CSV
        df = pd.read_csv(uploaded_file)

        st.success(f"✅ File loaded: {uploaded_file.name}")

        with st.expander("Preview Data"):
            st.dataframe(df.head(10))

        # Generate button
        if st.button("📊 Generate Report", type="primary", use_container_width=True):
            if report_type == "BRC HOURS Report":
                output = generate_brc_hours_report(df)
                filename = "BRC_HOURS_REPORT.csv"
            else:
                output = generate_inspections_report(df)
                filename = "INSPECTIONS_REPORT.csv"

            st.success("✅ Report generated successfully!")

            st.download_button(
                label="⬇️ Download Report",
                data=output,
                file_name=filename,
                mime="text/csv",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
