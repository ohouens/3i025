def initPrefEtu(path):
	f = open(path, "r")
	if(f.mode == "r"):
		etudiants = []
		buff = f.readlines()
		#print(buff)
		nbr = 0
		final = []
		for i in range(len(buff)):
			if(i == 0):
				nbr = buff[i].rstrip('\r\n')
				#print('nbr'+nbr)
			else:
				inter = buff[i].rstrip('\r\n').split('\t')
				#print(inter)
				final.append(inter)
		for i in range(len(final)):
			etudiants.append((final[i][1], -1, 1, final[i][2:], []))
		return etudiants

def initPrefSpe(path):
	f = open(path, "r")
	if(f.mode == "r"):
		masters = []
		buff = f.readlines()
		#print(buff)
		final = []
		pref = []
		for i in range(len(buff)):
			if(i == 0):
				nbr = buff[i].rstrip('\r\n')
				#print('nbr'+nbr)
			else:
				inter = buff[i].rstrip('\r\n').split('\t')
				#print(inter)
				pref.append(inter)
		capacity = pref[0][0]
		capacity = capacity.split(' ')
		capacity.remove('Cap')
		#print(capacity)
		final.append(capacity)
		inter = []
		for i in range(1, len(pref)):
			inter.append(pref[i])
		#print(inter)
		final.append(inter)
		for i in range(len(final[1])):
			masters.append((final[1][i][1], -1, final[0][i], final[1][i][2:], []))
		return masters

prefEtu = initPrefEtu("TestPrefEtu.txt")
prefSpe = initPrefSpe("TestPrefSpe.txt")

#print(prefEtu)
#print(prefSpe)

def verifLibre(listVerif):

	for nom, libre, capacity, demande, stack in listVerif:
		#print(nom, libre, capacity, demande)
		if(libre == -1):
			print("un etudiant est toujour libre")
			return True
	print("Tous le monde est pris")
	return False

def choisirLibre(listVerif):
	for i in range(len(listVerif)):
		#print(nom, libre, capacity, demande)
		nom, libre, capacity, demande, stack = listVerif[i]
		if(libre == -1):
			return i
	return False

def affecte(etudiants, masters, m, w):
	nom, libre, capacity, demande, stack = etudiants[m]
	stack.append(w)
	demande.remove(str(w))
	capacity = str(int(capacity)-1)
	if(int(capacity) <= 0):
		libre = 1
	etudiants[m] = (nom, libre, capacity, demande, stack)

	nom, libre, capacity, demande, stack = masters[w]
	stack.append(m)
	#demande.remove(str(m))
	capacity = str(int(capacity)-1)
	if(int(capacity) <= 0):
		libre = 1
	masters[w] = (nom, libre, capacity, demande, stack)

def divorce(etudiants, masters, n, w):
	nom, libre, capacity, demande, stack = etudiants[n]
	stack.remove(w)
	capacity = str(int(capacity)-1)
	libre = -1
	etudiants[n] = (nom, libre, capacity, demande, stack)

	nom, libre, capacity, demande, stack = masters[w]
	stack.remove(n)
	capacity = str(int(capacity)-1)
	libre = -1
	masters[w] = (nom, libre, capacity, demande, stack)


def choisirPlusNul(verif):
	for i in range(-1, -len(verif[3])-1, -1):
		if(int(verif[3][i]) in verif[4]):
			return verif[3][i]

def prefere(verif, m, n):
	for i in range(len(verif[3])):
		if(verif[3][i] == str(m) or verif[3][i] == str(n)):
			if(verif[3][i] == str(m)):
				return True
			return False
	return False

def gale_shapley(v1, v2, temoin=1):
	case = ['etudiant', 'master']
	if(temoin == 0):
		case = ['master', 'etudiant']
	#print(v1)
	#print(v2)
	a = 0
	print('debut')
	while(verifLibre(v1) and a<11*11):
		print('a: '+str(a)+'\n')
		m = int(choisirLibre(v1))#etudiant
		print(case[0]+' choisit: '+v1[m][0])
		w = int(v1[m][3][0])#master
		print(case[1]+' choisit: '+v2[w][0])
		if(int(v2[w][2]) > 0):
			print('capacite de '+str(v2[w][0])+' a '+str(v2[w][2])+' donc affectation automatique')
			affecte(v1, v2, m, w)
		else:
			n = int(choisirPlusNul(v2[w]))
			print('plus nul choisit: '+str(n))
			if(prefere(v2[w], m, n)):
				print(v2[w][0]+' prefere etudiant['+str(m)+'] a etudiant['+str(n)+']\n')
				divorce(v1, v2, n, w)
				affecte(v1, v2, m, w)
			else:
				print(v2[w][0]+' rejette etudiant['+str(m)+']\n')
				v1[m][3].remove(str(w))

		print('\n'+case[0])
		print(v1)
		print('\n'+case[1])
		print(v2)
		print('\n\n\n\n')
		a = a-1
	print('fin')

#gale_shapley(prefEtu, prefSpe)
#gale_shapley(prefSpe, prefEtu, 0)
import random

def initAleaEtu(n):
	final = []
	for i in range(n):
		tirage = []
		for y in range(n):
			tirage.append(y)
		pref = []
		temoin = -1
		for y in range(n):
			while(not(temoin in tirage)):
				numero = random.randint(0, len(tirage)-1)
				temoin = tirage[numero]
			pref.append(temoin)
			tirage.remove(temoin)
		final.append(("Etu"+str(i), 1, pref, []))
	return final

def initAleaMaster(n):
	nomMaster = ["ANDROIDE", "BIM", "DAC", "IMA", "RES", "SAR", "SESI", "SFPN", "STL"]
	nbMaster = 9
	if(n < nbMaster):
		nbMaster = n
	capacite = n
	final = []
	i = 0
	while(i<nbMaster and capacite > 0):
		place = 2*n
		while(place > capacite):
				if(capacite == 1):
					place = 1
				elif(i == n-1):
					place = capacite
				else:
					place = random.randint(1, 7)
		capacite = capacite - place
		tirage = []
		for y in range(n):
			tirage.append(y)
		pref = []
		temoin = -1
		for y in range(n):
			while(not(temoin in tirage)):
				numero = random.randint(0, len(tirage)-1)
				temoin = tirage[numero]
			pref.append(temoin)
			tirage.remove(temoin)
		final.append((nomMaster[i], place, pref, []))
		i = i+1
	return final

#print(initAleaMaster(13))
import time
import matplotlib.pyplot as plt

def measureExecTime(a, b, c):
	temps = []
	valeurs = []
	for i in range(a, b, c):
		start = time.time()
		initAleaMaster(i)
		end = time.time()
		temps.append(end-start)
		valeurs.append(i)
	plt.plot(valeurs, temps)
	plt.ylabel('times')
	plt.xlabel('values')
	plt.show()
	return (valeurs, temps)

measureExecTime(200, 2000, 200)