from mitumc.operation.generator import Generator, JSONParser

source_prv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
source_pub = "rcrd3KA2wWNhKdAP8rHRzfRmgp91oR9mqopckyXRmCvG:btc-pub-v0.0.1"
source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"

priv1 = "SCXSRCZKAB5A53TKAFSFZEPMQRM4AAZAND2MBIHFDBEQLM3DWILRQUF2:stellar-priv-v0.0.1"
pub1 = "GBMWRVVIY2SHIMLG3ZQR54WGXKG5RYXFHGC2HNT3W674DLXK6VQ4QY4X:stellar-pub-v0.0.1"
addr1 = "ATDxH32CL7hdrpgLcvtNroNTF111V6wUJCK5JTa4f8Po:mca-v0.0.1"

generator = Generator('mitum')

# CreateDocumentsItem
createDocumentsItem = generator.createCreateDocumentsItem("abc:mbhf-v0.0.1", [], "MCC")

# CreateDocumentsFact
createDocumentsFact = generator.createCreateDocumentsFact(source_addr, [createDocumentsItem])

# CreateDocuments
createDocuments = generator.createOperation(createDocumentsFact, "")
createDocuments.addFactSign(source_prv)

JSONParser.generateFile(createDocuments.to_dict(), "../example/create_documents.json")

# TransferDocumentsItem
transferDocumentsItem = generator.createTransferDocumentsItem(source_addr, addr1, 0, "MCC")

# TransferDocumentsFact
transferDocumentsFact = generator.createTransferDocumentsFact(source_addr, [transferDocumentsItem])

# TransferDocuments
transferDocuments = generator.createOperation(transferDocumentsFact, "")
transferDocuments.addFactSign(source_prv)

JSONParser.generateFile(transferDocuments.to_dict(), "../example/transfer_documents.json")

# SignDocumentsItem
signDocumentsItem = generator.createSignDocumentsItem(source_addr, 0, "MCC")

# SignDocumentsFact
signDocumentsFact = generator.createSignDocumentsFact(source_addr, [signDocumentsItem])

# SignDocuments
signDocuments = generator.createOperation(signDocumentsFact, "")
signDocuments.addFactSign(source_prv)

JSONParser.generateFile(signDocuments.to_dict(), '../example/sign_documents.json')