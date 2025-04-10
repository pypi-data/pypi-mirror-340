# -*- coding: utf-8 -*-

import os
import platform
import requests
import json
import chardet
import re
import time

def check_platform(print_infos=False):

    if print_infos is True:
        print("Checking platform ...")
        print("Platform : " + platform.platform())
        print("System   : " + platform.system())

    return platform.system().strip()


def get_project_profiles(tailer_configuration, firebase_user):

    # Call API to retrieve Project Profiles accessible by the user
    #
    try:

        url = tailer_configuration["tailer_api_endpoint"] + "project-profile"
        data = {
            "payload": {
                "uid": firebase_user["userId"]
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]}

        r = requests.post(
                url,
                headers=headers,
                data=json.dumps(data),
                verify=tailer_configuration["perform_ssl_verification"])

        if r.status_code != 200:
            print("\nError : %s\n" % str(r.content, "utf-8"))
            return False, None
        else:
            response = r.json()
            return True, response["payload"]["message"]

    except Exception as ex:
        print("Error while trying to contact Tailer API ...")
        print(ex)
        return False, None


def choose_project_profiles(
        tailer_configuration, 
        firebase_user):

    ret_code, payload = get_project_profiles(
                            tailer_configuration,
                            firebase_user)

    if ret_code is False:
        return False, None
    
    # Display available profiles for the user
    #
    print("")
    print("List of available profiles for you :")
    print("-----------------------------------")
    index = 1

    payload.sort()

    for profile in payload:

        print("{} - {}".format(str(index), profile))
        index += 1
    print("")

    # Ask the user to pick one
    #
    while True:
        print("Please choose a profile by typing its number : ", end='', flush=True)
        user_value = input()

        try:
            user_value = int(user_value)
        except Exception as ex:
            continue

        if (user_value <= len(payload)) and (user_value >= 1):
            break

        continue

    # Infos
    #
    choice = payload[user_value - 1]
    print("\nYou choosed to use profile : {}\n".format(choice))

    return True, choice


def get_available_context_for_user(
        tailer_configuration=None,
        firebase_user=None):

    # Call API
    #
    try:
        url = tailer_configuration["tailer_api_endpoint"] + "configuration/v2"
        data = {
            "payload": {
                "resource_type": "get-context-for-user",
                "uid": firebase_user["userId"]
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]}
            
        retry = 3
        while retry != 0:

            r = requests.post(url, headers=headers, data=json.dumps(
                data), verify=tailer_configuration["perform_ssl_verification"])

            if r.status_code == 404:
                # Not found
                #
                print("\nNo context available for your user.")
                return None
            
            elif r.status_code == 504:
                # Timeout
                #
                print("\ntimeout while retrieving context, re-trying ...")
                retry -= 1
                time.sleep(5)

            elif r.status_code != 200:
                print("\nError(s) : \n%s\n" % str(r.content, "utf-8"))
                return None

            else:
                response = r.json()
                return response["payload"]["message"]

    except Exception as ex:
        print("Error while trying to contact Tailer API ...")
        print(ex)
        return None


def retrieve_context(
        tailer_configuration,
        firebase_user,
        context_id):

    # Call API
    #
    try:

        url = tailer_configuration["tailer_api_endpoint"] + "configuration/v2"
        data = {
            "payload": {
                "resource_type": "retrieve-context",
                "resource": context_id,
                "uid": firebase_user["userId"]
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]}

        r = requests.post(url, headers=headers, data=json.dumps(
            data), verify=tailer_configuration["perform_ssl_verification"])

        if r.status_code == 404:
            # Not found
            #
            print("\nThe context requested is not available.\n")
            return False, None

        elif r.status_code != 200:
            print("\nError(s) : \n%s\n" % str(r.content, "utf-8"))
            return False, None

        else:
            response = r.json()
            return True, response["payload"]["message"]

    except Exception as ex:
        print("Error while trying to contact Tailer API ...")
        print(ex)
        return False, None


def choose_context(
        tailer_configuration,
        firebase_user):

    contexts = get_available_context_for_user(
                    tailer_configuration=tailer_configuration,
                    firebase_user=firebase_user)

    if contexts is None:
        return True, "NO_CONTEXT"
    
    # Display available profiles for the user
    #
    print("")
    print("List of available contexts for you :")
    print("-----------------------------------")
    index = 1

    payload = []
    for key in contexts.keys():
        payload.append(key)

    payload.sort()

    # Add the "no context" option
    #
    payload.append("NO_CONTEXT")
    contexts["NO_CONTEXT"] = {"account":"xxxxxx", "configuration_id": "Do not use any context"}

    for context_key in payload:

        print("{} - {}".format(str(index), contexts[context_key]["account"] + " --> " + contexts[context_key]["configuration_id"]))
        index += 1
    print("")

    # Ask the user to pick one
    #
    while True:
        print("Please choose a context by typing its number : ", end='', flush=True)
        user_value = input()

        try:
            user_value = int(user_value)
        except Exception as ex:
            continue

        if (user_value <= len(payload)) and (user_value >= 1):
            break

        continue

    # Infos
    #
    choice = contexts[payload[user_value - 1]]["account"] + " --> " + contexts[payload[user_value - 1]]["configuration_id"]
    print("\nYou choosed to use context : {}\n".format(choice))

    return True, payload[user_value - 1]


def apply_context(payload, context_data):

    # Parse the user's configuration file and apply context
    #
    try:
        # FD variables
        #
        payload = payload.replace("{{FD_ENV}}", context_data["environment"])
        payload = payload.replace("{{FD_ACCOUNT}}", context_data["account"])
        payload = payload.replace(
                    "{{FD_CONTEXT}}",
                    context_data["account"].strip() \
                    + "_" \
                    + context_data["configuration_id"].strip())

        # Regular variables
        #
        regex = """\"{{([^{]*)}}\""""
        result = re.findall(regex, payload)
        
        for variable in result:
            try:
                print("Parsing variable : {}".format(variable))
                payload = payload.replace("""\"{{""" + variable + """}}\"""", json.dumps(context_data["parameters"][variable]["value"], indent=4, ensure_ascii=False))
            except Exception:
                pass

        # Variables embedded within strings
        # This will replace STRING, INT and FLOAT types only
        #
        regex = """{{([^{]*)}}"""
        result = re.findall(regex, payload)
        
        variable: str
        for variable in result:
            
            # Do not process "protected" variables : FD_*
            # nor TEMPLATE_CURRENT_DATE
            #
            if (variable.startswith("FD_")) \
                or (variable.strip() == "TEMPLATE_CURRENT_DATE"):

                continue

            try:
                print("Parsing variable : {}".format(variable))
                if context_data["parameters"][variable]["type"] in ["string", "integer", "float"]:
                    payload = payload.replace("""{{""" + variable + """}}""", json.dumps(context_data["parameters"][variable]["value"], indent=4, ensure_ascii=False).replace("\"",""))
                else:
                    payload = payload.replace("""{{""" + variable + """}}""", "VARIABLE_TYPE_NOT_SUPPORTED_PLEASE_CHECK_CONTEXT")

            except Exception as ex:
                
                print(f"Error while applying context on the configuration variable {variable}")
                return False, None

        return True, payload

    except Exception as ex:

        print("Error while parsing configuration : {}".format(str(ex)))
        return False, None


def get_path_from_file(
        input_file: str,
        sub_element: str=None):

    # Get path
    #
    filepath = os.path.dirname(input_file)

    host_system = check_platform()

    path_element = None
    if (host_system == "Linux") or (host_system == "Darwin"):
        path_element = "/"
    elif host_system == "Windows":
        path_element = "\\"
    else:
        print("Host OS unknown, cannot process path from file.")
        return None

    if (filepath is None) or (filepath == ""):
        return ""
    else:
        if sub_element is None:
            return (filepath + path_element)
        else:
            return (filepath + path_element + sub_element.strip() + path_element)


def read_file_as_utf_8(full_filename):

    detector = chardet.universaldetector.UniversalDetector()
    with open(full_filename, "rb") as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        
    detector.close()

    detectorEncoding = str(detector.result["encoding"]).strip()

    print(f"encoding detected : {detectorEncoding}")

    if detectorEncoding not in ["UTF-8", "ascii"]:
        print(f"warning : the file {full_filename} is not encoded in UTF-8. Some characters might be transcoded incorrectly. Please consider converting your file to UTF-8.")

    if detector.result["confidence"] <= 0.9:
        encoding = "utf-8"
    else:
        encoding = detectorEncoding

    try:
        with open(full_filename, "r", encoding=encoding) as f:

            data = f.read()

            if len(data) <= 0:
                return None
            
            return data.encode("utf-8")
            
    except Exception as ex:
       
       print(f"warning : the file {full_filename} is not properly encoded in UTF-8. Some characters might be transcoded incorrectly. Please consider coverting your file to UTF-8.")
        
       with open(full_filename, "r", encoding=detectorEncoding) as f:

            data = f.read()

            if len(data) <= 0:
                return None
            
            return data.encode("utf-8")