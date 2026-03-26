
# ☁️ AWS EBS Snapshot Cleanup & Cost Optimization

An automated, serverless utility designed to optimize AWS cloud storage costs by identifying and deleting stale Amazon Elastic Block Store (EBS) snapshots. 

By leveraging AWS Lambda and CloudWatch Events, this tool ensures continuous cost reduction by automatically purging snapshots that are no longer associated with active EC2 instances. The entire infrastructure is managed as code (IaC) using Terraform for easy and reproducible deployments.

## 🚀 Key Features

- **Automated Cost Optimization:** Reduces continuous cloud storage costs by seamlessly removing orphaned and unused EBS snapshots.
- **Serverless Architecture:** Engineered using Python and Boto3 on AWS Lambda, requiring zero server maintenance.
- **Scheduled Execution:** Driven by Amazon CloudWatch Events (EventBridge) to run automated daily cleanups.
- **Infrastructure as Code (IaC):** Fully automated resource provisioning, including IAM roles and Lambda configurations, using Terraform.

## 🛠️ Tech Stack

* **Cloud Provider:** AWS
* **Compute:** AWS Lambda (Serverless)
* **Automation & Scheduling:** Amazon CloudWatch Events / EventBridge
* **Language/SDK:** Python 3.8, Boto3
* **Infrastructure as Code:** Terraform

## ⚙️ How It Works

1. **Trigger:** A scheduled CloudWatch Event triggers the Lambda function daily.
2. **Discover:** The function fetches all EBS snapshots owned by the AWS account and retrieves a list of all active EC2 instances (both running and stopped).
3. **Evaluate:** For each snapshot, the script validates whether the associated original volume is currently attached to any active instance.
4. **Action:** If a snapshot is deemed "stale" (its parent volume is deleted or no longer in use), the function deletes the snapshot.

## 📂 Repository Structure

```text
aws-ebs-snapshot-cleanup/
│
├── lambda_function/                # Contains the AWS Lambda function code
│   └── lambda_function.py          # Python script for the Lambda function
│
├── infrastructure/                 # Contains infrastructure configuration files
│   ├── lambda_iam_role.json        # IAM role policy for the Lambda function
│   ├── cloudwatch_event_rule.json  # CloudWatch Event rule configuration
│   └── terraform/                  # Terraform configuration files
│       ├── main.tf                 # Main Terraform configuration
│       ├── variables.tf            # Terraform input variables
│       └── outputs.tf              # Terraform output values
│
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies for the Lambda function
```


## 📋 Prerequisites
Before deploying the project, ensure you have the following:
- **AWS Account**: With permissions to create Lambda functions, IAM roles, and CloudWatch Events.
- **AWS CLI**: Installed and configured with your credentials.
- **Python 3.8+**: Installed on your local machine(for testing the Lambda function).
- **Terraform**: Installed to automate infrastructure deployment.

## Deployment Steps
  1. Clone the Repository
```bash
git clone https://github.com/imssp/aws-ebs-snapshot-cleanup.git
cd aws-ebs-snapshot-cleanup
```

2. Prepare the Lambda Function

      Install the required Python libraries locally to package them with your code:

    ```bash
    pip install -r requirements.txt
    ```
      Zip the Lambda function code and its dependencies:

    ```bash
    cd lambda_function
    zip -r ../lambda_function_payload.zip .
    cd ..
    ```
3. Deploy Infrastructure via Terraform
    
    Navigate to the Terraform directory:
    ```bash
    cd infrastructure/terraform
    ```     
    
    Initialize the Terraform backend and provider plugins:
    ```bash
    terraform init
    ```
            
    Review the deployment plan and apply the infrastructure:
    ```bash
    terraform apply
    ```
            

    (Type yes when prompted to confirm the deployment.)

4. Test the Deployment
    - Log in to the AWS Management Console.

    - Navigate to AWS Lambda and locate your newly deployed function.

    - Create a test event and manually trigger the function.

    - Navigate to CloudWatch Logs to review the execution output and verify that stale snapshots were successfully identified and deleted.

5. Clean Up

If you wish to remove the deployed resources from your AWS account to prevent any charges, use Terraform to destroy the infrastructure:

```bash
terraform destroy
```
(Type yes when prompted to confirm the destruction.)

<br>
<br>

### Let's Connect:

<br>

Created by **Satya Sourav Patel**.

Subscribe to my [Substack](https://satyasouravpatel.substack.com/) for deep dives into DevOps, MLOps, and System Design.
