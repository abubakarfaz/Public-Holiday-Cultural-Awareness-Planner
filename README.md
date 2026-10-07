# Public Holiday & Cultural Awareness Planner

A Python-based project for exploring public holidays, saving favourite countries, and storing holiday guides for cultural awareness and planning.

## Overview

This application is designed to help users:

- track favourite countries
- view or save holiday information by year
- keep local holiday guides for offline viewing
- support future cultural-awareness insights tied to public holidays

The project currently includes a data-persistence layer for favourites and saved holiday guides, plus tests covering the core functionality.

## Features

- Favourite country management
- Duplicate prevention for saved favourites
- Holiday guide saving and retrieval
- Local JSON storage for data persistence
- Unit tests for favourites and guide storage

## Tech Stack

- Python 3
- Streamlit
- Requests
- Python-dotenv
- unittest

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── data/
│   ├── README.md
│   ├── favourites.json
│   └── saved_guides.json
├── modules/
│   ├── __init__.py
│   ├── comparison.py
│   ├── culture_guide.py
│   ├── date_utils.py
│   ├── favourites.py
│   ├── holiday_api.py
│   ├── README.md
│   ├── validation.py
│   └── __pycache__/
├── tests/
│   ├── __init__.py
│   ├── README.md
│   └── favourites_test.py
└── venv/
```

## Installation

1. Clone the repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

This project uses Streamlit, so the app can be started with:

```bash
streamlit run app.py
```

If the app is still being developed and `app.py` only contains placeholder logic, you can still use the project’s data and module structure as the foundation for the Streamlit interface.

## Running Tests

```bash
python -m unittest discover -s tests
```

## Data Storage

The following files are used to persist user preferences and saved guides:

- `data/favourites.json`
- `data/saved_guides.json`

These files are created automatically when the app or storage manager is used.

## Notes

The project is structured around a modular design, with functionality split into separate Python modules for:

- holiday data retrieval
- guide generation
- validation
- date handling
- comparisons
- saved favourites

## Future Improvements

Potential extensions include:

- a full UI for searching countries and holidays
- AI-generated cultural explanations
- filtering by region, month, or holiday type
- export and sharing of saved guides

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, consider adding an appropriate license.
