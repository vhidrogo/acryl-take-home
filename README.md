# acryl-take-home
Acryl Data take-home exercise for Software Engineer role

## Overview
This project is a Django application that connects to a Snowflake instance to fetch information about schemas, tables, and columns.

## Requirements
- Python 3.x
- Django
- Snowflake Connector for Python
- Django REST Framework

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/acryl-take-home.git
   cd acryl-take-home
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the `acryl_take_home/` directory with the following content:
   ```env
   SNOWFLAKE_ACCOUNT_ID=<your_account_id>
   SNOWFLAKE_USER=<your_user>
   SNOWFLAKE_PASSWORD=<your_password>
   SNOWFLAKE_ROLE=<your_role>
   SNOWFLAKE_WAREHOUSE=<your_warehouse>
   SNOWFLAKE_DATABASE=<your_database>
   ```

5. **Run the Django server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the API**:
   You can access the API at `http://127.0.0.1:8000/api/schemas/` to list the schemas.

## Reflection

- **Time Spent**: I spent approximately 4 hours on this take-home exercise, including setup, coding, and testing.
  
- **What Went Well**: One aspect that went well was setting up the connection to the Snowflake database and successfully fetching the schema and table information. The integration with Django was straightforward, allowing for quick implementation of the required endpoints.

- **Improvements**: If I had more time, I would focus on writing unit tests for the API endpoints to ensure they function correctly under various scenarios. Also, I would implement a more efficient data retrieval mechanism for handling large tables. The current solution may run into memory issues when fetching large datasets. A better approach would be to use generators to avoid loading the entire dataset into memory at once, thus improving scalability and ensuring the API can handle very large tables without running out of memory. Additionally, I would like to improve error handling and validation for the input parameters to enhance the robustness of the API.
