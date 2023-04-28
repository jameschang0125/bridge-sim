# bridge-sim

## general setup

- `mkdir data`
    - or you might want to do `mkdir /tmp/data && ln -s /tmp/data data`

## building cpp

- `cd cpp`
- you might want to add `CC_BOOST_LINK` in Makefile
- depends on system, you might need to rebuild `libdds.a`
- you might want to change some parameters in `main.cpp`
- to test, run `make test && ./test`
- run `make && ./main` should generate two files `deal` and `res` under `../data`, which can be used afterwards

## building py

- install some required packages
- `main.py` shows a example of running logistic regression on "8+ trump fit -> game?"

## references

- [dds](https://github.com/dds-bridge/dds)