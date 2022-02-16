from mitumc import Generator, JSONParser
from mitumc.operation.blocksign import BLOCKSIGN_CREATE_DOCUMENTS, BLOCKSIGN_SIGN_DOCUMENTS

source_prv = "KwsWqjb6stDe5x6cdN6Xz4aNiina5HK8SmWXSCc1LMXE252gTD39mpr"
source_pub = "buSmGvywmR6TgRXaH2gy3WWvHPTiWDYZsJu1VMnY3gaYmpu"
source_addr = "FB3m9zS9DWYLgRETYr5j5A8WCTk5QY6dHAjTpzkjyPvzmca"

prv1 = "L2AJFiNcyC6gzbTQMpD7QRD6UUGnAFzDfcCFv68MPNqoYP4NGM9Cmpr"
pub1 = "tjX9kWwUJaosuGvmiLQZy5aipq2fzDZLXfn21a5iK91impu"
addr1 = "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca"

generator = Generator('mitum')
gn = generator.blockSign

# CreateDocumentsItem
createDocumentsItem = gn.createCreateDocumentsItem("abcdddd:mbhf-v0.0.1", 100, "user01", "title100", 1234, "MCC", [], ["user02"])

# CreateDocumentsFact
createDocumentsFact = gn.createBlockSignFact(BLOCKSIGN_CREATE_DOCUMENTS, source_addr, [createDocumentsItem])

# CreateDocuments
createDocuments = generator.createOperation(createDocumentsFact, "")
createDocuments.addFactSign(source_prv)

JSONParser.generateFile(createDocuments.dict(), "../example/create_documents.json")

# SignDocumentsItem
signDocumentsItem = gn.createSignDocumentsItem(source_addr, 0, "MCC")

# SignDocumentsFact
signDocumentsFact = gn.createBlockSignFact(BLOCKSIGN_SIGN_DOCUMENTS, source_addr, [signDocumentsItem])

# SignDocuments
signDocuments = generator.createOperation(signDocumentsFact, "")
signDocuments.addFactSign(source_prv)

JSONParser.generateFile(signDocuments.dict(), '../example/sign_documents.json')