import boto3

class S3Client(object):
    def __init__(self, region_name=AWS_S3_REGION_NAME):
        self.region_name = region_name
        self.client = boto3.client('s3', region_name=self.region_name)

    def generate_put_signed_url(self, bucket_name, key, expiry=3600, acl=None):
        '''
        For ACL to be public bucket either must be public or private with object can be public
        '''
        parameters = {
            'Bucket': bucket_name,
            'Key': key,
        }
        if acl:
            parameters['ACL'] = acl

        return self.client.generate_presigned_url(
            ClientMethod='put_object',
            Params=parameters,
            ExpiresIn=expiry
        )

    def generate_get_signed_url(self, bucket_name, key, expiry=3600, acl=None):
        '''
        For ACL to be public bucket either must be public or private with object can be public
        '''
        parameters = {
            'Bucket': bucket_name,
            'Key': key,
        }
        if acl:
            parameters['ACL'] = acl

        return self.client.generate_presigned_url(
            ClientMethod='get_object',
            Params=parameters,
            ExpiresIn=expiry
        )
    
    def read_inmemory(self, bucket, key):
        obj = self.client.get_object(Bucket=bucket, Key=key)
        body = obj['Body']
        return body.read()

s3_client = S3Client()

def delete_file(file):
    try:
        import os
        os.remove(file)
    except:
        pass

file_name = str(uuid1()) + ".jpg"
    background_image = background_image.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    new_file_name = '/tmp/' + file_name
    background_image.save(new_file_name, optimize=True, quality=80)
    try:
        # background_image.show()
        S3.upload_file(new_file_name, BUCKET_NAME, 'zamzar/{0}'.format(file_name),
                       ExtraArgs={'ACL': 'public-read'})
        delete_file(new_file_name)
        ret_code = 200
        body = "https://uadoc.uacdn.net/" + file_name
    except Exception as e:
        ret_code = 500
        body = str(e)