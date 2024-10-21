# Django Project - API and Registration Form

## Project Overview
This project is a Django-based application that consists of:
1. A RESTful API to handle user registrations and allow checking and updating of registration information.
2. A web-based registration form to submit user data.
The project is built to demonstrate handling HTTP requests without using Django REST Framework (DRF) and includes rate limiting, validation, logging, and basic error handling. It also provides a straightforward way to test the user registration functionality using a web form.

## Requirements
- Python 3.8+
- Django 4.0+
- Virtual environment (optional but recommended)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/BlacAc3/novaji_assessment
   cd novaji_assessment
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

## How to Access and Test the Application

### 1. RESTful API (Question 3 from the Test)

The RESTful API has three endpoints:
base url = `127.0.0.1/api` or `localhost:8000/api`

- **POST `/register`**: Register a new user with the following parameters:
  - `phone_number`: User's phone number.
  - `mobile_network`: The network provider (e.g., MTN, Airtel, 9mobile, Glo).
  - `message`: A message to be stored with the registration.
  - `ref_code`: A unique, alphanumeric reference code (minimum 16 characters).
  
  Example:
  ```bash
  curl -X POST http://127.0.0.1:8000/register -H "Content-Type: application/json" -d '{
      "phone_number": "1234567890",
      "mobile_network": "MTN",
      "message": "Test registration",
      "ref_code": "ABC123XYZ4567890"
  }'
  ```

- **GET `/status/<ref_code>`**: Retrieve the status of a registration using the `ref_code`.

  Example:
  ```bash
  curl http://127.0.0.1:8000/status/ABC123XYZ4567890
  ```

- **PUT `/update/<ref_code>`**: Update the `message` field of an existing registration.

  Example:
  ```bash
  curl -X PUT http://127.0.0.1:8000/update/ABC123XYZ4567890 -H "Content-Type: application/json" -d '{
      "message": "Updated registration message"
  }'
  ```

### Location of API Code:
The implementation of the API can be found in the following files:
- **`api/views.py`**: Contains the logic for handling the POST, GET, and PUT requests.
- **`api/urls.py`**: Defines the URL routes for the API endpoints.
- **`novaji_asessment/urls.py`**: Main URL configuration that includes the `api` app routes.

### 2. Registration Form (Question 2 from the Test)

The project also includes a basic registration form that allows users to submit the required details as a test. The form takes the same parameters as the API endpoint and sends them via a POST request.

**To access the form:**
- Navigate to `http://127.0.0.1:8000/` in your web browser.

**Fields in the Form:**
- **Phone Number**: A field to input the user’s phone number.
- **Mobile Network**: Dropdown selection of available network providers.
- **Message**: Text input for a custom message.
- **Reference Code**: A text field for a unique, alphanumeric reference code (minimum of 16 characters).

### Location of Registration Form Code:
The code for the form can be found in the following files:
- **`api/views.py`**: Logic to handle the form submission.
- **`api/forms.py`**: Defines the Django form used in the web page.

### Additional Features
- **Rate Limiting**: Limits the number of requests per minute to prevent abuse.
- **Logging**: All requests and responses are logged for monitoring purposes.
- **Validation**: Ensures that inputs are correctly formatted and follow the required rules.

## Running app
To run project, use:
```bash
python manage.py runserver
```

## Conclusion
This project demonstrates how to create a RESTful API in Django without using Django REST Framework and implement a basic web form for testing the registration functionality. It includes essential features like rate limiting, input validation, and logging to enhance the usability and security of the application.

Feel free to explore the code and adapt it for your use cases!
```

### Explanation:
- **Setup Instructions**: Provides a step-by-step guide to set up and run the Django application.
- **API Details**: Explains how to interact with the RESTful API endpoints, along with example `curl` commands.
- **Registration Form**: Guides users on how to access the web-based registration form.
- **File Locations**: Clearly states where each part of the implementation can be found in the project directory, making it easier for anyone reviewing the code to understand the structure.
- **Additional Features**: Highlights key features added to the project like rate limiting and logging.
