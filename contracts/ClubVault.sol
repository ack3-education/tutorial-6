// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

/// @title ClubVault
/// @notice The student club's vault. Members deposit ETH and collect points, the owner pays
///         prizes to winners and sets a weekly puzzle with an ETH prize.
/// @dev It has six bugs, one for each exploit from the slides. Prove them in
///      tests/test_club_vault.py.
contract ClubVault {
    address public owner;

    mapping(address => uint256) public deposits;
    uint256 public totalDeposits;
    mapping(address => uint256) public points;

    address[] public winners;

    bytes32 public answerHash;
    uint256 public puzzlePrize;

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // ---------------------------------------------------------------- owner

    function setOwner(address newOwner) external {
        owner = newOwner;
    }

    /// @notice Sends everything in the vault to the owner, in case something goes wrong.
    function emergencyWithdraw() external onlyOwner {
        (bool ok, ) = owner.call{value: address(this).balance}("");
        require(ok, "transfer failed");
    }

    // ---------------------------------------------------------------- deposits

    function deposit() external payable {
        require(msg.value > 0, "nothing sent");
        deposits[msg.sender] += msg.value;
        totalDeposits += msg.value;
        points[msg.sender] += 10;                   // 10 points for every deposit
    }

    function withdraw() external {
        uint256 amount = deposits[msg.sender];
        require(amount > 0, "nothing to withdraw");

        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");

        deposits[msg.sender] = 0;
        totalDeposits -= amount;
    }

    /// @notice How much of the vault's ETH belongs to `member`.
    function shareOf(address member) external view returns (uint256) {
        return deposits[member] / totalDeposits * address(this).balance;
    }

    // ---------------------------------------------------------------- points

    /// @notice Spend points, for example on a club t-shirt.
    function usePoints(uint256 amount) external {
        unchecked {
            points[msg.sender] -= amount;
        }
    }

    // ---------------------------------------------------------------- prizes

    function addWinner(address winner) external onlyOwner {
        winners.push(winner);
    }

    /// @notice The owner sends the prize money with the call; every winner gets the same part.
    function payWinners() external payable onlyOwner {
        uint256 prize = msg.value / winners.length;
        for (uint256 i = 0; i < winners.length; i++) {
            (bool ok, ) = winners[i].call{value: prize}("");
            require(ok, "payment failed");
        }
    }

    // ---------------------------------------------------------------- puzzle

    /// @notice `_answerHash` is keccak256 of the answer. The ETH sent is the prize.
    function setPuzzle(bytes32 _answerHash) external payable onlyOwner {
        answerHash = _answerHash;
        puzzlePrize = msg.value;
    }

    function solve(string calldata answer) external {
        require(answerHash != 0 && keccak256(bytes(answer)) == answerHash, "wrong answer");
        answerHash = 0;                             // only the first one wins

        uint256 prize = puzzlePrize;
        puzzlePrize = 0;
        (bool ok, ) = msg.sender.call{value: prize}("");
        require(ok, "transfer failed");
    }
}

/// @notice A contract without receive(): it refuses plain ETH. Use it as a winner.
contract Refuser {}
