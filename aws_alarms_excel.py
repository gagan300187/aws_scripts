import pandas as pd
import json
import boto3

def get_config_data():
    cfile = open('config.json','r')
    cdata = json.load(cfile)
    return cdata 

def fetch_alarms_data():
    client = boto3.client('cloudwatch')
    data = client.describe_alarms()
    return data


def filter_namespace(filter_data, ns_data):
    for i in filter_data:
        namespace = i[4]
        if namespace in ns_data.keys():
            ns_data.get(namespace)['data'].append(i)
        else:
            ns_data.get("Generic")['data'].append(i)
    return ns_data
    


def generate_excel(excel_filename, sheet_data, sheet_columns):
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
