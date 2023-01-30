from google.cloud import bigquery
import googleapiclient.discovery


def create_or_get_table_and_dataset(project, bigquery_client, dataset_name, table_name):
    """
    This function creates or retrieves a BigQuery dataset and table using the provided BigQuery client.
    :param bigquery_client (google.cloud.bigquery.Client): A BigQuery client instance.
    :param dataset_name (str): The name of the BigQuery dataset.
    :param table_name (str): The name of the BigQuery table.
    :return: A tuple containing the BigQuery dataset and table objects.
    """
    try:
        dataset = bigquery_client.get_dataset(bigquery.Dataset(project + '.' + dataset_name))
    except:
        dataset = bigquery_client.create_dataset(bigquery.Dataset(project + '.' + dataset_name))

    try:
        table = bigquery_client.get_table(dataset.table(table_name))
    except:
        table = bigquery.Table(dataset.table(table_name))
        table.schema = [bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
                        bigquery.SchemaField("resource", "STRING", mode="REQUIRED"),
                        bigquery.SchemaField("permissions", "STRING", mode="REPEATED")]
        bigquery_client.create_table(table)

    return dataset, table



def check_permissions(request):
    """
    This function takes in a user's email address and resource name and checks their permissions in Google Cloud Platform, then returns a list of those permissions and saves them in a BigQuery table for later viewing. This is a super simple function
    :param request: a dictionary/object containing the email address of the user, the project name and the type of user either serviceAccount or user
    :return: A list of permissions the users has in the project
    """
    email = request.args.get('email')
    project = request.args.get('project')
    type = request.args.get('type')
    email = type+':'+email

    bigquery_client = bigquery.Client()
    # Use the application default credentials from the environment
    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    client = googleapiclient.discovery.build("cloudresourcemanager", "v3")
    resource = 'projects/' + project
    policy = client.projects().getIamPolicy(resource=resource, body={}).execute()

    # Get all policy bidings for the email address
    permissions = []
    for binding in policy['bindings']:
        if email in binding['members']:
            permissions.append(binding['role'])


    # You can name the dataset and table anything you want, just added examples here
    dataset_name = 'user_permissions'
    table_name = 'permissions'



    dataset, table = create_or_get_table_and_dataset(project, bigquery_client, dataset_name, table_name)


    # Loads results into the BQ table
    email = email.replace(type+':', '')
    rows_to_insert = [{'email': email, 'resource': project, 'permissions': permissions}]
    errors = bigquery_client.insert_rows(table, rows_to_insert)
    print("Results Loaded into BQ")
    if errors:
        raise ValueError(errors)
    return "All Permissions have been loaded"

