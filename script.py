import yaml
import boto3
from collections import defaultdict
import traceback
import subprocess
import os,sys,stat 



KEYNAME = 'fetch-keypair'
IMAGES = defaultdict(str)
IMAGES ['amzn2-hvm-x86_64'] = 'ami-026b57f3c383c2eec'
# IP range of machines requiring SSH access
MYIP = '0.0.0.0/0'


with open('config.yaml', 'r') as conff:
    try:
        conf = yaml.safe_load(conff)
    except yaml.YAMLError as e:
        print(e)

try:
    ec2 = boto3.resource('ec2')
    conf = conf['server']
    vol1 = conf['volumes'][0]
    vol2 = conf['volumes'][1]
    user1 = conf['users'][0]
    user2 = conf['users'][1]

    # create keypairs
    with open(KEYNAME+'.pem', 'w') as kpfile:
        try:
            key_pair = ec2.create_key_pair(KeyName=KEYNAME)
            kpfile.write(str(key_pair.key_material))
        except Exception as e:
            print('Could not create key-pair as It already exists')
            print(type(e).__name__)
            kpfile.close()
        
    kname = KEYNAME + '.pem'

    os.chmod(kname,stat.S_IREAD)

    public_key = subprocess.run(['ssh-keygen','-y','-f',kname],capture_output = True)
    public_key = public_key.stdout.decode()

    ami = conf['ami_type']
    ami += '-' + conf['virtualization_type']
    ami += '-' + conf['architecture']

    user_data = f''' 
        #cloud-config
        cloud_final_modules:
            - [users-groups,always]
        users:
            - name: {user1['login']}
              groups: [ wheel ]
              sudo: [ "ALL=(ALL) NOPASSWD:ALL" ]     
              shell: /bin/bash
              ssh-authorized-keys: {public_key}

            - name: {user2['login']}
              groups: [ wheel ]
              sudo: [ "ALL=(ALL) NOPASSWD:ALL" ]     
              shell: /bin/bash
              ssh-authorized-keys: {public_key}
            
    '''

    # create a new EC2 instance
    instances = ec2.create_instances(
        KeyName=KEYNAME,
        ImageId=IMAGES[ami],
        InstanceType=conf['instance_type'],
        MinCount=conf['min_count'],
        MaxCount=conf['max_count'],
        UserData=user_data,
        BlockDeviceMappings=[
            {
                'DeviceName': vol1['device'],
                'Ebs': {
                    'VolumeSize': vol1['size_gb'],
                    'DeleteOnTermination' : True
                }
            },
            {
                'DeviceName': vol2['device'],
                'Ebs': {
                    'VolumeSize': vol2['size_gb'],
                    'DeleteOnTermination' : True
                }
            }
        ]
    )
    # wait for instance initialization
    print('Instance created, initialization pending ... ')
    instanceIds=[instances[0].id]
    waiter = ec2.meta.client.get_waiter('instance_running')
    waiter.wait(InstanceIds=instanceIds)
    print(' ... running!')

    print('Authorizing security group ingress for SSH ...')
    try:
        # allow inbound ssh rules
        client = boto3.client('ec2')
        describe = client.describe_instances()
        sgId = describe['Reservations'][-1]['Instances'][0]['SecurityGroups'][0]['GroupId']
        resp = client.authorize_security_group_ingress(
            GroupId=sgId,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': MYIP}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': MYIP}]}
        ])

    except Exception as e:
        pass

    print('Instance public ip address:')
    instance = list(filter(lambda x: x['Instances'][0]['InstanceId']==instances[0].id, describe['Reservations']))
    print(instance[0]['Instances'][0]['PublicIpAddress'])

except Exception as e:
    print(type(e).__name__)
    print('Could not create instance.')
    traceback.print_exc()