from mitumc import Generator, JSONParser\

gn = Generator('mitum')

# user document
statistics = gn.md.bc.userStatistics(1, 1, 1, 1, 1, 1, 1)
userDocument = gn.md.bc.userDocument("4cui", "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 10, 10, statistics)

# land document
landDocument = gn.md.bc.landDocument("4cli", "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", "abcd", "city1", "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2021-10-22", 10)

# vote document
c1 = gn.md.bc.candidate("8sXvbEaGh1vfpSWSib7qiJQQeqxVJ5YQRPpceaa5rd9Ymca", "foo1", "", 1)
c2 = gn.md.bc.candidate("Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "foo2", "", 2)
voteDocument = gn.md.bc.voteDocument("4cvi", "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 1, "2022-02-22", [c1, c2], "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2022")

# history document
historyDocument = gn.md.bc.historyDocument("4chi", "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "abcd", "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "2022-02-01T00:00:00.000+09:00", "bob", "foo")

# create document
userCreateItem = gn.md.getCreateDocumentsItem(userDocument, "PEN")
userCreateFact = gn.md.getCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [userCreateItem])

landCreateItem = gn.md.getCreateDocumentsItem(landDocument, "PEN")
landCreateFact = gn.md.getCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [landCreateItem])

voteCreateItem = gn.md.getCreateDocumentsItem(voteDocument, "PEN")
voteCreateFact = gn.md.getCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [voteCreateItem])

historyCreateItem = gn.md.getCreateDocumentsItem(historyDocument, "PEN")
historyCreateFact = gn.md.getCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [historyCreateItem])

# update document
userUpdateItem = gn.md.getUpdateDocumentsItem(userDocument, "PEN")
userUpdateFact = gn.md.getUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [userUpdateItem])

landUpdateItem = gn.md.getUpdateDocumentsItem(landDocument, "PEN")
landUpdateFact = gn.md.getUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [landUpdateItem])

voteUpdateItem = gn.md.getUpdateDocumentsItem(voteDocument, "PEN")
voteUpdateFact = gn.md.getUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [voteUpdateItem])

historyUpdateItem = gn.md.getUpdateDocumentsItem(historyDocument, "PEN")
historyUpdateFact = gn.md.getUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [historyUpdateItem])

o1 = gn.getOperation(userCreateFact, "")
o2 = gn.getOperation(landCreateFact, "")
o3 = gn.getOperation(voteCreateFact, "")
o4 = gn.getOperation(historyCreateFact, "")
o5 = gn.getOperation(userUpdateFact, "")
o6 = gn.getOperation(landUpdateFact, "")
o7 = gn.getOperation(voteUpdateFact, "")
o8 = gn.getOperation(historyUpdateFact, "")

o1.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
o2.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
o3.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
o4.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
o5.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
o6.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
o7.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
o8.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")

JSONParser.toFile(o1.dict(), "example/user_create_documents.json")
JSONParser.toFile(o2.dict(), "example/land_create_documents.json")
JSONParser.toFile(o3.dict(), "example/vote_create_documents.json")
JSONParser.toFile(o4.dict(), "example/history_create_documents.json")
JSONParser.toFile(o5.dict(), "example/user_update_documents.json")
JSONParser.toFile(o6.dict(), "example/land_update_documents.json")
JSONParser.toFile(o7.dict(), "example/vote_update_documents.json")
JSONParser.toFile(o8.dict(), "example/history_update_documents.json")