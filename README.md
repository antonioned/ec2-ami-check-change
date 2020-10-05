# ec2-ami-check-change
A python script that checks ami key in a JSON file and changes it correspondingly.

The use case I have is that I use a JSON file to launch new EC2 instances. In the JSON file I have all of the EC2 paramaters needed (SG, subnet, instance type, ami). The point of interest here is the AMI used. I bake a new image via Packer automatically in my CI/CD pipeline and when that new AMI is available, I want to change the JSON file with it.

The JSON contains different keys which correspond to different services that launch different EC2 instances. I only need to change the ones that have a `type` key which equals `linux-browsers`. The others which don't have the `type` key or have a different value for it, must not be changed.

The script does exactly this:

1. Checks the JSON file for the `ami` key
2. Checks a txt file which has been pushed by the CI/CD pipeline in S3 and contains the AMI ID of the latest AMI.
3. Compares them both and if there is a difference, changes the value of the `ami` key in the JSON file, only where needed.

Check the `JSON_FILE.example.json` as an example of how the JSON file can look like.