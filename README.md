# I-94-Calculator
Calculates the days spent in the United States provided an I-94 travel history PDF file obtained at https://i94.cbp.dhs.gov/search/history-search/

## How to use
`python tool.py <file.pdf> <start_date>`

for example:
`python tool.py travel_history.pdf 2023-01-01`

## Requirements
PyMuPDF==1.24.0
pandas==2.2.1
python-dateutil==2.9.0.post0
