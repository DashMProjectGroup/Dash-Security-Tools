# DPNS-Tester

TypeScript scripts used to validate and test the Dash Platform Name Service (DPNS) functionality.

Current version was used to generate a lot of names for a specified wallet identity in order to test a potential Denial-of-Service vulnerability using the wildcard name search.

## Installation

Requires NodeJS above version 12.xx.

To install the necessary dependencies run:
```sh
npm i
```

## Usage

First you will have to configure the `src/index.ts` file.
There are instructions on what values to put and where to get them in case you don't have them already.

Once you've configured the script properly, you can just run it using:
```sh
npm start
```

This will trigger the TypeScript compilation and run the resulting script.

## Dependencies

- [dashsdk](https://github.com/dashevo/platform/tree/master/packages/js-dash-sdk)

## Contributing

Feel free to open an issue regarding any questions that might come up.

## License

MIT @ Dash-MProject-Group