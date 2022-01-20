#!/usr/bin/env python3

from json.decoder import JSONDecodeError
from lib.client import client
from lib.util import pretty_print
import typing as t
import argparse
import json
import time


def _exec_raw(id: str, command: list[str]) -> t.Tuple[int, str]:
    containers: list[t.Any] = client.containers.list()
    container: t.Any = next(c for c in containers if c.name == id)
    print(f"{id} ({container.id[:5]}): {' '.join(command)}")
    code, output = container.exec_run(command, stdin=True, tty=True)
    return code, output.decode()


def _check_code(code: int) -> None:
    if code != 0:
        exit(code)


# TODO In theory, it would be nice if for the lnd containers the default command was lncli, and for the
# bitcoin container it was bitcoind and then you had to specify it manually otherwise
def exec(id: str, command: str, params: list[str]) -> t.Any:
    if command == "lncli":
        params = ["--network=regtest", "--no-macaroons", *params]
    if command == "bitcoin-cli":
        params = ["-rpcport=43782", "-rpcuser=user", "-rpcpassword=pass", *params]

    while True:
        code, output = _exec_raw(id, [command, *params])

        known_errors = ["before the wallet is fully synced", "server is still in the process of starting"]
        if code != 0 and any(e in output for e in known_errors):
            print(f"{output.strip()}, retrying...")
            time.sleep(2)
        else:
            break

    try:
        response = json.loads(output)
        pretty_print(response)
        _check_code(code)
        return response
    except JSONDecodeError:
        print(output)
        _check_code(code)
        return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute an lncli command.")
    parser.add_argument("id", type=str, help="container name")
    parser.add_argument("command", type=str, help="command to execute")
    args = parser.parse_args()

    command, *params = args.command.split()
    exec(args.id, command, params)
