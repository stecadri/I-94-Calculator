import fitz
import pandas as pd
from datetime import datetime
import argparse
import re

def extract_i94_data(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    lines = text.split("\n")
    pattern_date = re.compile(r"\d{4}-\d{2}-\d{2}")
    entries = []
    
    for idx, line in enumerate(lines):
        if pattern_date.match(line.strip()):
            date = line.strip()
            type_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            location_line = lines[idx + 2].strip() if idx + 2 < len(lines) else ""
            
            if type_line.lower() in ['arrival', 'departure']:
                entries.append({
                    'Date': date,
                    'Type': type_line,
                    'Location': location_line
                })

    return pd.DataFrame(entries)

def calculate_stays(df, start_date):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    stays = []
    total_days = 0
    arrival_date = None

    df = df[df['Date'] >= pd.to_datetime(start_date)].reset_index(drop=True)

    for _, row in df.iterrows():
        if row['Type'].lower() == 'arrival':
            arrival_date = row['Date']
        elif row['Type'].lower() == 'departure' and arrival_date:
            departure_date = row['Date']
            days_stayed = (departure_date - arrival_date).days
            stays.append({
                'Arrival': arrival_date.date(),
                'Departure': departure_date.date(),
                'Days': days_stayed
            })
            total_days += days_stayed
            arrival_date = None

    # If still in US without recorded departure
    if arrival_date:
        days_stayed = (datetime.now() - arrival_date).days
        stays.append({
            'Arrival': arrival_date.date(),
            'Departure': 'Present',
            'Days': days_stayed
        })
        total_days += days_stayed

    return stays, total_days

#def display_timeline(stays, total_days):
#    print(f"{'Arrival':<12} {'Departure':<12} {'Days Stayed'}")
#    print('-' * 36)
#    for stay in stays:
#        print(f"{stay['Arrival']:<12} {stay['Departure']:<12} {stay['Days']}")
#    print('-' * 36)
#    print(f"Total days in the US: {total_days}")

def display_timeline(stays, total_days):
    print(f"{'Arrival':<12} {'Departure':<12} {'Days Stayed'}")
    print('-' * 36)
    for stay in stays:
        arrival_str = str(stay['Arrival'])
        departure_str = str(stay['Departure'])
        print(f"{arrival_str:<12} {departure_str:<12} {stay['Days']}")
    print('-' * 36)
    print(f"Total days in the US: {total_days}")

def main():
    parser = argparse.ArgumentParser(description='I-94 Travel History Timeline')
    parser.add_argument('pdf_file', help='Path to the PDF file')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')

    args = parser.parse_args()

    df = extract_i94_data(args.pdf_file)
    if df.empty:
        print("No data extracted. Check your PDF format.")
        return
    stays, total_days = calculate_stays(df, args.start_date)
    display_timeline(stays, total_days)

if __name__ == "__main__":
    main()

