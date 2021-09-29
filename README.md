# Elects

Elects is a simple command line utility, which shows simple charts of elects by given name of Czech village. It searches the Czech villages, if there is more than 1 village with such name (which is pretty common in Czech republic), it will ask you to choose for the exact one you want to show charts for. Make sure to download the whole folder or use the git clone :-)

## Usage

No installation of extra modules required, you should be able to run this on anything.
There are 2 options to run this:

> with a "name" parameter (call it like -n VILLAGE or --name VILLAGE)
```sh
python3 elects.py --name "Bechovice"
```
> without any paramater, the script will ask you later on for your input
```sh
python3 elects.py
```

Of course you can access the help with calling -h or --help
> 
```sh
python3 elects.py -h
```
## Extra
The search for villages is cAsE + accents insensitive, so you can search for your desired village name without any struggle.
If there is a certainity of exactly 1 village, no need to choose it, the chart will be shown directly.
## License
MIT
