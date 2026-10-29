from wake.testing import *

from pytypes.contracts.ClubVault import ClubVault, Refuser


# Print the call trace of a failing transaction
def revert_handler(e: RevertError):
    if e.tx is not None:
        print(e.tx.call_trace)


# ClubVault has six bugs, one for each exploit from the slides. For each one, write a test
# that makes the bug happen and assert what really happens.
# Prove all five: 1 bonus point. Prove the reentrancy (the last one): 1 more bonus point.


# ---------------------------------------------------------------- 1. access control

@chain.connect()
@on_revert(revert_handler)
def test_anyone_can_become_owner():
    owner, alice, bob, mallory = chain.accounts[0:4]
    vault = ClubVault.deploy(from_=owner)
    vault.deposit(from_=alice, value="5 ether")
    vault.deposit(from_=bob, value="5 ether")

    # TODO: Mallory is not the owner. Can she take Alice's and Bob's 10 ETH?
    #       Look at which functions have onlyOwner, and which don't.
    pass


# ---------------------------------------------------------------- 2. underflow

@chain.connect()
@on_revert(revert_handler)
def test_points_underflow():
    owner, alice = chain.accounts[0:2]
    vault = ClubVault.deploy(from_=owner)
    vault.deposit(from_=alice, value="1 ether")      # 10 points

    # TODO: Alice has 10 points and spends 15. How many points does she have now?
    pass


# ---------------------------------------------------------------- 3. rounding

@chain.connect()
@on_revert(revert_handler)
def test_share_rounds_to_zero():
    owner, alice, bob = chain.accounts[0:3]
    vault = ClubVault.deploy(from_=owner)
    vault.deposit(from_=alice, value="1 ether")
    vault.deposit(from_=bob, value="1 ether")

    # TODO: Alice owns half of the 2 ETH, so her share should be 1 ETH. What does shareOf say?
    pass


# ---------------------------------------------------------------- 4. denial of service

@chain.connect()
@on_revert(revert_handler)
def test_one_winner_blocks_everyone():
    owner, alice, bob = chain.accounts[0:3]
    vault = ClubVault.deploy(from_=owner)
    refuser = Refuser.deploy(from_=owner)            # a contract without receive(): it refuses ETH

    # TODO: Alice, the refuser and Bob win. The owner pays them 3 ETH with payWinners.
    #       Does anyone get paid? What if the owner tries again?
    pass


# ---------------------------------------------------------------- 5. front-running

@chain.connect()
@on_revert(revert_handler)
def test_bot_copies_the_answer():
    owner, alice, bot = chain.accounts[0:3]
    vault = ClubVault.deploy(from_=owner)
    vault.setPuzzle(keccak256(b"festival"), from_=owner, value="1 ether")

    # TODO: Alice sends solve("festival"). The bot reads it in the mempool and pays a higher
    #       tip, so its copy runs first. In a test you choose the order yourself.
    #       Who gets the 1 ETH, and what happens to Alice's call?
    pass


# ---------------------------------------------------------------- bonus: reentrancy

@chain.connect()
@on_revert(revert_handler)
def test_drain_the_vault():
    owner, alice, bob, attacker = chain.accounts[0:4]
    for a in (alice, bob, attacker):
        a.balance = Wei.parse("10 ether")

    vault = ClubVault.deploy(from_=owner)
    vault.deposit(from_=alice, value="5 ether")
    vault.deposit(from_=bob, value="5 ether")

    # TODO (bonus): like the bank in class. Write contracts/ClubAttacker.sol, run
    #       `wake up pytypes`, import it here and take everything from the vault.
    pass
