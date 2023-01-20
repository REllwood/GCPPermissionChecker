
# Check User Permissions in Google Cloud Platform

This Cloud Function takes in a user's email address and checks their permissions in Google Cloud Platform, then returns a list of those permissions and saves them in a BigQuery table for later viewing.


## Usage/Examples

To use the function, make a GET request to the cloud functions endpoint with the following parameters:

**email:** The email address of the user whose permissions you want to check

The request object should have the following format:

```
{
    "args": {
        "email": "test@company.com",
        "resource": "projects/[PROJECT_ID]"
    }
}


```
## Notes
You need to have the appropriate credentials set up for the google-cloud-sdk and the google-auth library.
Your service account needs to have the necessary permissions to retrieve the IAM policy of the resource in question and create and insert rows in a Bigquery table.
- If the dataset or table does not exist it will create them but it will use the name 'user_permissions' for the dataset and 'permissions' for the table.
- If the table exists it should have the same schema as the function defined otherwise it may raise an error.
## Output - What to expect

The function will return a list of the permissions that the user has in the project.
It will also insert the user's email, resource and permissions into a BigQuery table for later viewing.
## Installation
- Clone the repository
- Create a virtual environment
- Install the required package from requirements.txt
- Deploy the function to your environment
- Make a GET request to the endpoint of the deployed function with the required parameters and you are good to go
    
## Contributing

Contributions are always welcome!

- Fork the repository
- Create a new branch
- Make the necessary changes
- Create a Pull Request


## License

[MIT](https://choosealicense.com/licenses/mit/)


