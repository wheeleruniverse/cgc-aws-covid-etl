
import boto3
import json

from boto3.dynamodb.types import TypeSerializer
from botocore.exceptions import ClientError
from os import environ
from pathlib import Path

# global initialization
aws_profile = environ.get("AWS_PROFILE")
print(f"'aws_profile': {aws_profile}")

# s3 initialization
s3_bucket_name = environ.get("S3_BUCKET_NAME")
s3_object_path = environ.get("S3_OBJECT_PATH")
s3_resource = boto3.resource("s3") if s3_bucket_name else None
s3_meta_client = s3_resource.meta.client if s3_resource else None
print(f"'s3_bucket_name': {s3_bucket_name}")
print(f"'s3_object_path': {s3_object_path}")

# sns initialization
sns_topic_arn = environ.get("SNS_TOPIC_ARN")
sns_resource = boto3.resource('sns') if sns_topic_arn else None
sns_topic = sns_resource.Topic(sns_topic_arn) if sns_resource else None
print(f"'sns_topic_arn': {sns_topic_arn}")

# dynamodb initialization
dynamodb_client = boto3.client("dynamodb")
serializer = TypeSerializer()


def load_json(records):
    """
    converts the records provided into json and writes them to S3
    :param records: the records to write to S3
    :return: None
    """

    if not s3_meta_client:
        print("WARN: S3 Bucket not initialized!")
        print("WARN: Ensure 'S3_BUCKET_NAME' is set as an Environment Variable")
        return

    # convert records to json
    json_rec = [i.to_json() for i in records]
    json_bin = json.dumps(json_rec, default=str, indent=4, sort_keys=True)

    # write json to a file
    src_file = f"{Path.cwd()}/main/resources/CovidStats.json"
    dst_path = f"{s3_object_path}/" if s3_object_path else ""
    dst_file = f"{dst_path}CovidStats.json"

    with open(src_file, "w") as f:
        f.write(json_bin)

    try:
        s3_meta_client.upload_file(src_file, s3_bucket_name, dst_file)

    except ClientError as e:
        print(f"ERROR: {str(e)}")


def load_all(dataclass, records):
    """
    puts multiple records into DynamoDB by delegating to the load_one function
    :param dataclass: the dataclass to write
    :param records: the records to write
    :return: the responses from the underlying function as a list
    """

    cnt = 0
    res = list()

    try:
        for r in records:
            res.append(load_one(dataclass, r))
            cnt += 1

        success_message = \
            f"SUCCESS! Loaded {cnt}/{len(records)} Record(s) into {dataclass.table_name}"

        print(f"INFO: {success_message}")
        publish_message("CGC0920: Data Load Success", success_message)

    except ClientError as e:
        failure_message = \
            f"FAILURE! Loaded {cnt}/{len(records)} Record(s) into {dataclass.table_name}\nError Message: {str(e)}"

        print(f"ERROR: {failure_message}")
        publish_message("CGC0920: Data Load Failure", failure_message)

    return res


def load_one(dataclass, record):
    """
    puts a single item in a DynamoDB table using boto3
    :param dataclass: the dataclass to write
    :param record: the record to write
    :return: the response from the put item call
    """

    if not hasattr(dataclass, "table_name"):
        raise ValueError(f"ERROR: Provided 'dataclass': {dataclass} must have a field named 'table_name'")

    item = {k: serializer.serialize(v) for k, v in dataclass.Schema().dump(record).items() if v != ""}
    print(f"INFO: Loading[Table: {dataclass.table_name}, Item: {item}]")
    try:
        return dynamodb_client.put_item(TableName=dataclass.table_name, Item=item)

    except ClientError as e:
        raise e


def publish_message(subject, message):
    """
    publishes a message to an SNS Topic
    :param subject: the subject of the message to publish
    :param message: the body of the message to publish
    :return: None
    """

    if not sns_topic:
        print("WARN: SNS Topic not initialized!")
        print("WARN: Ensure 'SNS_TOPIC_ARN' is set as an Environment Variable")
        return

    try:
        sns_topic.publish(Subject=subject, Message=message)

    except ClientError as e:
        print(f"ERROR: Failed to Publish Message"
              f"\n\tSNS Topic: {sns_topic}"
              f"\n\tError Message: {str(e)}")
