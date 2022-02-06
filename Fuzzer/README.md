# Fuzzer

Multithreaded Python Fuzzer used to analyze the gRPC endpoints offered by the [Dash-API](https://github.com/dashevo/platform/tree/master/packages/dapi).
Supports both the Dash TestNet and a local DevNet once a correct set of Masternode IP addresses has been supplied.

## Installation

Requires Python above version 3.

```sh
sudo snap install protobuf --clasic
pip install –upgrade protobuf

git clone --recursive https://github.com/trailofbits/protofuzz
cd protofuzz
python3 setup.py install
```

## Usage

Sadly there is no automatic masternode IP setup so you will likely have to configure your own masternode IP addresses. The ones listed were working until the 24th of December 2021.
The files to adjust would be `masternode_ips.txt` or `masternode_ips_devnet.txt` depending on which mode you're using.

For the fuzzer you can simply run `python fuzzer.py` or `python evaluation.py` in order to run the evaluation script.

## Dependencies

- [protofuzz](https://github.com/trailofbits/protofuzz)

## Contributing

Feel free to open an issue regarding any questions that might come up.

## License

MIT @ Dash-MProject-Group