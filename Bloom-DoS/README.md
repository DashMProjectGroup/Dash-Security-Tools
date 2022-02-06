# Bloom-DoS

Script to stress the tx-filter-stream with multiple requests uding special bloom filters, effectively requesting all transactions of the entire blockchain.

## Installation

Requires NodeJS above version 12.xx.

To install the necessary dependencies run:
```
npm install
```

## Usage

First you will have to configure the `bloomDoSv2.js` file.
There are four constants with mostly self-explanatory names. clusterMode can be set to true to enable multi-threading. Each thread issues 1000 API calls (hard coded at the very bottom of the file)

Use `npm start` to execute the script.

## Contributing

Feel free to open an issue regarding any questions that might come up.

## License

MIT @ Dash-MProject-Group