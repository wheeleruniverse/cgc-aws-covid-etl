
import boto3
from boto3.dynamodb.types import TypeSerializer
from botocore.exceptions import ClientError

# initialization
dynamodb_client = boto3.client('dynamodb')
serializer = TypeSerializer()


def load_all(table, records, dataclass):
    """
    puts multiple records into DynamoDB by delegating to the load_one function
    :param table: the table to write to
    :param records: the records to write
    :param dataclass: the dataclass to write
    :return: the responses from the underlying function as a list
    """

    response = list()
    for r in records:
        response.append(load_one(table, r, dataclass))

    print(f"INFO: Loaded {len(records)} into {table}")
    return response


def load_one(table, record, dataclass):
    """
    puts a single item in a DynamoDB table using boto3
    :param table: the table to write to
    :param record: the record to write
    :param dataclass: the dataclass to write
    :return: the response from the put item call
    """

    item = {k: serializer.serialize(v) for k, v in dataclass.Schema().dump(record).items() if v != ""}
    print(f"INFO: Loading DynamoDB\n\tTable: {table}\n\tItem: {item}")
    try:
        return dynamodb_client.put_item(TableName=table, Item=item)

    except ClientError as e:
        raise e

