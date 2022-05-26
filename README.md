# aws_alarms_excel

## Setting up runtime environment

  create AWS credentials file in your home directory as `~/.aws/credentials` or set up required environment variables. For more details on setting up AWS cli environment, check [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

## Generating report

- Install the required packages:
    `pip install pandas json boto3`  
- Execute the file:
    `python3 aws_alarms_excel.py`

## Customising and scaling capabilities

  `config.json` file contains the configurable parameters. In this file you can customise the following:

- Fields that will be included in report, you can add/delete the list of fields here.

     ```javascript
     "fields":[
      "AlarmName",
      "ActionsEnabled",
      "AlarmActions",
      "MetricName",
      "Namespace"]
   ```

- Name of the excel sheets and their segregation conditions.

    ```javascript
     "Excel_sheets_namespace":{
      "AWS/EC2": {"name": "EC2", "data" : []},
      "AWS/AutoScaling" : {"name": "Autoscaling", "data" : []}, 
      "Generic": {"name": "Others", "data" : []}
   }
   ```

- Filename where result will be stored.

    ```javascript
    "output_file": "aws_alarms.xlsx"
    ```
