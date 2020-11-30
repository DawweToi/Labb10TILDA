#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
 

from molgrafik import *
from linkedQFile import *

LETTER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter = 'abcdefghijklmnopqrstuvwxyz'
num = '0123456789'
AtomStr = 'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Fl Lv'


def FuckThis():
	AtomList = []
	tempLet = ''
	for letter in AtomStr:
		if letter == ' ':
			AtomList.append(tempLet)
			tempLet = ''
		else: tempLet += letter
	return AtomList

AtomList = FuckThis()


def fixAtomList():
	atomDict = {}
	for line in open('atomer.txt'):
		tempAtom = ''
		tempWeight = ''
		isAtom = True
		for symbol in line:
			if symbol == ' ':
				isAtom = False

			elif isAtom: tempAtom += symbol
			else: tempWeight += symbol

		atomDict[tempAtom] = float(tempWeight)

	return atomDict

atomDict = fixAtomList()

class Syntaxfel(Exception):
	pass

def readFormel(q):
	mol = readMolekyl(q)
	return mol


def readMolekyl(q):
	# läser kön
	# print('Bokstav:'+q.peek()+'----')
	mol = readGroup(q)
	if q.peek() == '\n':
		return mol
	else:
		mol.next = readMolekyl(q)

	return mol

def readMol2(q):
	mol = readGroup(q)
	if q.peek() == '\n' or q.peek() == ')':
		return mol
	else:
		mol.next = readMol2(q)

	return mol


def readGroup(q):
	rutan = Ruta()

	if q.peek() in LETTER:
		rutan.atom = readAtom(q)
		if q.peek() in num:
			rutan.num = int(readNum(q))
		return rutan

	elif q.peek() == '(':
		q.dequeue()
		rutan.down = readMol2(q)
		if not q.peek() == ')':
			raise Syntaxfel('Saknad högerparentes vid radslutet ' + restOfString(q))
		# print(q.peek())
		q.dequeue()
		if not q.peek() in num:
			raise Syntaxfel('Saknad siffra vid radslutet ' + restOfString(q))
		rutan.atom = '( )'
		rutan.num = int(readNum(q))
		return rutan

	else:
		# print('Slut på readGroup, bokstav:'+q.peek()+'----')
		if q.peek() in letter:
			raise Syntaxfel('Saknad stor bokstav vid radslutet ' + restOfString(q))
		raise Syntaxfel('Felaktig gruppstart vid radslutet ' + restOfString(q))
	


def readAtom(q):
	# läser atomen
	firstLetter = q.dequeue()
	secondLetter = ''

	if q.peek() in letter:
		secondLetter = q.dequeue()

	if checkAtom(firstLetter+secondLetter) == False:
		raise Syntaxfel('Okänd atom vid radslutet ' + restOfString(q))

	return firstLetter+secondLetter


def readNum(q):
	# kollar siffror efter atom eller molekyl
	numStr = q.dequeue()
	
	if not numStr == '0':
		while q.peek() in num:
			numStr += q.dequeue()
	if numStr == 0 or int(numStr) < 2:
		raise Syntaxfel('För litet tal vid radslutet ' + restOfString(q))
	else:
		return numStr


def checkAtom(atom):
	if not atom in AtomList:
		return False

def restOfString(q):
	tempStr = ''
	while not q.isEmpty():
		if q.peek() == '\n':
			q.dequeue()
		else: tempStr += q.dequeue()
	return tempStr

def TestaSyntax(q):
	# testar syntax
	try:
		mol = readFormel(q)
		return 'Formeln är syntaktiskt korrekt', mol
	except Syntaxfel as fel:
		return str(fel), None

def molWeight(mol):
	if mol == None: return 0

	if mol.atom == '( )': return mol.num * molWeight(mol.down) + molWeight(mol.next)

	if mol.down == None:
		return atomDict[mol.atom] * mol.num + molWeight(mol.next)
	else: 
		return molWeight(mol.down) + molWeight(mol.next)


# def kollaSyntax(testString):
# 	q = LinkedQ()
# 	for symbol in testString:
# 		q.enqueue(symbol)
# 	q.enqueue('\n')
# 	return TestaSyntax(q)

def main():
	# atomDict = fixAtomList()
	line = ''
	while line != 'e':
		line = input('Skriv molekyl: ')
		q = LinkedQ()
		# print('\nNu på: '+line)
		for symbol in line:
			q.enqueue(symbol)
		q.enqueue('\n')
		testMsg, mol = TestaSyntax(q)
		print(testMsg)

		molVikt = molWeight(mol)
		print('Vikt: ' + str(molVikt))

		if not mol == None:
			mg = Molgrafik()
			mg.show(mol)

	
	
if __name__ == "__main__":
    main()
    # kollaSyntax('abc')
