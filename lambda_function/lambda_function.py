import boto3
import logging

# Seting up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initializing EC2 client
    ec2 = boto3.client('ec2')

    try:
        # Fetching all snapshots owned by the account
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

        # Fetching all active EC2 instances (running and stopped)
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}])
        active_volumes = set()

        # Extractracting volume IDs from active instances
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                for volume in instance.get('BlockDeviceMappings', []):
                    active_volumes.add(volume['Ebs']['VolumeId'])

        # Identifying stale snapshots
        stale_snapshots = []
        for snapshot in snapshots:
            volume_id = snapshot.get('VolumeId')
            if volume_id and volume_id not in active_volumes:
                stale_snapshots.append(snapshot['SnapshotId'])

        # Deleting stale snapshots
        for snapshot_id in stale_snapshots:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            logger.info(f"Deleted stale snapshot: {snapshot_id}")

        return {
            'statusCode': 200,
            'body': f"Deleted {len(stale_snapshots)} stale snapshots."
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e