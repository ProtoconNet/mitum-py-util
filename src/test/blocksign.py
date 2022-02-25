from mitumc import Generator, JSONParser

source_prv = "KwsWqjb6stDe5x6cdN6Xz4aNiina5HK8SmWXSCc1LMXE252gTD39mpr"
source_pub = "buSmGvywmR6TgRXaH2gy3WWvHPTiWDYZsJu1VMnY3gaYmpu"
source_addr = "FB3m9zS9DWYLgRETYr5j5A8WCTk5QY6dHAjTpzkjyPvzmca"

prv1 = "L2AJFiNcyC6gzbTQMpD7QRD6UUGnAFzDfcCFv68MPNqoYP4NGM9Cmpr"
pub1 = "tjX9kWwUJaosuGvmiLQZy5aipq2fzDZLXfn21a5iK91impu"
addr1 = "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca"

generator = Generator('mitum')
gn = generator

# create documents
creator = gn.md.bs.user(source_addr, "signer01", True)
signer1 = gn.md.bs.user(source_addr, "signer01", True)
signer2 = gn.md.bs.user(addr1, "signer02", False)
cdDocument = gn.md.bs.document("bstest01sdi", source_addr, "fs:01", creator, "doc01", "1234", [signer1, signer2])
cdItem = gn.md.getCreateDocumentsItem(cdDocument, "PEN")
cdFact = gn.md.getCreateDocumentsFact(source_addr, [cdItem])
cdOper = gn.getOperation(cdFact, "")
cdOper.addFactSign(source_prv)

JSONParser.toFile(cdOper.dict(), "example/blocksign_create_documents.json")

# sign documents
sdItem = gn.md.bs.getSignDocumentsItem("bstest01sdi", source_addr, "PEN")
sdFact = gn.md.bs.getSignDocumentsFact(source_addr, [sdItem])
sdOper = gn.getOperation(sdFact, "")
sdOper.addFactSign(source_prv)

JSONParser.toFile(cdOper.dict(), "example/blocksign_sign_documents.json")
