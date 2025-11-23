# AI SQL Query Generator

A Streamlit-based application that converts natural language questions into SQL queries using Google's Gemini AI, with built-in security features and sensitive data filtering.

## Features

- 🤖 Natural language to SQL conversion using Gemini AI
- 🔒 SQL injection protection with safety validation
- 🛡️ Automatic filtering of sensitive columns (IDs, passwords, audit fields)
- 💾 SQL Server integration with Windows Authentication support
- ⚡ Real-time query execution with loading states
- 🎯 MVC architecture for clean code organization

## Prerequisites

- Python 3.10+
- SQL Server with ODBC Driver 17
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd texttosql
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirement.txt
```

4. Configure environment variables:
Create a `.env` file with:
```env
SQL_SERVER=your_server_name
SQL_DATABASE=your_database_name
SQL_USERNAME=
SQL_PASSWORD=
GOOGLE_API_KEY=your_gemini_api_key
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Project Structure

```
texttosql/
├── app.py                      # Main Streamlit application
├── controllers/
│   └── query_controller.py    # Query processing logic
├── models/
│   └── db.py                   # Database connection
├── services/
│   ├── ai_service.py          # Gemini AI integration
│   ├── sql_safety.py          # SQL injection protection
│   └── column_filter.py       # Sensitive data filtering
├── requirement.txt            # Python dependencies
└── .env                       # Environment configuration
```

## Security Features

- **SQL Injection Prevention**: Blocks dangerous SQL operations (DROP, DELETE, TRUNCATE, etc.)
- **Column Filtering**: Automatically hides sensitive columns from results
- **AI Guardrails**: Instructs AI to avoid requesting sensitive data

## License

MIT
