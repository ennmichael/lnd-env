#!/usr/bin/env python3

import argparse
from open_channel import open_channel
from lib.containers import LND_A_CONTAINER, LND_B_CONTAINER, LND_C_CONTAINER
from mine_blocks import mine_blocks


def setup() -> None:
    mine_blocks(500, LND_A_CONTAINER)
    mine_blocks(500, LND_B_CONTAINER)
    mine_blocks(500, LND_C_CONTAINER)
    open_channel(LND_A_CONTAINER, LND_B_CONTAINER, 100000, 50000)
    open_channel(LND_B_CONTAINER, LND_C_CONTAINER, 100000, 50000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup the cluster by funding and connecting nodes")
    setup()
