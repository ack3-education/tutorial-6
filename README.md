# Tutorial 6: Security

Find the bug, prove it with a test, fix it. Everything here runs with
[Wake](https://github.com/ack3-ai/wake) 5.

## Install Wake (once)

You need Python 3.10 or newer ([python.org/downloads](https://www.python.org/downloads/)).
Plain `pip install eth-wake` installs the older Wake 4, so name the version.

Windows (PowerShell or cmd):

```powershell
pip install eth-wake==5.0.0rc4
wake --version
```

If `wake` is not found, Python was installed without being added to PATH: reinstall it and tick
**Add python.exe to PATH**.

Linux and macOS (the system Python refuses `pip install` for programs, so use pipx):

```bash
sudo apt install pipx             # macOS: brew install pipx
pipx ensurepath                   # then open a new terminal
pipx install eth-wake==5.0.0rc4
wake --version
```

## Run it

```bash
wake up pytypes                                   # compile and generate pytypes/; again after every Solidity change
wake test                                         # all tests: 9 pass before you start
wake test tests/test_club_vault.py                # one file
wake test -s tests/test_bank.py::test_deposit     # one test, with your print() output
```

`wake.toml` sets `cmd = "revm"`: Wake runs its own chain, so you don't need anything else.
Warnings about files inside Wake's own folder (`...site-packages/wake/contracts/...`) can be ignored.

## What is in it

| Path | What |
|:--|:--|
| `contracts/SimpleBank.sol` | the example: we test it and break it together in class |
| `contracts/ClubVault.sol` | your exercise: one contract, six bugs |
| `tests/test_bank.py` | `test_deposit` is written; `test_withdraw` and `test_drain_the_bank` we write in class |
| `tests/test_club_vault.py` | your tests: the setup is written, you write the rest |

## Your exercise: ClubVault

| # | Test | The question |
|:--|:--|:--|
| 1 | `test_anyone_can_become_owner` | Mallory is not the owner. Can she take everything? |
| 2 | `test_points_underflow` | Alice has 10 points and spends 15. How many are left? |
| 3 | `test_share_rounds_to_zero` | Alice owns half of 2 ETH. What does `shareOf` say? |
| 4 | `test_one_winner_blocks_everyone` | One winner refuses ETH. Does anyone get paid? |
| 5 | `test_bot_copies_the_answer` | A bot copies Alice's answer. Who gets the prize? |
| bonus | `test_drain_the_vault` | Reentrancy, like the bank: write your own attacker contract |

**Bonus points:** prove all five, +1. Prove the reentrancy, +1.

For each one: read the contract, write a test that makes the bug happen and `assert` what
really happens, run it alone with `wake test -s tests/test_club_vault.py::<test name>`, then fix
the contract (`wake up pytypes`) and change the test so it expects the safe behaviour.

## Coverage (for the semestral task)

```bash
wake test --cov 1 tests/test_bank.py
```

This writes `wake-coverage.cov`. In VS Code, with the Solidity (Wake) extension, press
`Ctrl+Shift+P` and run **Show Coverage**. A modifier's `_;` always shows as not covered.

## Cheat sheet

| You want to | In Wake |
|:--|:--|
| more than 10 accounts | `@chain.connect(accounts=50)`, or `Account.new()` (starts with 0 ETH) |
| send from an account, attach ETH | `bank.deposit(from_=bob, value="1 ether")` |
| pass an amount as an argument | `bank.withdraw(Wei.parse("0.5 ether"), from_=bob)` |
| send plain ETH, no function | `contract.transact(value="1 ether", from_=bob)` |
| expect a revert with a message | `with must_revert(Error("insufficient balance")):` |
| expect a custom error / a panic | `must_revert(MyContract.NotOwner)` / `must_revert(PanicCodeEnum.UNDERFLOW_OVERFLOW)` |
| check an event | `SimpleBank.Deposit(bob.address, Wei.parse("1 ether")) in tx.events` |
| hash a string like Solidity | `keccak256(b"festival")` |
| move time | `chain.mine(lambda t: t + 3600)` |
| set a balance | `alice.balance = Wei.parse("10 ether")` |
| see what happened | `print(tx.call_trace)`, `tx.gas_used` |
| run the detectors | `wake detect all` |

Don't name a helper function `setup`: pytest runs a function with that name before Wake's chain
exists.

Docs: [ack3.ai/wake/docs](https://ack3.ai/wake/docs/latest).
