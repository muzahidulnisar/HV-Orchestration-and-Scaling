import boto3

# Initialize EC2 client
ec2_client = boto3.client('ec2')

def create_vpc():
    # Create VPC
    response = ec2_client.create_vpc(
        CidrBlock='10.0.0.0/16',
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {'Key': 'Name', 'Value': 'MyVPC'}
                ]
            }
        ]
    )
    vpc_id = response['Vpc']['VpcId']
    print(f"Created VPC with ID: {vpc_id}")

    # Enable DNS support and DNS hostnames for the VPC
    ec2_client.modify_vpc_attribute(
        VpcId=vpc_id,
        EnableDnsSupport={'Value': True}
    )
    ec2_client.modify_vpc_attribute(
        VpcId=vpc_id,
        EnableDnsHostnames={'Value': True}
    )
    return vpc_id

def create_subnet(vpc_id, cidr_block, az):
    # Create a subnet in the specified Availability Zone
    response = ec2_client.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block,
        AvailabilityZone=az,
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {'Key': 'Name', 'Value': f'Subnet-{az}'}
                ]
            }
        ]
    )
    subnet_id = response['Subnet']['SubnetId']
    print(f"Created Subnet with ID: {subnet_id} in {az}")
    return subnet_id

def create_security_group(vpc_id, group_name, description):
    # Create a security group within the VPC
    response = ec2_client.create_security_group(
        Description=description,
        GroupName=group_name,
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {'Key': 'Name', 'Value': group_name}
                ]
            }
        ]
    )
    security_group_id = response['GroupId']
    print(f"Created Security Group with ID: {security_group_id}")
    return security_group_id

def authorize_security_group_ingress(security_group_id):
    # Allow inbound SSH and HTTP traffic
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    print(f"Ingress rules added to Security Group ID: {security_group_id}")

if __name__ == '__main__':
    # Step 1: Create VPC
    vpc_id = create_vpc()

    # Step 2: Create Subnets
    subnet_1 = create_subnet(vpc_id, '10.0.1.0/24', 'us-east-1a')
    subnet_2 = create_subnet(vpc_id, '10.0.2.0/24', 'us-east-1b')

    # Step 3: Create Security Group
    security_group_id = create_security_group(vpc_id, 'MySecurityGroup', 'Security group for my VPC')
    
    # Step 4: Authorize inbound traffic (SSH, HTTP)
    authorize_security_group_ingress(security_group_id)
