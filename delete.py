import boto3
import subprocess
import os,sys,stat 

try:
	os.remove("fetch-keypair.pem")
except Exception as e:
	pass


ec2 = boto3.client('ec2')
try:
	response = ec2.delete_key_pair(KeyName='fetch-keypair')
except Exception as e:
	pass