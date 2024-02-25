# CVE Alert System

The CVE Alert System is a Python-based application designed to automate the monitoring and notification of Common Vulnerabilities and Exposures (CVEs) based on reports fetched from a specified API. It processes each report to extract CVE details and sends out alerts for each identified CVE.

## Features

- Fetching CVE reports from a REST API.
- Basic Authentication for secure API access.
- Processing and extracting detailed information from each CVE report.
- Sending formatted CVE alerts via a custom notification service.
- Avoiding duplicate notifications for already processed CVEs.

## Requirements

- Python 3.x
- requests library
- Access to a Unix-like command-line interface for curl commands

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine using:

    git clone <repository-url>

### Step 2: Install Dependencies

Navigate to the cloned repository's directory and install the required Python libraries:

    pip install -r requirements.txt

### Step 3: Configuration

Edit the script to include your specific API endpoints, authentication credentials, and other configurations:

- Replace http://<server-ip>:8000/api and http://<server-ip>/restAPI with your actual API and notification endpoints.
- Replace <username> and <password> with your actual authentication credentials.

Ensure that these sensitive details are securely stored and not hard-coded in the script for production environments.

## Usage

To run the CVE Alert System, execute the script from your command-line interface:

    python cve_alert_system.py

The script will automatically:

1. Fetch the list of CVE reports from the configured API endpoint.
2. Process each report to extract and format CVE details.
3. Send out a notification for each CVE, ensuring no duplicates are sent.

<img width="513" alt="image" src="https://github.com/praxxley-tech/openCEV/assets/82277204/f1541fa0-0f79-42d7-8868-cc994efd2cc3">

### Alert Format

Notifications are sent with the following format:

🚨 CVE Alert: CVE-XXXX-XXXX 🚨
Title: <Title of the CVE>
ID: <Report ID>
CVE: <CVE ID>
Score: <CVSS Score>
Summary: <CVE Summary>

<img width="516" alt="image" src="https://github.com/praxxley-tech/openCEV/assets/82277204/eb2d482f-4036-4deb-9217-c81c0ec7e8b8">

## Security and Privacy

Ensure to handle authentication credentials and sensitive information with care:

- Avoid hard-coding credentials directly in the script.
- Use environment variables or secure vaults to manage sensitive information.
- Regularly update and rotate credentials.

## Troubleshooting

- Ensure all dependencies are correctly installed and up-to-date.
- Verify network connectivity to the specified API and notification endpoints.
- Check for correct authentication credentials and endpoint configurations.
- For detailed error logs, consider implementing logging within the script.

## Contributing

Contributions to the CVE Alert System are welcome. If you have suggestions for improving this system, please follow the steps below:

1. **Fork the Repository**: Navigate to the original repository, and use the 'Fork' button to create your own copy of the project to your account.
2. **Create Your Feature Branch**: From your forked repository, execute `git checkout -b feature/YourAmazingFeature` in your terminal to create a new branch for your contributions.
3. **Commit Your Changes**: After making your changes, commit them with a clear and concise commit message using `git commit -m 'Add some YourAmazingFeature'`.
4. **Push to the Branch**: Upload your changes to your repository with `git push origin feature/YourAmazingFeature`.
5. **Open a Pull Request**: On your forked repository on GitHub, select your 'feature' branch and click on 'Pull Request'. Fill in some details about your changes and submit the request for review.

Your contributions will be reviewed as soon as possible. We appreciate your effort to enhance the functionality and performance of the CVE Alert System!

## Contact

For any questions or concerns regarding this project, or if you need support, please reach out to the repository owner.

Thank you for considering contributing to the CVE Alert System. Your effort to improve this tool is greatly appreciated!
