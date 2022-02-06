## Dash Core Stress-Test Script
This small Python script allows you to run a stresstest on a running Dash-Node. It requires a locally running dashd. Also the dashd has to be reachable via the standard dash-cli. The script creates valid transactions as fast as possible in parallel and sends them to the reachable Dash-Network via the locally running dashd.

### Usage
Python 3.6 or higher is required.

Run: `>_ python3 tx_dos_simple.py`

You can adjust the amount of transactions to be sent via the `TX_PER_THREAD` constant.
The script creates a logging file automatically.

If you also want to monitor the stats of the mempool, you can run `>_ python3 mempool_monitor.py`
This dumps the stats of the local mempool into a CSV-file periodically.
