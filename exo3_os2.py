import sys

test = False
os2 = input("Entrez votre os : ")

while test==False:
	print("Ton os est selon toi est", os2, "mais ...")
	
	if os2 in ["Windows","windows","win"]:
			print("...tu as raison")
			test==True
	else:
		print("...tu mens")
		os2 = input("Non sérieux quelle est ton vrai os?")
        
input()