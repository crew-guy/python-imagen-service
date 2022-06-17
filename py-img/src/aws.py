import boto3
import os
from utils import delete_file
from dotenv import load_dotenv
load_dotenv()
class S3Client(object):
    def __init__(self, region_name=os.getenv('AWS_S3_REGION_NAME')):
        self.region_name = region_name
        self.client = boto3.client(
            's3', 
            region_name=self.region_name,
            aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('S3_ACCESS_KEY_SECRET'),
        )


    def upload_file(self, filename, bucket_name, key):
        self.client.upload_file(
            filename, 
            bucket_name, 
            key,
            ExtraArgs={'ACL': 'public-read'}
        )
        delete_file(filename)
        
        # try: 
        #     ret_code = 200
        #     body = "https://uadoc.uacdn.net/" + filename
        # except Exception as e:
        #     ret_code = 500
        #     body = str(e)
    
    # def read_inmemory(self, bucket, key):
    #     obj = self.client.get_object(Bucket=bucket, Key=key)
    #     body = obj['Body']
    #     return body.read()

s3_client = S3Client()



# AWS Queuing Service

class SQSClient(object):
    def __init__(self, region_name=os.getenv('AWS_S3_REGION_NAME')):
        self.region_name = region_name
        self.client = boto3.client('sqs', region_name=self.region_name)
        self.queues_url = {}


    def get_queue_url(self, queue_name):
        queue_url = self.queues_url.get(queue_name)
        if queue_url is None:
            try:
                queue_url = self.client.get_queue_url(QueueName=queue_name)['QueueUrl']
                self.queues_url[queue_name] = queue_url
            except Exception as e:
                print('fail')
                # submit_exception_to_sentry(e)
        return queue_url


    def send_message(self, queue_name, message):
        queue_url = self.get_queue_url(queue_name)
        try:
            self.client.send_message(QueueUrl=queue_url, MessageBody=message)
            return "Message pushed to queue successfully"
        except Exception as e:
            print('fail')
            # submit_exception_to_sentry(e)
        return "Failed to send sms"


    def receive_messages(self, queue_name, max_msgs=10, visibility_timeout=30):
        queue_url = self.get_queue_url(queue_name)
        try:
            response = self.client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_msgs,
                VisibilityTimeout=visibility_timeout,
                MessageAttributeNames=[
                    'All'
                ],
            )
            return response
        except Exception as e:
            print('fail')
            # submit_exception_to_sentry(e)
        return []


    def delete_messages_batch(self, queue_name, messages_to_delete):
        queue_url = self.get_queue_url(queue_name)
        response = {
            "Successful": [],
            "Failed": []
        }
        try:
            for i in range(0, len(messages_to_delete), 10):
                message_batch_to_delete = messages_to_delete[i:i+10]
                batch_response = self.client.delete_message_batch(
                    QueueUrl=queue_url,
                    Entries=message_batch_to_delete
                )
                response["Successful"].extend(batch_response.get("Successful", []))
                response["Failed"].extend(batch_response.get("Failed", []))
            return response
        except Exception as e:
            print('fail')
            # submit_exception_to_sentry(e)
        return response


sqs_client = SQSClient(region_name=os.getenv('AWS_SQS_REGION_NAME'))