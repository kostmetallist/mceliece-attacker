# McEliece Cryptosystem Attacker

## Descirption

This repo contains Chizhov-Borodin attack implementation on McEliece 
cryptosystem based on Reed-Muller codes.

## How to run

First, you need to install `pipenv` in order to manage virtual environments.
Then, run `pipenv --python 3.8` (or higher) in order to configure your 
environment. To download and extract all the required third-party libraries, 
simply do `pipenv install`.

After configuration actions have been done, enter pipenv shell with `pipenv shell`
and start the main script with `python launch.py`. This command will run
Chizhov-Borodin attacker for cases set in `launch.py`.

To adjust logging granularity, one may want to edit `logging.conf` for manually
setting desired levels, handlers, and formatters for Python's `logging` module.

## Troubleshooting

Please leave all detected issues and possible improvements in the 
[issues](https://github.com/kostmetallist/mceliece-attacker/issues) section.

## Credits

Used [blincodes](https://github.com/a1falcon/blincodes) library for mathematical
operations with vectors, matrices, and Reed-Muller codes; 
[networkx](https://networkx.github.io/) for graph structures and operations;
[scipy](https://www.scipy.org/) for algebraical transformations.
