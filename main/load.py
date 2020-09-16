
import boto3
from boto3.dynamodb.types import TypeSerializer
from botocore.exceptions import ClientError

# initialization
dynamodb_client = boto3.client('dynamodb')
serializer = TypeSerializer()


def load_all(dataclass, records):
    """
    puts multiple records into DynamoDB by delegating to the load_one function
    :param dataclass: the dataclass to write
    :param records: the records to write
    :return: the responses from the underlying function as a list
    """

    response = list()
    for r in records:
        response.append(load_one(dataclass, r))

    print(f"INFO: Loaded {len(records)} into {dataclass.table_name}")
    return response


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
    print(f"INFO: Loading DynamoDB\n\tTable: {dataclass.table_name}\n\tItem: {item}")
    try:
        return dynamodb_client.put_item(TableName=dataclass.table_name, Item=item)

    except ClientError as e:
        raise e
