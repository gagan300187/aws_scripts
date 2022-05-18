import pandas as pd
import json
import boto3

def get_config_data():
    """Fetches user defined configuration data from 'config.json' file

    Returns:
        dict: user defined config data in dict format.
    """
    cfile = open('config.json','r')
    cdata = json.load(cfile)
    return cdata 

def fetch_alarms_data():
    """fetches cloudwatch alarms data from configured AWS account

    Returns:
        dict: Cloudwatch data in form of dict.
    """
    client = boto3.client('cloudwatch')
    data = client.describe_alarms()
    return data


def filter_namespace(filter_data, ns_data):
    """seggregates alarms data as per namespace given in config.json
    this namespace mapping will be used to categorize the type of resource/cloudwatch alarm
    if namespace is not provided in config.json file, then data will be allocated to generic/others category.

    Args:
        filter_data (list): list of all cloudwatch alarms received from aws
        ns_data (dict): namespace and settings mapping of configured namespaces

    Returns:
        dict: dictionary of seggregated namespace with cloudwatch alarms details
    """
    for i in filter_data:
        namespace = i[4]
        if namespace in ns_data.keys():
            ns_data.get(namespace)['data'].append(i)
        else:
            ns_data.get("Generic")['data'].append(i)
    return ns_data
    


def generate_excel(excel_filename, sheet_data, sheet_columns):
    """Geerates excel file with multiple sheets (with sheet_name configured in namespace data)

    Args:
        excel_filename (string): name of the output excel file that will store the result
        sheet_data (dict): Cloudwatch alarms data to be saved in given sheets
        sheet_columns (list): list of selected columns to be saves in sheet
    """
    writer=pd.ExcelWriter(excel_filename)
    for sheet in sheet_data:
        sheet_name=sheet_data[sheet]['name'] #define sheet name for excel report
        if len(sheet_data[sheet]['data']) > 0:
            df = pd.DataFrame(sheet_data[sheet]['data'])
            df.columns = sheet_columns
            df.to_excel(writer, sheet_name=sheet_name, index=False) #write csv file to excel
    writer.save()  #Save excel file

if __name__ == "__main__":
    filter_data = []
    config_data = get_config_data()
    fields = config_data['fields']
    ns_data = config_data['Excel_sheets_namespace']
    alarms = fetch_alarms_data()['MetricAlarms']
    output_file = config_data['output_file']
    for alarm in alarms: 
        filter_data.append([alarm[x] for x in fields])
    sheet_data = filter_namespace(filter_data, ns_data)
    generate_excel(output_file, sheet_data, fields)
