# bridge-sim

## general setup

- `mkdir data`

## build cpp

- `cd cpp`
- change `CC_BOOST_LINK` in Makefile
- change the path in main.cpp
- depends on system, you might need to rebuild `libdds.a`
- to test, run `make test && ./main`

## extern libs

- [dds](https://github.com/dds-bridge/dds)