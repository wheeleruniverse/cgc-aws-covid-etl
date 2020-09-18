
import boto3
from boto3.dynamodb.types import TypeSerializer
from botocore.exceptions import ClientError
from os import environ

# global initialization
aws_profile = environ.get("AWS_PROFILE")
print(f"'aws_profile': {aws_profile}")

sns_topic_arn = environ.get("SNS_TOPIC_ARN")
print(f"'sns_topic_arn': {sns_topic_arn}")

dynamodb_client = boto3.client("dynamodb")
serializer = TypeSerializer()

sns_resource = boto3.resource('sns') if sns_topic_arn else None
sns_topic = sns_resource.Topic(sns_topic_arn) if sns_resource else None


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
