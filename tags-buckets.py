import boto3
import os
import json


class Tags_Buckets:
    def __init__(self, path_file):
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.path_file = path_file

    

    def create_tags_bucket(self, buckets, tags):
        try:
            # Crea etiquetas para el bucket
            for item_bucket in buckets:
                print("item_bucket", item_bucket)
                response = self.s3.put_bucket_tagging(
                    Bucket=item_bucket,
                    Tagging={
                        'TagSet': tags
                    }
                )
                print("response", response)
        except Exception as e:
            return str(e)
        
    
    def read_file_env(self, ):
        file = open(self.path_file, 'r')
        env_data = {}
        for line in file:
            if not line.strip() or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            env_data[key] = value
        return env_data
        

if __name__ == "__main__":
    try:
        path_file = os.path.join(os.path.dirname(__file__), 'tags.env')
        read_file_env = Tags_Buckets(path_file)
        env_data = read_file_env.read_file_env()
        tags_bucket = env_data['TAGS_BUCKET']
        tags_values = env_data['BUCKETS']
        json_tags_bucket = json.loads(tags_bucket)
        json_tags_values = json.loads(tags_values)
        response = read_file_env.create_tags_bucket(json_tags_values, json_tags_bucket)
    except Exception as e:
        print(str(e))
