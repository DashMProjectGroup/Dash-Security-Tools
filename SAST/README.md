# SAST-Tools
Information on the used tools such as installation and usage.
## Semgrep
Semgrep is a fast, open-source, static analysis tool for finding bugs and enforcing code standards at editor, commit, and CI time.
## npm-audit
The audit command submits a description of the dependencies configured in your project to your default registry and asks for a report of known vulnerabilities.
## Installation
### Semgrep

Installation of Semgrep on Linux:
```
pip install semgrep
```
or

```
python3 -m pip install semgrep
```

Enforce global installation:

```
sudo -H python3 -m pip install semgrep
```

### npm-audit
Some DAPI dependencies require NodeJS >= 12.9:
```
# remove old versions
sudo apt-get purge node-* nodejs* npm*
# install curl (if not installed)
sudo apt-get install curl
# instructions from https://github.com/nodesource/distributions#debinstall
curl -fsSL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Install the dapi and requirements (cmake):
```
sudo apt-get install cmake
git clone https://github.com/dashevo/dapi.git
cd dapi
npm install 
```

## Usage
### Semgrep

```
semgrep  --config "p/nodejsscan" --config "p/nodejs"
```

To write the results to a file:
```
semgrep  --config "p/nodejsscan" --config "p/nodejs" > out.txt
```

The rulesets `nodejs` and `nodejsscan` contain rules that identify common security vulnerabilities.


## Contributing

Feel free to open an issue regarding any questions that might come up.

## License

MIT @ Dash-MProject-Group