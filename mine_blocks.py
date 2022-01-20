#!/usr/bin/env python3

from lib.containers import BITCOIN_CONTAINER
from lib.util import pretty_print
import typing as t
import argparse
from exec import exec


_DEAD_ADDRESS = "bcrt1qgq4c3n9uxye5lxhcxphevj9xsytrv4nhrnjw4v"


def mine_blocks(num_blocks: int = 1, container_id: str | None = None) -> t.Any:
    if container_id is not None:
        address_response = exec(container_id, "lncli", ["newaddress", "p2wkh"])
        address = address_response["address"]
    else:
        address = _DEAD_ADDRESS
    return exec(BITCOIN_CONTAINER, "bitcoin-cli", ["generatetoaddress", str(num_blocks), address])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mine blocks.")
    parser.add_argument("--count", type=int, help="number of block to mine", default=1)
    parser.add_argument("--target", type=str, help="LND container ID to mine into")
    args = parser.parse_args()

    response = mine_blocks(args.count, args.target)
    pretty_print(response)
