from flask import Flask, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# Initialize the S3 client
s3 = boto3.client('s3')

# Set the bucket name (replace with your actual bucket name)
BUCKET_NAME = 'http-bucket-vinod'  # Replace with your S3 bucket name


def list_s3_objects(path=''):
    """List objects in the S3 bucket for the given path."""
    try:
        # If path is empty, we list top-level content
        prefix = path if path else ''
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, Delimiter='/')

        # Collect the directories and files
        directories = [content['Prefix'].split('/')[1] for content in response.get('CommonPrefixes', [])]
        files = [content['Key'].split('/')[1] for content in response.get('Contents', [])]

        # Return the combined list
        return directories + files

    except (NoCredentialsError, PartialCredentialsError):
        return None


@app.route('/list-bucket-content/', methods=['GET'])
@app.route('/list-bucket-content/<path>', methods=['GET'])
def list_bucket_content(path=None):
    """Handle GET request to list content in the S3 bucket."""
    if path is None:
        path = ''  # Empty path means top-level content

    # Get the list of objects for the specified path
    content = list_s3_objects(path)

    if content is None:
        return jsonify({"error": "AWS credentials not configured properly."}), 500

    # Return JSON response with content
    return jsonify({"content": content})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Run the server on IP:PORT

