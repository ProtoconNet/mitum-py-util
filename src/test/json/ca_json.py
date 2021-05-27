from mitumc.operation.operations import generate_create_accounts

ac0_prv = " 6169fa9d292b1d7dd5ea58df8e6968453bd23341cd8a4cab9cb03f33783890a3-0114:0.0.1"
ac0_pub = "046482478b070090a8a85a33488b8147bd28a62bd666af30f8086fc5f9157ab5379b30e5d2b4f2264229d394f8f7fe5b7e7da27fd83e9613ae2ecc2ba6d99c1ae2-0115:0.0.1"
ac0_addr = "7D1mSbbraYGEmQ13BCxGt9umFRhGqfoPUrJ7fp1f6fC4-a000:0.0.1"

ac1_prv = "24cd3a9934b6d299aa0b80135d629021e3104affbf91e0008fcfc7abcec0042d-0114:0.0.1"
ac1_pub = "0405256e5caedf76215c25f89c970d10b1b0c7b5314b55d3a4aac093d1ba5aeb60a5f831cb8d0da4a88945f631dff6ceb1b581eeea8e45c3667c1d4d50f8fe07d0-0115:0.0.1"
ac1_addr = "DFAQ9V8ZkMnTJCvHocCZjP7TPEQyCaq9tFkC9pKWCYAe-a000:0.0.1"

createAccounts = generate_create_accounts(
    "mitum", ac0_prv, ac0_addr, (100, "MCC"), [(ac1_pub, 100)]
)

createAccounts.to_json("./test/json/create_accounts.json")