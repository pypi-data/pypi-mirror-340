# Stratio CLI Tool

Stratio CLI Tool is a Python-based command line interface designed for support and operations teams to manage AWS infrastructures for customers acquired through the AWS Marketplace. It enables you to manage customer accounts, deploy and control clusters, interact with bootstrap EC2 instances during cluster installations, access cluster administration via the KEOS container, and view key operational logs.

> **Note:** This tool is intended for managing clusters that are deployed in customer AWS accounts. It supports operations such as starting/stopping clusters, force-uninstalling clusters, and managing the bootstrap instances that are used during the installation process.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Workflow](#architecture--workflow)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
    - [General Usage](#general-usage)
    - [Command Examples](#command-examples)
        - [Customer Management](#customer-management)
        - [Cluster Management](#cluster-management)
        - [Bootstrap Instance Management](#bootstrap-instance-management)
        - [KEOS Operations](#keos-operations)
        - [AWS Console Access](#aws-console-access)
        - [Log Operations](#log-operations)
    - [Filtering](#filtering)

---

## Overview

Stratio CLI Tool provides a unified interface to manage AWS-based clusters for customers who have purchased cluster services via the AWS Marketplace. It automates tasks such as:

- **Loading a YAML configuration file:** Similar to how `kubectl` uses a kubeconfig.
- **Customer and Cluster Management:** List, filter, and operate on customer records and their respective clusters.
- **Cluster Operations:** Start, stop, and force uninstall clusters.
- **Bootstrap Instance Handling:** Interact with the temporary bootstrap EC2 instance used during cluster installations. These bootstraps remain active during installation (or if an installation fails) and are automatically removed when installation is successful.
- **KEOS Container Management:** Access the KEOS container which includes administration tools (like `kubectl` and the `keos-installer` component) for already installed clusters.
- **AWS Console Linking:** Generate a link to access the AWS console for a specific customer account.
- **Log Management:** View logs for cluster start/stop operations and uninstalls. *(Installation logs are available through the bootstrap.)*

---

## Features

- **Multi-environment Configuration:** Load different configuration files based on environment contexts (e.g., `dev`, `prod`) or a custom configuration file.
- **Filtering & Custom Output:** Support for filtering results using command-line options and displaying output in table or JSON format.
- **Interactive & Automated Prompts:** Confirmation prompts for potentially destructive actions with an option to bypass for automation.
- **Real-time Log Streaming:** Automatically stream and monitor log events from CloudWatch, with support for switching to new log streams as they appear.
- **Modular Command Structure:** Organized subcommands for customers, clusters, bootstraps, KEOS operations, AWS-related actions, and logs.

---

## Architecture & Workflow

1. **Customer & Cluster Management:**  
   Customers from the AWS Marketplace are managed using this tool. Each customer has one or more clusters deployed in their AWS account. The CLI provides commands to list and filter these entities.

2. **Bootstrap Instances:**  
   During the installation of a cluster, a temporary bootstrap EC2 instance is deployed. The bootstrap remains available if the installation is ongoing or fails, but is removed automatically upon successful installation.

3. **KEOS Container:**  
   Once a cluster is installed, administration is performed via the KEOS container. This container encapsulates necessary management tools including `kubectl` and `keos-installer`.

4. **AWS Console Access:**  
   A dedicated command generates an AWS console link for a specific cluster’s AWS account to facilitate direct AWS management tasks.

5. **Log Streaming:**  
   The CLI streams logs from CloudWatch for start/stop operations and uninstall events. It polls for new log streams and switches to newer streams automatically.

---

## Installation

### Prerequisites

- **Python 3.12+** is required.
- Ensure you have [pip](https://pip.pypa.io/en/stable/installation/) installed.
- [Poetry](https://python-poetry.org/docs/#installation) is recommended for dependency management and packaging.
- AWS credentials and necessary permissions must be configured for each environment.

### Steps

1. **Clone this Repository:**

   ```bash
   git clone https://github.com/Stratio/aws-marketplace-toolkit
   cd aws-marketplace-toolkit
   ```

2. **Create and Activate a Virtual Environment (Optional):**
   While Poetry creates its own virtual environment by default, you can also manage your environment manually. For example, using venv:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the Project with Poetry:**
   If you haven't already installed Poetry, follow the installation instructions.
   ```bash
   poetry install
   ```
    This command will:
    
    - Create a virtual environment (if one isn’t already active)
    - Install all the project dependencies as specified in your pyproject.toml
    - Apply dynamic versioning using the version specified in the VERSION file

4. **Using the CLI**
   Once installed, you can run the CLI tool directly using Poetry:

   ```bash
   poetry run marketplace --help
   ```
   
    Or
    
   ```bash
   poetry shell
   marketplace --help
   ```

   Alternatively, run directly using:

   ```bash
   ./src/stratio/cli/marketplace.py --help
   ```

---

## Deployment

To deploy the Stratio CLI Tool, follow these steps:

### Build the Package

1. **Ensure all dependencies are installed:**

   ```bash
   poetry install
   ```

2. **Build the package:**

   ```bash
   poetry build
   ```

   This will create the distribution files in the `dist` directory.

### Upload the Package

1. **Install Twine if not already installed:**

   ```bash
   poetry add --dev twine
   ```

2. **Upload the package to PyPI:**

   ```bash
   twine upload dist/*
   ```

   You will be prompted to enter your PyPI credentials.

By following these steps, you can build and upload your package to PyPI, making it available for installation via `pip`.

## Configuration

The CLI tool uses a YAML configuration file to manage its settings. By default, it looks for a configuration file at:

- `~/.marketplace/config_default.yaml`

You can override this by:

- **Using a specific context:**
  ```bash
  marketplace --context prod customers list
  ```
  This loads the configuration file at `~/.marketplace/config_prod.yaml`.

- **Providing a custom configuration file:**
  ```bash
  marketplace --config /path/to/your/config.yaml clusters list
  ```

The configuration file should include necessary API credentials, AWS settings, and other operational parameters. Here is a template of the configuration file:

```yaml
customers:

  table_filter_regex: "^MarketplaceSubscribers.*$"

  session:
    profile:
      name: "seller@dev"

clusters:

  table_filter_regex: "^MarketplaceSubscribers.*$"
  workspaces_bucket_regex: ".*-automations-stratio-artifacts$"

  keos:
    workspaces_local_folder: /tmp
    base_image: qa.int.stratio.com/stratio/keos-installer
    vault_key: Stratio123

  lambdas:
    marketplace_subscribers_prefix: "MarketplaceSubscribers"
    start_stop_stratio_cluster_prefix: "StartStopStratioCluster"
    start_stratio_applications_prefix: "StartStratioApplications"
    remove_stratio_cluster_prefix: "RemoveStratioCluster"

  root:
    profile:
      name: "root@dev"
  seller:
    profile:
      name: "seller@dev"
  automations:
    profile:
      name: "automations@dev"
```

Each subcommand also provides its own help text:

```bash
marketplace customers --help
marketplace clusters --help
marketplace bootstraps --help
marketplace keos --help
marketplace aws --help
marketplace logs --help
```

### Command Examples

#### Customer Management

- **List all customers:**

  ```bash
  marketplace customers list
  ```

- **List customers with filters:**

  ```bash
  marketplace customers list --filter "status eq active"
  ```

#### Cluster Management

- **List clusters (output as JSON):**

  ```bash
  marketplace clusters list --output json
  ```

- **Start a cluster (only if in stopped state):**

  ```bash
  marketplace clusters start --cluster my-cluster-id
  ```

- **Stop a cluster (automatic confirmation):**

  ```bash
  marketplace clusters stop --cluster my-cluster-id --yes
  ```

- **Force uninstall a cluster (only applicable for unsubscribed clusters with a successful installation):**

  ```bash
  marketplace clusters uninstall --cluster my-cluster-id
  ```

#### Bootstrap Instance Management

- **List all bootstrap instances:**

  ```bash
  marketplace bootstraps list
  ```

- **Enter a bootstrap instance via SSM session:**

  ```bash
  marketplace bootstraps exec --instance i-0123456789abcdef0
  ```

- **Terminate a bootstrap instance:**

  ```bash
  marketplace bootstraps terminate --instance i-0123456789abcdef0 --yes
  ```

#### KEOS Operations

- **Enter a cluster via the KEOS client:**

  ```bash
  marketplace keos exec --cluster my-cluster-id
  ```

- **Download the KEOS workspace:**

  ```bash
  marketplace keos download --cluster my-cluster-id
  ```

#### AWS Console Access

- **Generate an AWS console link for a customer account:**

  ```bash
  marketplace aws link --account 123456789012
  ```
  
- **Generate an AWS console link for stored profile:**

  ```bash
  marketplace aws link --profile automations@dev
  ```

#### Log Operations

- **Stream start/stop logs for a cluster:**

  ```bash
  marketplace logs cluster --start-stop --cluster my-cluster-id
  ```

- **Stream uninstall logs for a cluster:**

  ```bash
  marketplace logs cluster --uninstall --cluster my-cluster-id
  ```

- **List available log groups:**

  ```bash
  marketplace logs groups
  ```

- **List log streams for a specific log group:**

  ```bash
  marketplace logs streams --group '/aws/stratio/cluster'
  ```

- **Stream logs for a specific log stream:**

  ```bash
  marketplace logs read --group '/aws/stratio/cluster' --stream 'stream-name'
  ```
  
#### Repositories Operations

- **Uploading a HELM chart from a zip file:**

  ```bash
  marketplace repositories push-helm --zip /path/file.zip --prefix stratio-14.7.0
  ```
    The self-contained zip with charts can be found in http://qa.int.stratio.com/repository/paas/kubernetes-universe/charts/kubernetes-universe-charts-14.4.1.zip for your release


- **Uploading a HELM chart from a charts file:**

  ```bash
  marketplace repositories push-helm --zip /path/file.zip --prefix stratio-14.7.0
  ```

    The charts file should possess the following structure:

  ```bash
  cat <<EOF > /tmp/helm-list.yaml
  helm_charts_override: [{'name':'aws-metering','repo_url':'http://qa.int.stratio.com/repository/helm','version':'0.3.0'},{'name':'sis','repo_url':'http://qa.int.stratio.com/repository/helm-all','version':'2.3.3-914a5d6'},{'name':'stratio-home','repo_url':'http://qa.int.stratio.com/repository/helm-all','version':'1.1.0-4f53872'},{'name':'stratio-panel-ui','repo_url':'http://qa.int.stratio.com/repository/helm-all','version':'2.1.0-13fedb4'}]
  EOF
  ```

- **Uploading a Docker image from a list file:**

  ```bash
    marketplace repositories push-docker --images /path/file.lst --prefix stratio-14.7.0
    ```
  
  The list file should possess the following structure:

  ```bash
  cat <<EOF > /tmp/docker-list.lst
  docker.io/curlimages/curl:7.85.0
  docker.io/curlimages/curl:7.85.1
  EOF
  ```

- **Delete repositories by prefix:**

  ```bash
  marketplace repositories delete-repository --prefix stratio-14.7.0 -r eu-west-1 -r us-east-1
  ```

- **Delete repositories by repository name:**

  ```bash
  marketplace repositories delete-repository --name stratio-14.7.0/local-path-provisioner -r eu-west-1 -r us-east-1
  marketplace repositories delete-repository --name stratio-14.7.0/local-path-provisioner --tag 0.1.0 -r eu-west-1 -r us-east-1
  ```

### Filtering

The Stratio CLI Tool supports filtering of customers, clusters, and other resources using a set of operators. Filters are provided as a command-line option (`--filter` or `-f`) and should be specified in the following format:

```
field operator value
```

Each filter consists of:
- **field**: The attribute name to filter on (e.g. `status`, `clusterStatus`, `customerIdentifier`).
- **operator**: One of the following supported operators:
    - `eq`: Equal to. Matches when the field is equal to the provided value.
    - `neq`: Not equal to. Matches when the field is not equal to the provided value.
    - `gt`: Greater than. Matches when the field is greater than the provided value.
    - `lt`: Less than. Matches when the field is less than the provided value.
    - `gte`: Greater than or equal to. Matches when the field is greater than or equal to the provided value.
    - `lte`: Less than or equal to. Matches when the field is less than or equal to the provided value.
    - `contains`: Contains. Matches when the field contains the provided value.
    - `begins_with`: Begins with. Matches when the field starts with the provided value.
    - `in`: In list. Matches when the field's value is within a list of values. **Note:** The value for the `in` operator must be provided as a list in the format `[value1,value2,...]`.

- **value**: The value to compare against. For boolean values, use `true` or `false`. For the `in` operator, supply a comma-separated list enclosed in square brackets (e.g. `[active,inactive]`).

#### Examples

- **Filter clusters with status equal to "started":**

  ```bash
  marketplace clusters list --filter "clusterStatus eq started"
  ```

- **Filter customers where the customer identifier is not "1234":**

  ```bash
  marketplace customers list --filter "customerIdentifier neq 1234"
  ```

- **Filter clusters with a node count greater than or equal to 3:**

  ```bash
  marketplace clusters list --filter "nodeCount gte 3"
  ```

- **Filter customers whose status is either "active" or "pending":**

  ```bash
  marketplace customers list --filter "status in [active,pending]"
  ```

Multiple filters can be specified by repeating the `--filter` option. The CLI combines these conditions using logical AND.

Under the hood, these filters are translated into DynamoDB filter expressions, and when multiple filters are provided, their corresponding expressions are combined using the AND operator. This flexible filtering mechanism enables precise querying of resources based on various attributes.

## AWS Finder toolkit

Provides a simple python script to locate every single resource belonging to any particular AWS Account. This is useful to identify resources that are not tagged or are not part of any CloudFormation stack.
To use this tool, simply type `python3 aws-finder.py --help` and follow the instructions. The recommended use-case is:
- Create the desired AWS profile in your local machine using `python3 manager.py profiles add --name my-profile --customer-provisioned-account-id 0123456789`.
- Use with finder the `--profile my-profile` option to target your specific account.
- Use with finder the `--output-file output.json` to save all the identified resources for later use.
- Limit the amount of AWS resources to locate. An example command can be found by typing `python3 aws_finder.py --help-resources`.

Example for Stratio use-case:

```bash
python3 finder.py --profile client-profile --region us-east-1 --output-file output.json \
  --with-loadbalancers \
  --with-cloudformation \
  --with-cloudwatch \
  --with-ec2 \
  --with-eks \
  --with-kms \
  --with-s3
```

## AWS Remove toolkit

Provides a simple script to remove every single resource belonging to any particular AWS Account. This is useful to clean up resources that are not tagged or are not part of any CloudFormation stack.
To use this tool, simply type `./aws-remove.py --help` and follow the instructions. The recommended use-case is:
- Use the previously saved output file from the AWS Finder toolkit.
- Use the previously saved AWS profile from the Manager toolkit.
- Run the script and let it manage dependencies among AWS resources.

