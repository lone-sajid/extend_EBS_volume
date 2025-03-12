## Extend the root filesystem of any Linux EC2 Instance on the fly.

REQUIREMENTS:
------------
1. This Script uses boto3(AWS SDK for python) and paramiko(for ssh connectivity and command execution).

2. Setup IAM credentails which should have necessary access permissions, such as DescribeInstances, ModifyVolume.
   
3. OS username information using which you will login to the EC2 Instance such as ec2-user in case of Amazon Linux.
   
4. You should have the SSH key pair which you will need to allow SSH connection to happen.

5. SSH network connectivity access from the source machine to the concerned EC2 Instance.

DEMO EXECUTION WORKFLOW:
-------------------------

$ python3 extend_volume.py
Enter the Instance ID for which volume needs to be extended: i-xxxxxxxxxxxxxx           -> Specify the Instance ID here
vol-xxxxxxxxxxxx   xx.xxx.xxx.xx
Enter the size to modify the volume: <size>
Enter the username using which you will login to the Instance ex: ec2-user in case of Amazon Linux: <OS_USERNAME>
Enter the absolute path of key pair to be used ex (/path/to/key.pem): <key_pair_path>
Connecting to EC2 instance at xx.xxx.xxx.xx...
Devices:
 NAME      FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
xvda                                                                             
├─xvda1   xfs          /     f3225129-f7e3-4da4-90f7-5035c457993d    6.4G    20% /
├─xvda127                                                                        
└─xvda128 vfat   FAT16       9AA3-6C3B                               8.7M    13% /boot/efi

running growpath for /dev/xvda1...
growpart completed...
lsblk Command output after growpart:
  NAME      MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
xvda      202:0    0  12G  0 disk 
├─xvda1   202:1    0  12G  0 part /
├─xvda127 259:0    0   1M  0 part 
└─xvda128 259:1    0  10M  0 part /boot/efi

Extending Filesystem...

Final filesystem details after extending...
 Filesystem     Type      Size  Used Avail Use% Mounted on
devtmpfs       devtmpfs  4.0M     0  4.0M   0% /dev
tmpfs          tmpfs     475M     0  475M   0% /dev/shm
tmpfs          tmpfs     190M  448K  190M   1% /run
/dev/xvda1     xfs        12G  1.6G   11G  14% /
tmpfs          tmpfs     475M     0  475M   0% /tmp
/dev/xvda128   vfat       10M  1.3M  8.7M  13% /boot/efi
tmpfs          tmpfs      95M     0   95M   0% /run/user/1000
