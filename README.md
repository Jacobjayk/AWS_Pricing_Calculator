# 🌩️ Cloud Cost Calculator

## 📌 Overview
The **Cloud Cost Calculator** is a web-based tool that helps users estimate the cost of using various AWS services. The calculator supports multiple AWS services like EC2 and S3, allowing users to input usage details and receive an estimated cost based on current AWS pricing.

## 🚀 Features
- Estimate costs for AWS services like EC2 and S3
- Simple web interface using Flask
- Fetches real-time AWS pricing data via the AWS Pricing API
- Deployed on AWS Elastic Beanstalk

## 🛠️ Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **AWS Services:** AWS Pricing API, Elastic Beanstalk
- **Other Tools:** AWS CLI, Boto3 (AWS SDK for Python)

## 📖 How It Works
1. The user selects an AWS service (e.g., EC2 or S3).
2. The user enters their expected usage (e.g., hours for EC2, GB for S3).
3. The app calculates the estimated cost based on AWS pricing data.
4. The result is displayed on the screen.

## 🏗️ Installation & Setup

### Prerequisites
- Python 3.7+
- AWS CLI installed and configured (`aws configure`)
- Virtual environment (recommended)

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Jacobjayk/AWS_Pricing_Calculator.git
   cd cloud-cost-calculator
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Generate your secret key by running the `secret.py` file:
   ```bash
   python secret.py
   ```
   This will generate a secret key that you need to add to your `.env` file.

5. Open the `.env` file and manually update it with your AWS credentials:
   ```
   SECRET_KEY=your_generated_secret_key
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   ```
   > **Note:** The `.env` file is empty by default. You must add these credentials manually. Ensure that your AWS credentials have the required permissions to access the AWS Pricing API.
  
6. Run the Flask app:
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000/` in your browser.

## 🚀 Deployment on AWS Elastic Beanstalk
1. Install the Elastic Beanstalk CLI:
   ```bash
   pip install awsebcli --upgrade
   ```
2. Initialize Elastic Beanstalk:
   ```bash
   eb init
   ```
3. Create and deploy the app:
   ```bash
   eb create cloud-cost-calculator
   eb open
   ```

## 📸 Screenshots
- **Application Interface:** ![Application Interface](https://github.com/user-attachments/assets/4fbd8669-a9f2-4138-a97d-949baa4b88a5)
- **Cost Calculation Example:** ![Cost Calculation](https://github.com/user-attachments/assets/4c693b73-bc04-4f1a-a1cc-5649fe48edf2)
- **Cost Details:** ![Cost Details](https://github.com/user-attachments/assets/f05f429a-809f-40a2-a7b4-6e802c42703f)

> *If the images do not load, ensure the repository has public access or replace the links with direct GitHub-hosted images.*

## 📝 Future Enhancements
- Support more AWS services
- Add multi-region pricing comparisons
- Enhance security with user authentication and session management.

## 📩 Contact
Feel free to reach out if you have any questions or suggestions:
- **Email:** jacobakotuah@gmail.com
- **LinkedIn:** [Jacob Akotuah](https://www.linkedin.com/in/jacobakotuah)
- **GitHub:** [Jacobjayk](https://github.com/Jacobjayk)

For issues or contributions, feel free to open a GitHub issue or pull request.

---

### 📢 If you like this project, don't forget to ⭐ star the repository!
