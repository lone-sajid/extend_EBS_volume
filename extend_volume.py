import boto3
import paramiko                  #for ssh connection
ec2 = boto3.client('ec2')

instance_id = input("Enter the Instance ID for which volume needs to be extended: ")
response = ec2.describe_instances(InstanceIds=[instance_id])

### Fetch Root volume ID and Public IP address of Instance.
volume_id=response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
public_ip= response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']
print(volume_id, " ", public_ip)

# Modify Root EBS volume of given instance.
modified_size=int(input("Enter the size to modify the volume: "))
ec2.modify_volume(VolumeId=volume_id, Size=modified_size)
os_user= input("Enter the username using which you will login to the Instance ex: ec2-user in case of Amazon Linux: ")
private_key_path= input("Enter the absolute path of key pair to be used ex (/path/to/key.pem): ")

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
try:
    ### Connect to the Instance....
    print(f"Connecting to EC2 instance at {public_ip}...")
    ssh_client.connect(public_ip, username=os_user, key_filename=private_key_path)

    # Run Linux commands
    stdin, stdout, stderr = ssh_client.exec_command('sudo lsblk -f')
    device_name = stdout.read().decode()

    print("Devices:\n",device_name)
    dev = device_name.split()
    #print("After split:\n", dev)
    
    if 'xvda' in dev:
        print("running growpath for /dev/xvda1...")
        stdin, stdout, stderr = ssh_client.exec_command('sudo growpart /dev/xvda 1')
        print("growpart completed...")
        stdin, stdout, stderr = ssh_client.exec_command('sudo lsblk')
        print("lsblk Command output after growpart:\n ", stdout.read().decode())

    elif 'nvme0n1' in dev:
        print("running growpath for /dev/nvme0n1p1...")
        stdin, stdout, stderr = ssh_client.exec_command('sudo growpart /dev/nvme0n1 1')
        print("After running growpath...")
        stdin, stdout, stderr = ssh_client.exec_command('sudo lsblk')
        print("lsblk Command output:\n ", stdout.read().decode())
    else:
        print("Device name isn't compatible with this script")
        exit
    print("Extending Filesystem...\n")    
    if 'xfs' in dev:
        ssh_client.exec_command('sudo xfs_growfs -d /')
    else:
        if 'xvda' in dev:
            ssh_client.exec_command('sudo resize2fs /dev/xvda1')
        else:
            ssh_client.exec_command('sudo resize2fs /dev/nvme0n1p1')  

    stdin, stdout, stderr = ssh_client.exec_command('sudo df -Th')
    print("Final filesystem details after extending...\n", stdout.read().decode())
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh_client.close() 
