import boto3


class DB:
    def __init__(self, endpoint_url, name_url_table):
        self.connection = boto3.client('dynamodb', endpoint_url=endpoint_url, region_name='eu-west-1')
        self.name_url_table = name_url_table

    def init_db(self):
        self._create_table_if_not_exist()

    def _create_table_if_not_exist(self):
        if self.name_url_table not in self.connection.list_tables():
            table = self.connection.create_table(
                        TableName=self.name_url_table,
                        KeySchema=[
                            {
                                'AttributeName': 'short_url',
                                'KeyType': 'HASH'
                            }
                        ],
                        AttributeDefinitions=[
                            {
                                'AttributeName': 'long_url',
                                'AttributeType': 'S'
                            }
                        ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 5
                        }
                    )

        table.meta.client.get_waiter('table_exists').wait(TableName=self.name_url_table)

    def insert_url(self, short_url, long_url):
        url_table = self.connection.Table(self.name_url_table)
        url_table.put_item(
               Item={
                    'short_url': short_url,
                    'long_url': long_url,
                }
            )

    def get_long_url(self, short_url: str):
        url_table = self.connection.Table(self.name_url_table)
        row = url_table.get_item(
            Key={
                 'short_url': short_url
            }
        )
        return row.get('long_url')
