from mitumc import Signer, JSONParser

signer = Signer("mitum", "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr")
signed = signer.signOperation('example/create_accounts.json')

JSONParser.toFile(signed, 'example/signed.json')