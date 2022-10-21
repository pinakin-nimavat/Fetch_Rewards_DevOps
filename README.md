# Fetch_Rewards_DevOps

## Description
Develop an automation program that takes a YAML configuration file as input and deploys a Linux AWS EC2 instance with two volumes and two users.

Here are some guidelines to follow:

	•	Create a YAML file based on the configuration provided below for consumption by your application
	•	You may modify the configuration, but do not do so to the extent that you fundamentally change the exercise
	•	Include the YAML config file in your repo
	•	Use Python and Boto3
	•	Do not use configuration management, provisioning, or IaC tools such as Ansible, CloudFormation, Terraform, etc.

## Steps to run the program

Please gather all the files you may want to use to copy to ec2 instance or content of this repo into one folder.  Open the terminal at the same folder or open a terminal and change the working directory to the path of the same folder
mentioned in the former part of this sentence. 

- Ensure that python is up and running in your machine 
	If not please use:  sudo apt-get install python3  (in terminal)
- Ensure that you have pre installed pyyaml, boto3, awscli packages. 
	If not please use:  pip install -r requirements.txt
 
Configure user's policy with full permissions to EC2 following steps:

	1.	Launch the Identity and Access Management console (IAM) in AWS. 
	
	2.	Click Users on the navigation menu on the left of the screen. 
	
	3.	In the popup window, click on Add User. 
	
	4.	In the new window, provide a user name and choose the 'Programmatic Access' access type, then click next. 
	
	5.	to set the permissions, choose 'Attach Existing Policies Directly' and in the Policy Filter type 'AmazonEC2FullAccess', you can choose any permission level, but in this example I'll click on the checkbox next to 'AmazonEC2FullAccess' and then click the 'next' button. 
	
	6.	Finally, review the user and permission levels, and click on the 'Create User' button. 
	
	7.	The next page will show your keys. These are only available once, so its a good idea to download and save then safely in a secure location. You can use .csv file in the next step.

Configure AWS credentials locally (write following commands in terminal):

	1.	aws configure 
	
	⁃	Please use the downloaded csv file to enter the following values. 
	
	⁃	It will prompt you with:
	
	⁃	AWS Acecess Key ID: enter the id
	
	⁃	AWS Secret Access Key : enter the key 
	
	⁃	Default region name : enter the region 
	
	⁃	Default output format : json 

	2.	aws ec2 describe-instances ( This should return details of any EC2 instance running on AWS in JSON format if the credentials are good. Otherwise, an error is thrown, which means the credentials do not work. )

The script will deploy the instance using config.yaml file.

Run the python code using following command in terminal:
	python script.py
	
The script will run and generate a ip address. Use the ip address to log into ec2 instance:

	For user1 :  ssh -i fetch-keypair.pem user1@generated_ip_address
	
	For user2 :  ssh -i fetch-keypair.pem user2@generated_ip_address

In order to copy file to the user from your local machine to one of the user into the instance follow the steps:

	1.	User1 : scp -i fetch-keypair.pem file_to_upload user1@ec2-x-y-z-t.compute-1.amazonaws.com:/home/user1
	
	2.	User2 : scp -i fetch-keypair.pem file_to_upload user2@ec2-x-y-z-t.compute-1.amazonaws.com:/home/user2
	(where x,y,z,t are the generated ip address (x,y,z,t))
	
I have also added a deletaion script which will delete the generated keypair file from the cloud as well from the local machine. please use the code as python delete.py (in terminal). PLEASE NOTE THAT IT WILL NOT TERMINATE OR STOP THE INSTANCE. YOU HAVE TO DO THAT MANUALLY BY LOGGING INTO THE EC2 CONSOLE. 

### NOTE: DO NOT FORGET TO TERMINATE / STOP THE EC2 INSTANCE FROM EC2 CONSOLE :)	

## Resources

https://www.ipswitch.com/blog/how-to-create-an-ec2-instance-with-python
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
https://aws.amazon.com/premiumsupport/knowledge-center/ec2-user-account-cloud-init-user-data/	

