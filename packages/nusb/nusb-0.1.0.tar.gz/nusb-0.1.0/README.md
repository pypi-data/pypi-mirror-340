# `python-nusb`

Python bindings to [`nusb`](https://docs.rs/nusb/latest/nusb/).

## Hardware in the loop tests

Hardware in the loop tests assume a [Cynthion](https://cynthion.readthedocs.io/) running [Facedancer](https://facedancer.readthedocs.io/) is connected.
Both the control and the target C port must be connected.

To run the tests, ensure dependencies are installed with `pdm install -dG test`, then run `pdm test`.
