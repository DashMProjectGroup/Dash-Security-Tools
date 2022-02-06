import core_pb2_grpc, platform_pb2_grpc
import grpc, json, hashlib, time, socket, multiprocessing 
from protofuzz import protofuzz
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
from math import ceil

MAX_THREADS = multiprocessing.cpu_count()
# set to true to fuzz core endpoints
FUZZ_CORE = True
# set to true to fuzz platform endpoints
FUZZ_PLATTFORM = True
# set to true if you want to perform the tests on a local devnet
LOCAL_DEVNET = False

DEBUG_BREAK_AFTER_ITTER = False
BREAK_TIME = 500 #ms - time between requests to the same masternode
REQUEST_TIMEOUT = 5 #s
MINIMUM_AMOUNT_TO_CHUNK = 20000
CHUNK_SIZE = 10000


message_fuzzers_core = protofuzz.from_file('core.proto')
message_fuzzers_platform = protofuzz.from_file('platform.proto')

core_endpoints = [ ["GetTransactionRequest", [], 12417], ["GetBlockRequest", [], 136587], ["BroadcastTransactionRequest", [], 49668], ["TransactionsWithProofsRequest", [], 1000000] ]
platform_endpoints = [ ["BroadcastStateTransitionRequest", [], 12417], ["GetIdentityRequest", [], 24834], ["GetDataContractRequest", [], 24834],
                    ["GetDocumentsRequest", [], 1000000], ["GetConsensusParamsRequest", [], 24], ["GetIdentitiesByPublicKeyHashesRequest", [], 24834],
                    ["GetIdentityIdsByPublicKeyHashesRequest", [], 24834], ["WaitForStateTransitionResultRequest", [], 24834] ]

masternodes = list()
ip_path_suffix = "_devnet" if LOCAL_DEVNET else "" 
f=open('masternode_ips{}.txt'.format(ip_path_suffix),'r')
for ip in f.read().splitlines():
    masternodes.append(ip)
f.close()

# save data of the given report in the logfile of the given endpoint
def dumpIt(report, endpoint, end):
    folder_suffix = "_devnet" if LOCAL_DEVNET else ""
    with open("./logs{}/{}.txt".format(folder_suffix, endpoint[0]), "w") as f:
        json.dump(report, f)

    # free memory when finished
    if end == endpoint[2]:
        endpoint[1] = []


def fuzz():
    targets = []

    if FUZZ_CORE:
        targets.extend(core_endpoints)
    if FUZZ_PLATTFORM:
        targets.extend(platform_endpoints)

    core_endpoints_ids = [x[0] for x in core_endpoints]
    print(Fore.GREEN + "Fuzzing {} endpoint(s)\n".format(len(targets)))

    executor = ThreadPoolExecutor(max_workers=MAX_THREADS)

    i = 0
    for endpoint in targets:
        is_core = endpoint[0] in core_endpoints_ids
        fuzzer_messages = message_fuzzers_core if is_core else message_fuzzers_platform
        total_requests = endpoint[2]
        if total_requests >= MINIMUM_AMOUNT_TO_CHUNK:
            chunk_amount = ceil(total_requests / CHUNK_SIZE)
            for x in range(chunk_amount):
                # define worker ranges
                start = x * CHUNK_SIZE
                end = (x + 1) * CHUNK_SIZE
                node_address = masternodes[i % len(masternodes)]
                executor.submit(worker, fuzzer_messages=fuzzer_messages, endpoint=endpoint, is_core=is_core, node_address=node_address, start=start, end=end)
                print(Fore.GREEN + "Submitted {} to executor pool. [{}/{}]".format(endpoint, i, len(targets)))
                i += 1
        else:
            executor.submit(worker, fuzzer_messages=fuzzer_messages, endpoint=endpoint, is_core=is_core, node_address=masternodes[i % len(masternodes)], start=0, end=total_requests)
            print(Fore.GREEN + "Submitted {} to executor pool. [{}/{}]".format(endpoint, i, len(targets)))
            i += 1

        print(Fore.GREEN + "Executor work queue: {}".format(executor._work_queue.qsize()))
        


def worker(fuzzer_messages, endpoint, is_core, node_address, start, end):
    print(Fore.GREEN + "Starting worker with start: {} and end: {}".format(start, end))
    port = "3005" if LOCAL_DEVNET else "3010"
    channel = grpc.insecure_channel(node_address + ":" + port)
    stub = core_pb2_grpc.CoreStub(channel) if is_core else platform_pb2_grpc.PlatformStub(channel)

    i = 0
    report = endpoint[1]

    for obj in fuzzer_messages[endpoint[0]].permute():
        i += 1
        if i - 1 < start:
            continue
        if i - 1 == end:
            break
        request_start = int(time.time() * 1000)
        print(Fore.GREEN + "[{}] Generated object Nr. {}".format(endpoint[0], i))
        hs = hashlib.sha256(str(obj).encode('utf-8')).hexdigest()
        try:
            response = getResponseByEndpoint(endpoint[0], stub, obj)
            report.append({"exception": False, "payload": str(obj), "returned": str(response), "payload_hash": hs})
        except Exception as e:
            report.append({"exception": True, "payload": str(obj), "returned": repr(e), "payload_hash": hs})
        if DEBUG_BREAK_AFTER_ITTER:
            break
        time_diff = int(time.time() * 1000) - request_start

        if(time_diff <= BREAK_TIME):
            time.sleep((BREAK_TIME - time_diff) / 1000)

    # store after each chunk!
    dumpIt(report, endpoint, end)


# executes the correct function for the given endpoint and returns the response
def getResponseByEndpoint(endpoint, stub, obj):
    if (endpoint == "GetTransactionRequest"):
        return stub.getTransaction(obj, REQUEST_TIMEOUT)
    if (endpoint == "GetBlockRequest"):
        return stub.getTransaction(obj, REQUEST_TIMEOUT)
    if (endpoint == "BroadcastTransactionRequest"):
        return stub.broadcastTransaction(obj, REQUEST_TIMEOUT)
    if (endpoint == "BlockHeadersWithChainLocksRequest"):
        return stub.subscribeToBlockHeadersWithChainLocks(obj, REQUEST_TIMEOUT)
    if (endpoint == "TransactionsWithProofsRequest"):
        return stub.subscribeToTransactionsWithProofs(obj, REQUEST_TIMEOUT)
    if (endpoint == "BroadcastStateTransitionRequest"):
        return stub.broadcastStateTransition(obj, REQUEST_TIMEOUT)
    if (endpoint == "GetIdentityRequest"):
        return stub.getIdentity(obj, REQUEST_TIMEOUT)
    if (endpoint == "GetDataContractRequest"):
        return stub.getDataContract(obj, REQUEST_TIMEOUT)
    if (endpoint == "GetDocumentsRequest"):
        return stub.getDocuments(obj, REQUEST_TIMEOUT)
    if (endpoint == "GetIdentitiesByPublicKeyHashesRequest"):
        return stub.getIdentitiesByPublicKeyHashes(obj, REQUEST_TIMEOUT)
    if (endpoint == "GetIdentityIdsByPublicKeyHashesRequest"):
        return stub.getIdentityIdsByPublicKeyHashes(obj, REQUEST_TIMEOUT)
    if (endpoint == "WaitForStateTransitionResultRequest"):
        return stub.waitForStateTransitionResult(obj, REQUEST_TIMEOUT)
    if (endpoint == "GetConsensusParamsRequest"):
        return stub.getConsensusParams(obj, REQUEST_TIMEOUT)


def main():
    fuzz()


if __name__ == "__main__":
    main()
