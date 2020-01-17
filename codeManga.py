#du ligne 2-8 nous avons importé les modules necessaires 
import sys
import re
import bs4
import requests
import os
from io import BytesIO
from PIL import Image
def telechargerImage(LIEN_DE_IMAGE, T_CHAPITRE):#cette fonction nous permet de telecharger les images
	j=1
	while LIEN_DE_IMAGE:	
		data = requests.get(LIEN_DE_IMAGE)
		base = bs4.BeautifulSoup(data.text, 'html.parser')
		try:
			img = base.select_one("img[id='img']").get('src')#nous allons recuperer l'adresse de l'image en utilisant cette fonction
			print(f"TELECHARGEMENT DE L'IMAGE {j} DU Chapitre {T_CHAPITRE} : {LIEN_DE_IMAGE}")#f permet d'inserer la valeur f
			j=j+1#permet de compter le nombre d'image qu'on a telecharge
			res = requests.get(img)
			imgFile = Image.open(BytesIO(res.content))
			imgFile.save(os.path.basename(LIEN_DE_IMAGE)+'.jpg')#permet de definir le format de l'image et aussi pour l'enregistrement
		except Exception as e:
			print("Impossible de Demarer le telechargement !!!")
		nextLIEN  = base.select_one("div[id='imgholder'] a").get('href')
		if int(nextLIEN.split("/")[2]) != T_CHAPITRE:
			break
		LIEN_DE_IMAGE =f"{baseLIEN+nextLIEN}"		
def telechargerManga(Nom_Manga, Numero_Chapitre):
	sep = "".join(re.findall(r"[-,]", Numero_Chapitre))#cette fonction  nous permet d extraire  si on a le caractere , ou - et de l stocker dans sep
	Numero_Chapitre = re.split(r"[-,]",sys.argv[2])#la fonction re.split() va nous permetrre de decouper la chaine sys.argv[2] selon l expression qui les separe
	Numero_Chapitre = list(map(int, Numero_Chapitre))#ici nous allons  transformer les chaine de caractere en entier sous forme de tableau
	LIEN = f"{baseLIEN}/{Nom_Manga}"
	if len(Numero_Chapitre)==2:
		if sep == '-':
			debut, fin = Numero_Chapitre[0], Numero_Chapitre[1]+1
			for i in range(debut, fin):
				LIEN_DE_IMAGE = f"{LIEN}/{i}/1"
				if not os.path.exists(f"Chapitre {i}"):
					try:
						os.mkdir(f"Chapitre {i}")
					except :
						print(f"Impossible de cree le dossier du Chapitre {i}")
						sys.exit()
				os.chdir(f"Chapitre {i}")
				telechargerImage(LIEN_DE_IMAGE, i)
				os.chdir("..")
		elif sep == ',':
			for i in Numero_Chapitre:
				LIEN_DE_IMAGE = f"{LIEN}/{i}/1"
				if not os.path.exists(f"Chapitre {i}"):
					try:
						os.mkdir(f"Chapitre {i}")
					except :
						print(f"Impossible de cree le dossier du Chapitre {i}")
						sys.exit()
						
				os.chdir(f"Chapitre {i}")
				telechargerImage(LIEN_DE_IMAGE, i)
				os.chdir("..")
	elif len(Numero_Chapitre) == 1:
		chap = Numero_Chapitre[0]
		if not os.path.exists(f"Chapitre {chap}"):
			try:
				os.mkdir(f"Chapitre {chap}")
			except :
				print(f"Impossible de cree le dossier du Chapitre {i}")
				sys.exit()
						
		os.chdir(f"Chapitre {chap}")
		LIEN_DE_IMAGE = f"{LIEN}/{chap}/1"
		telechargerImage(LIEN_DE_IMAGE, chap)
	print("TELECHARGEMENT TERMINÈ ")
if __name__ == "__main__":
	Nom_Manga = sys.argv[1]
	chapiters = sys.argv[2]
	baseLIEN = "http://www.mangapanda.com"
	os.chdir(os.path.abspath("."))

	if not os.path.exists(Nom_Manga):
		try:
			os.mkdir(Nom_Manga)
		except :
			print(f"Impossible de cree le dossier du Chapitre {i}")
			sys.exit()
	try:
		os.chdir(Nom_Manga)
		telechargerManga(Nom_Manga, chapiters)
	except AttributeError as e:
			print(f"Manga {Nom_Manga} Non trouve")
	except ValueError as e:
			print(f"Chapitre {chapiters} Non trouve ")

	