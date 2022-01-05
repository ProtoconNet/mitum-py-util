from mitumc.key import getNewKeypair, getKeypairFromPrivateKey, getKeypairFromSeed

kp1 = getNewKeypair()
kp2 = getKeypairFromPrivateKey("L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr")
kp3 = getKeypairFromSeed("Thisisaseedforthisexample.Seedlength>=36.")

print(kp1.privateKey)
print(kp1.publicKey)

print(kp2.privateKey)
print(kp2.publicKey)

print(kp3.privateKey)
print(kp3.publicKey)