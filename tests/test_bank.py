from wake.testing import *

from pytypes.contracts.SimpleBank import SimpleBank


# Print the call trace of a failing transaction
def revert_handler(e: RevertError):
    if e.tx is not None:
        print(e.tx.call_trace)


# The example we write together in class.

# ---------------------------------------------------------------- the normal case

@chain.connect()
@on_revert(revert_handler)
def test_deposit():
    alice, bob = chain.accounts[0:2]                 # the first 2 of Wake's 10 test accounts
    bank = SimpleBank.deploy(from_=alice)

    tx = bank.deposit(from_=bob, value="1 ether")

    assert bank.balances(bob) == Wei.parse("1 ether")
    assert bank.getBalance() == Wei.parse("1 ether")
    assert SimpleBank.Deposit(bob.address, Wei.parse("1 ether")) in tx.events
    print("deposit() used", tx.gas_used, "gas")

    with must_revert(Error("deposit amount must be positive")):
        bank.deposit(from_=bob, value=0)


@chain.connect()
@on_revert(revert_handler)
def test_withdraw():
    alice, bob = chain.accounts[0:2]
    bank = SimpleBank.deploy(from_=alice)
    bank.deposit(from_=bob, value="2 ether")

    # TODO (in class): Bob withdraws 0.5 ETH. Check his balance in the bank, his ETH,
    #       the Withdraw event, and that withdrawing more than he has reverts.
    pass


# ---------------------------------------------------------------- the attack

@chain.connect()
@on_revert(revert_handler)
def test_drain_the_bank():
    alice, bob, attacker = chain.accounts[0:3]
    for a in (alice, bob, attacker):
        a.balance = Wei.parse("10 ether")                    # a known start, so balances are easy to check

    bank = SimpleBank.deploy(from_=alice)
    bank.deposit(from_=alice, value="5 ether")
    bank.deposit(from_=bob, value="5 ether")

    # TODO (in class): the attacker is a contract, contracts/BankAttacker.sol. We write it
    #       together, run `wake up pytypes`, import it here and take Alice's and Bob's ETH.
    pass
