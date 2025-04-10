import json
from os import listdir
import os

# from solc_ast_parser.enrichment import restore_ast
from solc_ast_parser.enrichment import restore_function_definitions, restore_storages
from solc_ast_parser.models.ast_models import SourceUnit
from solc_ast_parser.models.base_ast_models import NodeType
from solc_ast_parser.utils import (
    compile_contract_with_standart_input,
    update_node_fields,
)
from solc_ast_parser.comments import insert_comments_into_ast
from solc_ast_parser.utils import create_ast_from_source, create_ast_with_standart_input
from solcx.exceptions import SolcError


def create_contract(pseudocode: str) -> str:
    return pseudocode
    # return f"// SPDX-License-Identifier: MIT\npragma solidity ^0.8.28;\ncontract PseudoContract {{\n\n{pseudocode}\n}}"


# ast = create_ast_with_standart_input(vuln_template)
# path = "../../../pycryptor/data/"
# vuln_files = [f for f in listdir(path) if os.path.isfile(os.path.join(path, f)) and not f.startswith("userx-")]
path = "./"
vuln_files = [
    f
    for f in listdir(path)
    if os.path.isfile(os.path.join(path, f)) and f.endswith(".sol")
]
success = 0

# for file in vuln_files:
#     with open(os.path.join(path, file), "r") as f:
vuln_template = create_contract(
    """
pragma solidity ^0.8.0;

contract LiquidityPoolManager {
    uint256 public latestFundedDepositID;
    Deposit[] public deposits;
    uint256 public totalPoolLiquidity;
    address public governance;
    bool public emergencyShutdown;
    struct Deposit {
        uint256 amount;
        uint256 interestOwed;
        bool active;
        bool finalSurplusIsNegative;
        uint256 finalSurplusAmount;
        address depositor;
        uint256 timestamp;
    }
    event DepositCreated(uint256 indexed depositID, address indexed depositor, uint256 amount);
    event DepositFunded(uint256 indexed depositID, uint256 amount, uint256 interest);
    event EmergencyShutdownChanged(bool status);
    modifier nonReentrant() {
        require(!_locked, 'ReentrancyGuard: reentrant call');
        _locked = true;
        _;
        _locked = false;
    }
    modifier onlyGovernance() {
        require(msg.sender == governance, 'LiquidityPoolManager: caller is not governance');
        _;
    }
    bool private _locked;
    constructor() {
        governance = msg.sender;
        latestFundedDepositID = 0;
    }

    function createDeposit(uint256 amount) external returns (uint256) {
        require(amount > 0, 'LiquidityPoolManager: deposit amount must be greater than 0');
        require(!emergencyShutdown, 'LiquidityPoolManager: emergency shutdown active');
        uint256 interestRate = calculateInterestRate(amount);
        uint256 interestOwed = (amount * interestRate) / 10000;
        deposits.push(Deposit({amount: amount, interestOwed: interestOwed, active: true, finalSurplusIsNegative: false, finalSurplusAmount: 0, depositor: msg.sender, timestamp: block.timestamp}));
        totalPoolLiquidity += amount;
        emit DepositCreated(deposits.length - 1, msg.sender, amount);
        return deposits.length - 1;
    }

    function contributeMultiple(uint256 toDepositID) external nonReentrant {
        require(toDepositID > latestFundedDepositID, 'DInterest: Deposits already funded');
        require(toDepositID <= deposits.length, 'DInterest: Invalid toDepositID');
        (bool isNegative, uint256 surplus) = surplus();
        require(isNegative, 'DInterest: No deficit available');
        uint256 totalDeficit = 0;
        uint256 totalSurplus = 0;
        uint256 totalDepositAndInterestToFund = 0;
        for (uint256 id = latestFundedDepositID.add(1); id <= toDepositID; id = id.add(1)) {
            Deposit storage depositEntry = _getDeposit(id);
            if (depositEntry.active) {
                (isNegative, surplus) = surplusOfDeposit(id);
            } else {
                (isNegative, surplus) = (depositEntry.finalSurplusIsNegative, depositEntry.finalSurplusAmount);
            }
            if (isNegative) {
                totalDeficit = totalDeficit.add(surplus);
            } else {
                totalSurplus = totalSurplus.add(surplus);
            }
            if (depositEntry.active) {
                totalDepositAndInterestToFund = totalDepositAndInterestToFund.add(depositEntry.amount).add(depositEntry.interestOwed);
            }
        }
    }

    function setEmergencyShutdown(bool _status) external onlyGovernance {
        emergencyShutdown = _status;
        emit EmergencyShutdownChanged(_status);
    }

    function calculateInterestRate(uint256 amount) public view returns (uint256) {
        if (totalPoolLiquidity == 0) return 500;
        
        if (amount > totalPoolLiquidity / 10) {
            return 700;
        } else {
            if (amount > totalPoolLiquidity / 100) {
                return 600;
            } else {
                return 500;
            }
        }
    }

    function _getDeposit(uint256 depositID) internal view returns (Deposit storage) {
        return deposits[depositID - 1];
    }

    function surplus() public view returns (bool isNegative, uint256 surplusAmount) {
        uint256 totalDeposits = 0;
        uint256 totalInterest = 0;
        for (uint256 i = 0; i < deposits.length; i++) {
            if (deposits[i].active) {
                totalDeposits += deposits[i].amount;
                totalInterest += deposits[i].interestOwed;
            }
        }
        if (totalPoolLiquidity < (totalDeposits + totalInterest)) {
            return (true, (totalDeposits + totalInterest) - totalPoolLiquidity);
        } else {
            return (false, totalPoolLiquidity - (totalDeposits + totalInterest));
        }
    }

    function surplusOfDeposit(uint256 depositID) public view returns (bool isNegative, uint256 surplusAmount) {
        require(depositID > 0 && depositID <= deposits.length, 'LiquidityPoolManager: Invalid deposit ID');
        Deposit storage depositEntry = _getDeposit(depositID);
        uint256 totalValue = depositEntry.amount + depositEntry.interestOwed;
        uint256 currentValue = calculateCurrentValue(depositID);
        if (currentValue < totalValue) {
            return (true, totalValue - currentValue);
        } else {
            return (false, currentValue - totalValue);
        }
    }

    function calculateCurrentValue(uint256 depositID) internal view returns (uint256) {
        Deposit storage depositEntry = _getDeposit(depositID);
        uint256 timeElapsed = block.timestamp - depositEntry.timestamp;
        uint256 maxGrowth = depositEntry.amount + depositEntry.interestOwed;
        uint256 growthRate = maxGrowth / (30 days);
        if (timeElapsed >= 30 days) {
            return maxGrowth;
        } else {
            return depositEntry.amount + (growthRate * timeElapsed);
        }
    }

}
"""
)

try:
    ast = create_ast_with_standart_input(vuln_template)
    # ast = SourceUnit(**ast)
    # update_node_fields(ast, {"node_type": [NodeType.VARIABLE_DECLARATION.value, NodeType.IDENTIFIER.value], "name": "lpToken"}, {"name": "<|random:collateralId|collId|id>"})
    # update_node_fields(ast, {"node_type": [NodeType.FUNCTION_DEFINITION.value, NodeType.IDENTIFIER.value], "name": "addLPToken"}, {"name": "<|random:tokenExists|exists|check>"})
    with open("contract.json", "w+") as f:
        f.write("!!!!")
        f.write(ast.model_dump_json())

    # new_ast = restore_ast(ast)
    # new_ast = ast


    with open("contract_with_comments.json", "w+") as f:
        f.write(ast.model_dump_json())

    ast = insert_comments_into_ast(vuln_template, ast)

    # for node in ast.nodes:
    #     if node.node_type == NodeType.CONTRACT_DEFINITION:
    #         # res = "".join([node.to_solidity() for node in node.nodes])

    with open("new_contract.sol", "w+") as f:
      f.write(ast.to_solidity())

    # with open("new_contract.json", "w+") as f:
    #     f.write(json.dumps(res.model_dump(), indent=4))

    # res = insert_comments_into_ast(vuln_template, res)
    print([f.name for f in restore_function_definitions(ast)])
    # new_ast = restore_storages(new_ast)
    code = res.to_solidity()


except Exception as e:
    with open("error.txt", "w+") as f:
        f.write(str(e))
    raise e
with open("new_contract.sol", "w+") as f:
    f.write(code)


ast = create_ast_from_source(code)
# parse_ast_to_solidity(new_ast)
success += 1
# print(f"Success: {success}/{len(vuln_files)}")

# VALIDATOR INFO + TIME + STATUS
