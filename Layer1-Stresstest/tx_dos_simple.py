import threading
from os import system, remove
import random
import logging
import requests
import json
import csv
import time
import os

ESTIMATED_TX_SIZE = 250
TX_PER_THREAD = 5000
DASH_PER_TX = 100 / 10000000
addresses = ['yfLWMTzFL6XA3bG6H2HuoY8wMqGtgdZAgQ',
             'yWveuFN8okNRUukRA3jpXQgJZGi2picGo3',
             'yeC62idh355LqTA25YN7QfTHuiaZpN7wdC'
             ]

CSV_FILE = "mempool.csv"





class Tx_thread(threading.Thread):

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.sent_tx = 0

    def run(self):
        for i in range(TX_PER_THREAD):
            system(f"dash-cli sendtoaddress {random.choice(addresses)} {DASH_PER_TX} > /dev/null")
            self.sent_tx = self.sent_tx + 1
            if i % 100 == 0:
                logging.info(f"Thread {self.id} sent {self.sent_tx}, totalling about {self.sent_tx * ESTIMATED_TX_SIZE} Bytes in Size")


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='tx_dos.log', level=logging.DEBUG)
    send_threads = []
    for i in range(10):
        send_threads.append(Tx_thread(i))
    
    for thread in send_threads:
        thread.start()


if __name__ == "__main__": main()
