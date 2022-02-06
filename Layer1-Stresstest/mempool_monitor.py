
import threading
from os import system, remove
import random
import logging
import requests
import json
import csv
import time
import os
import datetime




class Monitoring_thread(threading.Thread):
    
    def __init__(self):
        now = datetime.datetime.now()
        super().__init__()
        self.csv_file = f"mempool{now.day}_{now.month}_{now.year}.csv"
        self.init_csv()

    def run(self):
        while True:
            self.monitor()
            time.sleep(5)



    def monitor(self):
        if os.path.exists("mempool.info"):
            os.remove("mempool.info")
        system("dash-cli getmempoolinfo > mempool.info")
        mempool_info = self.read_info_file(filename="mempool.info")
        logging.info(f"Transactions in Mempool: {mempool_info['size']}. Size of Mempool in bytes: {mempool_info['bytes']}. Memory Usage: {mempool_info['usage']}. Min Relay fee: {mempool_info['minrelaytxfee']}. Min Mempool fee {mempool_info['mempoolminfee']}")
        self.write_to_csv(mempool_info)

    def read_info_file(self, filename):
        with open(filename) as json_file:
            mempool_info = json.load(json_file)
            return mempool_info


    def write_to_csv(self, mempool_info):
        row = [mempool_info['size'], mempool_info['bytes'], mempool_info['usage'], f"{mempool_info['minrelaytxfee']:.9f}"]
        with open(self.csv_file, 'a') as csv_mempool_file:
            writer = csv.writer(csv_mempool_file)
            writer.writerow(row)


    def init_csv(self):
        top_row = ["size", "bytes", "usage", "minrelaytxfee"]
        with open(self.csv_file, 'w') as csv_mempool_file:
            writer = csv.writer(csv_mempool_file)
            writer.writerow(top_row)


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='mempool_monitoring.log', level=logging.DEBUG)
    monitor_thread = Monitoring_thread()
    monitor_thread.start()

if __name__ == "__main__": main()