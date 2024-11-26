import redshift_connector

host = 'arn:aws:redshift-serverless:us-east-2:779846797040:namespace/a50ffce3-a3d5-46f5-a454-49701c5b56aa'
database = 'dev'
user = 'admin'
password = ''
port = 5439  # Default Redshift port

# Establish connection
conn = redshift_connector.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)