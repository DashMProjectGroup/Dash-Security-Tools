# dash-pentest

This repository contains a variety of tools written for the purpose of testing the cryptocurrency project Dash for potential security vulnerabilites and related issues.
For more information on a specific tool, please take a look at the specific read me file.

# Tools

- Fuzzer
  - Multithreaded Python Fuzzer for the [DAPI](https://github.com/dashevo/platform/tree/master/packages/dapi) gRPC endpoints using [protofuzz](https://github.com/trailofbits/protofuzz).
  - Includes a script to evaluate the results.
- Dash Core Stresstest
  - Tool to flood a Dash-Network with an arbitrary amount of transactions
  - Implemented in Python 3 with multithreading
  - Also comes with a monitoring tool for the local Mempool
- DPNS-Tester
  - TypeScript scripts used to validate DPNS-Contract integrity (specifically name validation).
  - Multithreaded identity alias generation script to test a potential Denial-of-Service vulnerability.
- Bloom DoS
  - Node.js based stress test attacking the tx-filter-stream
  - Issues multiple special requests that cause a lot of load

## Results

- SAST reports
  - Static code anlysis using [npm-audit](https://docs.npmjs.com/cli/v8/commands/npm-audit) and [semgrep](https://github.com/returntocorp/semgrep)

## Contribution

Feel free to create an issue for any questions that come up regarding our tools, we would be happy to answer them.

## License

MIT @ Dash-MProject-Group 
