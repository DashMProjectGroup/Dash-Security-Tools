#!/usr/bin/env node

// npm install @dashevo/dapi-client
// npm install @dashevo/cluster

// enter your DAPI masternode IP address here
const DAPIhost = '127.0.0.1';
const jsonRPCPort = 3000;
const gRPCPort = 3006;
const clusterMode = true;

if (clusterMode) {
    const totalCPUs = require('os').cpus().length;
    const cluster = require('cluster');
    if (cluster.isMaster) {
        console.log(`Number of CPUs is ${totalCPUs}`);
        console.log(`Master ${process.pid} is running`);

        // Fork workers.
        for (let i = 1; i < totalCPUs; i++) {
            cluster.fork();
        }

        cluster.on('exit', (worker, code, signal) => {
            console.log(`worker ${worker.process.pid} died`);
            console.log("Let's fork another worker!");
            cluster.fork();
        });

    } else {
        console.log(`Worker ${process.pid} started`);
    }

}

const DAPIClient = require('@dashevo/dapi-client');

var client = new DAPIClient({
    dapiAddresses: [
        DAPIhost + ':' + jsonRPCPort + ':' + gRPCPort
    ],
});

async function run(worker, m, n) {
    console.log(worker + ", " + m + ", " + n)
    const filter = {
        "nHashFuncs": 11,
        "vData": [],
        "nTweak": 0,
        "nFlags": 0
    }; // A BloomFilter object
    const stream = await client.core.subscribeToTransactionsWithProofs(filter, {
        fromBlockHeight: 1
    });

    let errored = false;
    stream
        .on('data', (response) => {
            // console.log("data response");
            if (errored) {
                console.log("continues after error")
            }
        })
        .on('error', (err) => {
            console.log("error", err);
            errored = true;
        }).on('status', function (status) {
            console.log("status: ", status.code, status.details, status.metadata);
        }).on('end', function (end) {
            console.log("stream ended, restarting ...");
            run(worker, m, n + 1);
        });
}

for (var i = 0; i < 1000; i++) {
    run(process.pid, i, 0);
}
