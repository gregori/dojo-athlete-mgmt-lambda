# Dojo Athlete Management Lambda

This repository contains the AWS Lambda function for managing athletes in an Aikido dojo. The Lambda function handles
various operations related to athlete registration, profile management, enrollment, payments, and attendance tracking.

## Overview

The Dojo Athlete Management Lambda is designed to streamline the management of athletes in an Aikido dojo. It provides
functionalities for registering new athletes, updating their profiles, managing enrollments and payments, and tracking
attendance.

## Functional Requirements

### Athlete Management

- **Registration**:
    - Register new athletes with personal data (CPF, RG, name, address, email, phone).
    - Assign a unique registration number. The registration number is sequential and ends with the year of registration
      plus a dojo indicator.
- **Profile Management**:
    - Update personal data of athletes.
    - Track athletes' medical certificates and ensure they are up to date.
- **Enrollment and Payments**:
    - Manage athlete enrollments and monthly fees based on the number of training sessions per week.
    - Monitor payment of monthly fees and prevent athletes with outstanding debts from taking belt exams.
- **Attendance**:
    - Implement a barcode check-in system for training sessions.
    - Validate check-ins according to the athlete's enrollment and training schedule.

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/dojo-athlete-management-lambda.git
    cd dojo-athlete-management-lambda
    ```

2. **Install dependencies**:
    ```sh
    pip install -r app/requirements.txt
    ```

3. **Deploy the Lambda function using GitHub Actions**:
    - Ensure you have a `.github/workflows/deploy.yml` file with the following content:
    ```yaml
    name: Deploy Lambda

    on:
      push:
        branches:
          - main

    jobs:
      deploy:
        runs-on: ubuntu-latest

        steps:
        - name: Checkout code
          uses: actions/checkout@v2

        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: '3.8'

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r app/requirements.txt

        - name: Deploy to AWS Lambda
          env:
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            AWS_REGION: 'us-east-1'
          run: |
            zip -r lambda_function.zip .
            aws lambda update-function-code --function-name dojo-athlete-management --zip-file fileb://lambda_function.zip
    ```

## Usage

### Registering a New Athlete

To register a new athlete, send a POST request to the `/register` endpoint with the athlete's personal data.

### Updating Athlete Profile

To update an athlete's profile, send a PUT request to the `/update-profile` endpoint with the updated personal data.

### Managing Enrollments and Payments

To manage enrollments and payments, send a POST request to the `/enroll` endpoint with the enrollment details and a POST
request to the `/payment` endpoint with the payment details.

### Tracking Attendance

To track attendance, send a POST request to the `/checkin` endpoint with the athlete's barcode data.

## API Endpoints

- `POST /register`: Register a new athlete.
- `PUT /update-profile`: Update an athlete's profile.
- `POST /enroll`: Manage athlete enrollments.
- `POST /payment`: Manage athlete payments.
- `POST /checkin`: Track athlete attendance.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.