from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load financial data
data = pd.read_csv('financial_data.csv')

@app.route('/')
def home():
    return render_template('index.html', query=None, response=None)

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['query']
    
    # Check for matching financial data based on the query
    response = lookup_financial_data(query)
    
    return render_template('index.html', query=query, response=response)

# List of metrics
metrics = [
    "Total Revenue",
    "Net Income",
    "Total Assets",
    "Total Liabilities",
    "Cash Flow from Operating Activities"
]

# List of companies
companies = data['company'].unique().tolist()

# List of keywords for query parsing
query_keywords = {
    "total revenue": "Total Revenue",
    "net income": "Net Income",
    "total assets": "Total Assets",
    "total liabilities": "Total Liabilities",
    "cash flow from operating activities": "Cash Flow from Operating Activities"
}

def lookup_financial_data(query):
    # Normalize the query to lower case for easier matching
    query = query.lower().strip()  # Ensure there's no leading/trailing whitespace
    parts = query.split()
    company = None
    year = None
    financial_metric = None

    # Identify the company and year from the query
    for part in parts:
        # Check if part matches any company name (case insensitive)
        if part in data['company'].str.lower().values:
            company = data.loc[data['company'].str.lower() == part, 'company'].values[0]
        if part.isdigit() and len(part) == 4:  # Check if it's a year
            year = part

    # Determine the financial metric based on the query
    for keyword, metric in query_keywords.items():
        if keyword in query:
            financial_metric = metric
            break

    # Debug print statements to check values
    print(f"Query: {query}")
    print(f"Identified company: {company}")
    print(f"Identified year: {year}")
    print(f"Identified metric: {financial_metric}")

    # Look up the value in the DataFrame
    if company and year and financial_metric:
        try:
            value = data.loc[
                (data['company'] == company) & 
                (data['fiscal year'] == int(year)), 
                financial_metric
            ].values[0]
            return f"{financial_metric} of {company} in {year} is {value}."
        except IndexError:
            return "Sorry, I couldn't find that information."
    
    return "Please provide a valid query."


if __name__ == "__main__":
    app.run(debug=True)