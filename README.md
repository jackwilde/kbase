# kbase

## About
This project is a Python based web application created using the Django framework. It provides a simple knowledge base
application for users to post and share knowledge articles.

The application is written and tested with Python 3.13 with Django 5.1.2. Full package requirements can be found in the 
[requirements.txt](./src/requirements.txt) file. 

## Deployment
The application is designed to run as a container, and in production scenarios Kubernetes is advised. It can be run
using Docker but this is only recommended in development and test environments. More information on running kbase with 
Docker is available [here](./docker/README.md)

Most settings can be controlled by environment variables, some will default if not set. View the table below for more
details.

In addition to the kbase application a **Postgres** database and **Nginx** reverse proxy are required. The Kubernetes deployment
guide will automate the set up of both of these.

A working SMTP server is required to run the application as user sign ups require email verification.

### Kubernetes
In a production environment it is recommended to deploy the application with Kubernetes using the provided Helm Chart.
1. Add the kbase Helm repository
    ```
    helm repo add kbase https://jackwilde.github.io/kbase
    helm repo update
    ```

2. Create a local copy of the chart [values.yaml](./helm/kbase/values.yaml) file and edit the required values. \
The minimum required values that must be set for the application to launch are listed here. 
    ```
   web:
     django:
       settings:
         secret_key: "<secret_key>"
         csrf_trusted_origins: "https://<server_hostname>"
   postgres:
     storage:
       storageClass: "<stoage_class>" # If no default StorageClass exists
     settings:
       postgres_db: "<database_name>"
       postgres_user: "<database_user>
       postgres_password: "<database_user_password>"
   ```

3. In addition to those settings it is highly recommended to enable and configure kbase to enable and use Kubernetes 
**Ingress** and **Network Policy** to provide additional security.

4. Once the values.yaml file has been configured, run the following command to deploy kbase
    ```
    helm install --create-namespace kbase kbase/kbase --namespace kbase --values ./values.yaml
    ```

### Environment
The following environment variables can be used to configure the application. The provided Helm chart and Docker compose
will assist in setting these.

| Environment Variable | Required | Default Value | Description                                                         |
|----------------------|----------|---------------|---------------------------------------------------------------------|
| POSTGRES_DB          | Yes      |               | The name of the database where the application will store its data  |
| POSTGRES_HOST        | Yes      |               | The IP address or hostname of the Postgres database server          |
| POSTGRES_PORT        |          | 5432          | The TCP port the Postgres server is listening on                    |
| POSTGRES_USER        | Yes      |               | The name of the Postgres user with owner permission to the database |
| POSTGRES_PASSWORD    | Yes      |               | The password for the Postgres user                                  |
| SECRET_KEY           | Yes      |               | The Django secret key use for cryptographic signing                 | 
| TIME_ZONE            |          | UTC           | The time zone of the Django server                                  |
| DEBUG                |          | False         | The status of Django debug mode                                     |
| ALLOWED_HOSTS        | Yes      |               | Comma separated list of approved hostnames for the website          | 
| SITE_URL             | Yes      |               | Fully qualified site URL include protocol prefix                    |
| EMAIL_HOST           | Yes      |               | SMTP server host address                                            |
| EMAIL_PORT           |          | 587           | SMTP server port                                                    |
| EMAIL_USE_TLS        |          | True          | Enable TLS connection to SMTP server                                |
| EMAIL_HOST_USER      | Yes      |               | Username for connection to SMTP server                              |
| EMAIL_HOST_PASSWORD  | Yes      |               | Password for connection to SMTP server                              |
| DEFAULT_FROM_EMAIL   | Yes      |               | Default email sending address                                       |


## Using the application
### Roles
The kbase application has two roles
* Standard
* Admin

When the application is deployed the first user that creates an account will become the designated admin. This admin 
user can then be used to promote other users to the admin role. Following this all users who create an account via the
sign up page will become standard users.

### Permissions
When creating a knowledge base article, the default permission is that only the creator and admins can view and edit the
article.

Kbase uses group based permissions which allow any user with edit permission on an article to delegate view and edit 
permissions to other groups. If a group has edit based permission for an article then they will also automatically be
able to view it. **_Any user with edit permission on an article will also be able to delete it._**

Initially there is only one group **'All Users'** which will contain all registered users of the application and cannot 
be modified. Admin users can create additional groups and update user membership from the admin dashboard.

### Standard Users
Standard users are able to log into the application and create knowledge base articles. That user will be able to view, 
edit, and delete any knowledge base articles they create. They will also be able to delegate permission to view and/or 
edit their articles.

### Admin Users
Admin users can use the same functions as standard users but will also be able to view, edit, and delete all articles. 
They additionally have access to the admin dashboard which will allow them to do the following actions:
* View and delete user accounts
* View, create, edit and delete user groups

