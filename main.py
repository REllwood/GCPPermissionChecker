import google.auth
from google.auth.transport.requests import Request
from google.cloud import iam, bigquery



def check_permissions(request):
    """
    This function takes in a user's email address and resource name and checks their permissions in Google Cloud Platform, then returns a list of those permissions and saves them in a BigQuery table for later viewing. This is a super simple function
    :param request: a dictionary/object containing the email address of the user
    :return: A list of permissions the users has in the project
    """
    email = request.args.get('email')
    # Use the application default credentials from the environment
    creds, project = google.auth.default()
    client = iam.Client(credentials=creds)
    policy = client.get_iam_policy(project)

    # Get all policy bidings for the email address
    permissions = []
    for binding in policy.bindings:
        if email in binding.members:
            permissions.extend(binding.role.split('.')[-1])
    bigquery_client = bigquery.Client(credentials=creds)

    # You can name the dataset and table anything you want, just added examples here
    dataset_name = 'user_permissions'
    table_name = 'permissions'

    dataset = bigquery_client.create_dataset(dataset_name)
    table = bigquery.Table(dataset.table(table_name))
    table.schema = [bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("resource", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("permissions", "STRING", mode="REPEATED")]
    table = bigquery_client.create_table(table)

    # Loads results into the BQ table
    rows_to_insert = [{'email': email, 'resource': project, 'permissions': permissions}]
    errors = bigquery_client.insert_rows(table, rows_to_insert)
    if errors:
        raise ValueError(errors)

    return permissions

