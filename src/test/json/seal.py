from mitumc.operation import key_updater
from mitumc.operation.operations import generate_create_accounts, generate_key_updater, generate_seal, generate_transfers

source_prv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok-0112:0.0.1"
source_pub = "rcrd3KA2wWNhKdAP8rHRzfRmgp91oR9mqopckyXRmCvG-0113:0.0.1"
source_addr = "8PdeEpvqfyL3uZFHRZG5PS3JngYUzFFUGPvCg29C2dBn-a000:0.0.1"

ac1_prv = "SBGISVULOQA6BPEYF4OS2JGMBST7HYCBSL3TA2QRVGRNBMVWIZVE6336-0110:0.0.1"
ac1_pub = "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35-0111:0.0.1"
ac1_addr= "8HQt6CfBVgMhLmPxcataTF2CXHuw2Km32FAcW7FXmQZ3-a000:0.0.1"

ac2_prv = "8d15c09377e0d504f175f8ad595690b83e59e08c67d7f71f7795a489412b6f04-0114:0.0.1"
ac2_pub = "04c7a0b69c4041d2d3cf60d9318b5fdb1c29c7f63b3514aab52db6a852083dd3e1065afa8524c4ba54688ae36055377b2bb3de931054c124f01f38e7eab27e9e8f-0115:0.0.1"
ac2_addr = "8dsqP9dUPKv3TjJg6DCKJ7NE7vsMx47Gc4VrseEcyXtt-a000:0.0.1"

ac3_prv = "SBEJGCQ4OBOOIHFWZBEHOI6FSSTDLATDFY73QIZANP2J6KMLL77CAI4D-0110:0.0.1"
ac3_pub = "GCV6WZ5U7HXFOXWTMLUXCG4PW3KP2YYTMAPZDE3IIVWQY7Q6SYPG63TZ-0111:0.0.1"
ac3_addr = "8dsqP9dUPKv3TjJg6DCKJ7NE7vsMx47Gc4VrseEcyXtt-a000:0.0.1"

createAccounts = generate_create_accounts(
    "mitum", source_prv, source_addr, (100, "MCC"), [(ac1_pub, 100)]
)
keyUpdater = generate_key_updater("mitum", ac1_prv, ac1_addr, ac3_pub, 100, "MCC")
transfers = generate_transfers("mitum", source_prv, source_addr, ac2_addr, (100, "MCC"))

operations = [createAccounts, keyUpdater, transfers]

generate_seal("seal.json", "mitum", source_prv, operations)