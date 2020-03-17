# pi-eye-py
Motion detection and object identification with DarkNet on Raspberry Pi setup


1. Run below commands
	sudo apt-get install python3-pip
	pip3 install -r requirements.txt
2. Configure aws CLI
	Download from https://aws.amazon.com/cli/
	navigate to directory ..\Amazon\AWSCLIV2
	open cli
	Run command: aws configure
		Add access key and secret key created from: https://console.aws.amazon.com/iam/home
		set region as: us-east-1
		set output format as: json
3. BOTO3 and aws user local setup complete
		
