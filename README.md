
# AWS EBS Snapshot Cleanup
This project automates the cleanup of stale Amazon Elastic Block Store (EBS) snapshots in an AWS account to optimize storage costs. It uses an AWS Lambda function to identify and delete snapshots that are no longer associated with active EC2 instances.

## Features
- **Automated Cleanup**: Identifies and deletes stale EBS snapshots.
- **Cost Optimization**: Reduces unnecessary storage costs by removing unused snapshots.
- **Scheduled Execution**: Runs daily using Amazon CloudWatch Events.
- **Infrastructure as Code**: Uses Terraform to automate the deployment of AWS resources.

## Repository Structure
```bash
aws-ebs-snapshot-cleanup/
│
├── lambda_function/                # Contains the AWS Lambda function code
│ └── lambda_function.py            # Python script for the Lambda function
│
├── infrastructure/                 # Contains infrastructure configuration files
│ ├── lambda_iam_role.json          # IAM role policy for the Lambda function
│ ├── cloudwatch_event_rule.json    # CloudWatch Event rule configuration
│ └── terraform/                    # Terraform configuration files
│ ├── main.tf                       # Main Terraform configuration
│ ├── variables.tf                  # Terraform input variables
│ └── outputs.tf                    # Terraform output values
│
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies for the Lambda function
```
## How It Works
1. The **Lambda function** fetches all EBS snapshots owned by the account.
2. It retrieves a list of active EC2 instances (both running and stopped).
3. For each snapshot, it checks if the associated volume is not attached to any active instance.
4. If a snapshot is stale (i.e., its volume is not in use), it deletes the snapshot.
5. The process is automated using a **CloudWatch Event rule** that triggers the Lambda function daily.

## Prerequisites
Before deploying the project, ensure you have the following:
- **AWS Account**: With permissions to create Lambda functions, IAM roles, and CloudWatch Events.
- **AWS CLI**: Installed and configured with your credentials.
- **Python 3.8**: Installed on your local machine (for testing the Lambda function).
- **Terraform**: Installed to automate infrastructure deployment.

## Deployment Steps
```bash
  1. Clone the Repository
    git clone https://github.com/your-username/aws-ebs-snapshot-cleanup.git
    cd aws-ebs-snapshot-cleanup

2. Set Up the Lambda Function
    1. Install the required Python libraries:
            pip install -r requirements.txt

    2. Zip the Lambda function code:
            cd lambda_function
            zip lambda_function_payload.zip lambda_function.py

3. Deploy the Infrastructure with Terraform
    1. Navigate to the Terraform directory:
            cd infrastructure/terraform
    2. Initialize Terraform:
            terraform init
    3. Deploy the infrastructure:
            terraform apply
Confirm the deployment by typing yes when prompted.

4. Test the Project
    1. Manually trigger the Lambda function in the AWS Console.

    2. Check CloudWatch Logs to verify the execution and ensure snapshots are deleted as expected.

5. Clean Up
    To delete all resources created by Terraform:
        terraform destroy
```

