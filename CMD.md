initialize a project with brownie

```sh
brownie init
```

brownie run a specific test in brownie

```sh
brownie test -k name_of_that_test --network=name_of_that_network
```

brownie run test and show print statements

```sh
brownie test -s --network=name_of_that_network
```

brownie run all test

```sh
brownie test --network=name_of_that_network
```

compile with brownie

```sh
brownie compile
```

brownie running a script

```sh
brownie run scripts/script-name.py --network network-name
```

delete network from brownie

```sh
brownie networks delete name-of-network
```

list all the networks

```sh
brownie networks list
```

add a mainnet fork
surrond the fork with single quote if reading from .env file

```sh
brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork='GET_FROM_ENV' accounts=10 mnemonic=brownie port=8545
```
