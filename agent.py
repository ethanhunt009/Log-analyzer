import subprocess 
import os
import shutil
from langchain.tools import Tool  
from langchain_core.tools import StructuredTool
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from pydantic import BaseModel
from dotenv import load_dotenv

import paramiko

#-------------------------------------------------------


#-------------------------------------------------------

def read_suricata_log():
    """Read the suricata log file"""
    try:
        with open("log.txt", 'r') as file:
            content = file.read()
    except FileNotFoundError:
        content = "Log file not found."
    return content

suricata_tool = Tool(
    name = "read_suricata_log",
    description="Read the suricata log file",
    func=read_suricata_log,
)
#-------------------------------------------------------

def report_anomaly(report: str):
    """Report an anomaly to the server"""
    try:
        with open("anomaly_report.txt", 'w') as file:
            file.write(report)
        return "Anomaly reported successfully."
    except Exception as e:
        return f"Failed to report anomaly: {str(e)}"

report_anomaly_tool = Tool(
    name = "report_anomaly",   
    description="Report an anomaly to the server",
    func=report_anomaly,   
)
#-------------------------------------------------------

def report_error(error: str):
    """Report an error to the server"""
    try:
        with open("error_report.txt", 'w') as file:
            file.write(error)
        return "Error reported successfully."
    except Exception as e:
        return f"Failed to report error: {str(e)}"

report_error_tool = Tool(
    name = "report_error",
    description="Report an error to the server",
    func=report_error,
)
#-------------------------------------------------------

def update_suricata_rulee(rule: str):
    """update the suricata rule"""
    try:
        with open("suricata_riles.txt",'a') as file:
            file.write(rule+"\n")
        return "Suricata rule updated successfully."
    except Exception as e:
        return f"Failed to update suricata rule: {str(e)}"

update_suricata_rule_tool = Tool(
    name = "update_suricata_rule",
    description="Update the suricata rule",
    func=update_suricata_rulee,
)
#-------------------------------------------------------

