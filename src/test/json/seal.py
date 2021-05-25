from mitum.operation.operations import generate_create_accounts, generate_key_updater, generate_seal, generate_transfers

ac0_prv = "L1oTaxcPztdqAU7ZzrHMWLnX2iUm6MhMW3RxT5YByiEpceDbUhPE-0112:0.0.1"
ac0_pub = "sMs6R5BF9EsVcGV6enuwVZ4hv4H4y48RNy2yPJg6F6RH-0113:0.0.1"
ac0_addr = "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1"

ac1_prv = "KzwnfXA32SsDZEJcor4nv1qG4YMWexxuuLTNYsfyUGKuf24GW3C3-0112:0.0.1"
ac1_pub = "27LZo3wxW5T9VH5Da1La9bCSg1VfnaKtNvb3Gmg115N6X-0113:0.0.1"
ac1_addr = "CHmkPR6GqTZfxrs1ptoWupsgvzkgvNdE7ZzhvimGUErg-a000:0.0.1"

createAccounts = generate_create_accounts(
    "mitum", ac0_prv, ac0_addr, (100, "MCC"), [(ac1_pub, 100)]
)

keyUpdater = generate_key_updater("mitum", ac0_prv, ac0_addr, ac1_pub, 100, "MCC")

transfers = generate_transfers("mitum", ac0_prv, ac0_addr, ac1_addr, (100, "MCC"))

operations = [transfers]

generate_seal("./test/json/seal.json", "mitum", ac0_prv, operations)