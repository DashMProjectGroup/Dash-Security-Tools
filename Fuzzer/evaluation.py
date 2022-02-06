#!/bin/python3
# evaluation script for the fuzzer results

from sys import argv
from os import path as p
from os import makedirs as mkdir
from glob import glob
import json, re

STATUS_CODE = re.compile("StatusCode\.[A-Z_]+")
CREATED = re.compile("@[0-9]+.[0-9]+")
DETAILS = re.compile("\(not '.+'\)")
IPS = re.compile("ipv4:[0-9]+.[0-9]+.[0-9]+.[0-9]+:3010")

DUMP_ERROR = ["UNAVAILABLE", "INTERNAL", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED"]

def main():
    if len(argv) != 2:
        print("Invalid argument: Usage {} <FOLDER_WITH_FUZZER_LOGS>".format(argv[0]))
        exit(-1)

    if not p.exists(argv[1]):
        print("Invalid path: {} - Please specify a path that points to the logs of the fuzzer.".format(argv[1]))
        exit(-1)

    if not ("testnet" in argv[1] or "devnet" in argv[1]):
        print("Invalid naming - folder of logs must contain testnet or devnet to decide fuzz source of data.")
        exit(-1)

    for file in glob(p.join(argv[1], "*.txt")):
        print("Processing: {}".format(file))
        process(file, "testnet" in argv[1])
        print("")

def process(file, testnet):
    failed = 0
    success = 0
    error_codes = {}
    anomalies = []
    dumped_hashes = {}
    grouped_error_messages = {}

    with open(file, "r") as f:
        j = json.load(f)
    
    print("Loaded: {} data points.".format(len(j)))

    for dp in j:
        if dp["exception"]:
            failed += 1
            match = STATUS_CODE.findall(dp["returned"])
            if match:
                result = match[0].replace("StatusCode.", "")
                if result in error_codes:
                    error_codes[result] = error_codes[result] + 1
                else:
                    error_codes[result] = 1
                
                if result in DUMP_ERROR:
                    dp["returned"] = CREATED.sub("replaced for easier evaluation", dp["returned"]) # replace created-field to group error messages
                    dp["returned"] = DETAILS.sub("not the provided input (input replaced for easier evaluation)", dp["returned"]) # replace input payload in returned to group messages
                    dp["returned"] = IPS.sub("Peer-Adress replaced for easier evaluation", dp["returned"]) # replace peer IPs to group messages

                    found = False
                    for k in grouped_error_messages:
                        if grouped_error_messages[k]["error_returned"] == dp["returned"]:
                            grouped_error_messages[k]["count"] += 1
                            grouped_error_messages[k]["occuredByInput"].append(dp["payload"])
                            found = True
                            break
                    if not found: 
                        grouped_error_messages[len(grouped_error_messages)] = {
                            "error_returned": dp["returned"],
                            "count" : 1,
                            "occuredByInput": [dp["payload"]]
                    }

                    if result in dumped_hashes:
                        dumped_hashes[result].append(dp["payload_hash"])
                    else:
                        tmp = []
                        tmp.append(dp["payload_hash"])
                        dumped_hashes[result] = tmp
            else:
                print("Anomaly detected :: NO_ERROR_CODE -> {} | {}".format(dp["payload_hash"], dp["returned"]))
                anomalies.append(dp["payload_hash"])
        else:
            success += 1
    
    folder = "logs_testnet_analyzed" if testnet else "logs_devnet_analyzed"
    if not p.exists(folder):
        mkdir(folder)

    write_into = folder + "/" + p.basename(file)[:-4] + "_analyzed.json"
    with open(write_into, "w") as f:
        json.dump({
            "ID": p.basename(file)[:-4],
            "TESTNET": testnet, 
            "REQUESTS": len(j),
            "SUCCESS": success,
            "EXCEPTION": failed,
            "SUCCESS_QUOTA": 1.0*success/len(j),
            "EXCEPTION_QUOTA": 1.0*failed/len(j),
            "ERROR_CODES_RAW_DISTRIBUTION": error_codes,
            "ERROR_CODES_QUOTA_DISTRIBUTION": calcErrCodeDist(error_codes, len(j)-success),
            "ANOMALY_COUNT": len(anomalies),
            "ANOMALY_HASHES": anomalies,
            "OCCURED_ERROR_MESSAGES": grouped_error_messages,
            "DUMPED_HASHES": dumped_hashes  
        }, f, indent=True)
    print("Result persisted in {}...".format(write_into))

def calcErrCodeDist(error_codes, n):
    if len(error_codes) == 0:
        return {}

    tmp = {}
    for k in error_codes:
        tmp[k] = 1.0*error_codes[k]/n

    return tmp

if __name__ == "__main__":
    main()
