import boto3
import time

# Initialize EC2 client and resource
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

key_name = 'test-hv'
security_group_id = 'sg-0fccc5cc345e23eef'
docker_image_frontend = 'muzahidulnisar/frontend:latest'
instance_type = 't2.micro'
ami_id = 'ami-0c2af51e265bd5e0e'

# User data script to install Docker and run your frontend application
user_data_script = f'''#!/bin/bash
# Update system and install Docker
yum update -y
amazon-linux-extras install docker
service docker start
usermod -a -G docker ubuntu

# Pull and run the Docker container with your frontend application
docker run -d -p 3000:3000 {docker_image_frontend}
'''

def create_ec2_instance():
    # Launch an EC2 instance
    instance = ec2_resource.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,
        SecurityGroupIds=[security_group_id],
        UserData=user_data_script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'Frontend'}
                ]
            }
        ]
    )[0]
    
    print(f"Launching EC2 Instance {instance.id}...")
    instance.wait_until_running()
    instance.reload()

    print(f"EC2 Instance {instance.id} is running.")
    print(f"Public DNS: {instance.public_dns_name}")
    return instance

if __name__ == '__main__':
    instance = create_ec2_instance()
    
    # Step 2: Wait for EC2 to initialize and provide access
    print(f"Instance {instance.id} public IP: {instance.public_ip_address}")
    print("Frontend application is now running.")
