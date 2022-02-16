from mitumc import Generator, JSONParser
from mitumc.operation.blockcity import DOCTYPE_USER_DATA, DOCTYPE_LAND_DATA, DOCTYPE_VOTE_DATA, DOCTYPE_HISTORY_DATA

generator = Generator('mitum')
gn = generator.blockCity

# user document
userInfo = gn.info(DOCTYPE_USER_DATA, "4cui")
statistics = gn.userStatistics(1, 1, 1, 1, 1, 1, 1)
userDocument = gn.userDocument(userInfo, "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 10, 10, statistics)

# land document
landInfo = gn.info(DOCTYPE_LAND_DATA, "4cli")
landDocument = gn.landDocument(landInfo, "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", "abcd", "city1", "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2021-10-22", 10)

# vote document
voteInfo = gn.info(DOCTYPE_VOTE_DATA, "4cvi")
c1 = gn.candidate("8sXvbEaGh1vfpSWSib7qiJQQeqxVJ5YQRPpceaa5rd9Ymca", "foo1", "", 1)
c2 = gn.candidate("Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "foo2", "", 2)
voteDocument = gn.voteDocument(voteInfo, "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 1, "2022-02-22", [c1, c2], "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2022")

# history document
historyInfo = gn.info(DOCTYPE_HISTORY_DATA, "1000chi")
historyDocument = gn.historyDocument(historyInfo, "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "abcd", "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "2022-02-01T00:00:00.000+09:00", "bob", "foo")

# create document
userCreateItem = gn.createCreateDocumentsItem(userDocument, "PEN")
userCreateFact = gn.createCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [userCreateItem])

landCreateItem = gn.createCreateDocumentsItem(landDocument, "PEN")
landCreateFact = gn.createCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [landCreateItem])

voteCreateItem = gn.createCreateDocumentsItem(voteDocument, "PEN")
voteCreateFact = gn.createCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [voteCreateItem])

historyCreateItem = gn.createCreateDocumentsItem(historyDocument, "PEN")
historyCreateFact = gn.createCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [historyCreateItem])

# update document
userUpdateItem = gn.createUpdateDocumentsItem(userDocument, "PEN")
userUpdateFact = gn.createUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [userUpdateItem])

landUpdateItem = gn.createUpdateDocumentsItem(landDocument, "PEN")
landUpdateFact = gn.createUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [landUpdateItem])

voteUpdateItem = gn.createUpdateDocumentsItem(voteDocument, "PEN")
voteUpdateFact = gn.createUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [voteUpdateItem])

historyUpdateItem = gn.createUpdateDocumentsItem(historyDocument, "PEN")
historyUpdateFact = gn.createUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [historyUpdateItem])

o1 = generator.createOperation(userCreateFact, "")
o2 = generator.createOperation(landCreateFact, "")
o3 = generator.createOperation(voteCreateFact, "")
o4 = generator.createOperation(historyCreateFact, "")
o5 = generator.createOperation(userUpdateFact, "")
o6 = generator.createOperation(landUpdateFact, "")
o7 = generator.createOperation(voteUpdateFact, "")
o8 = generator.createOperation(historyUpdateFact, "")

JSONParser.generateFile(o1.dict(), "example/user_create.json")
JSONParser.generateFile(o2.dict(), "example/land_create.json")
JSONParser.generateFile(o3.dict(), "example/vote_create.json")
JSONParser.generateFile(o4.dict(), "example/history_create.json")
JSONParser.generateFile(o5.dict(), "example/user_update.json")
JSONParser.generateFile(o6.dict(), "example/land_update.json")
JSONParser.generateFile(o7.dict(), "example/vote_update.json")
JSONParser.generateFile(o8.dict(), "example/history_update.json")