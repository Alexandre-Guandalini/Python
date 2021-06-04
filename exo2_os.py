import sys
os2 = input("Entrez votre os :")

print("Ton os est selon toi", os2, "mais ...")

if os2 in ["Windows","windows","win"]:
     if sys.platform == 'win32':
        print("...et tu as raison")
     else:
        print("...et tu mens")
else:
    print("...et tu mens")