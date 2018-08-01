#!/home/lmanrique/anaconda3/bin/python3
import os
import sys
import re
import time
from astropy.io import fits

#path_utils = '/home/lmanrique/lib_AMM/utils/'
path_utils = '/home/lmanrique/solvepol/pipelineV16_1/'

def validate():
	if (len(sys.argv) == 1 or not os.path.isdir(sys.argv[1])):
		return False
	return True

def createList(path):
	listDir = os.listdir(path)
	resp = []
	regex = re.compile(r'^[0-9]{2}[a-zA-Z]{3}[0-9]{2}.?$')
	for ld in listDir:
		if os.path.isdir(sys.argv[1] + '/' + ld) and regex.match(ld): 
			resp.append(ld)		
	return resp

def removeDir(listDir):
	rm = ['bias', 'flat', 'lixo', '.DS_Store'] # Add to this list the directories that should be ignored by solvepol
	temp = list(listDir)
	for ld in listDir:
		if ld in rm:
			temp.remove(ld)
	return temp

def numkin(lista):
	f = open(lista, 'r')
	lpos = {}
	while True:
		line = f.readline()
		if not line: break
		pos = line.split('/')[-1]
		if not len(pos.split('_')) > 1: return 1
		pos = pos.split('_')[-3]

		if pos not in lpos: 
			lpos[pos] = 1
		else: 
			lpos[pos] += 1
	return list(lpos.values())[0]

def solvepol():
	for ld in listDir:
		os.chdir(ld)
		objects = os.listdir('.')
		objects = removeDir(objects)
		os.chdir(list(objects)[0])
		objectfile = os.path.dirname(os.getcwd()) + '/' + list(objects)[0] + '/' + list(objects)[0] + '_no_path.list'
		nreads = numkin(objectfile)

		print('##############################################################')
		print('Running solvepol (nread = ' + str(nreads) + ') in the directory:')
		print('CD, "' + os.path.dirname(os.getcwd()) + '/' + list(objects)[0] + '"')
		print('##############################################################')

		with open(path_utils + 'run_solvepol.pro', 'w') as f:
			print('pro run_solvepol', file=f)
			print('CD, "' + os.path.dirname(os.getcwd()) + '/' + list(objects)[0] + '"', file=f)
			#print('   solvepol, "' + objectfile + '", nreads=' + str(nreads) + ', flats="' + os.path.dirname(os.getcwd()) + '/flat/flat.list", bias="' + 
			#	   os.path.dirname(os.getcwd()) + '/bias/bias.list", fluxsigma = 5., polsigma = 5., astrometry="y"', file=f)
			print('   solvepol, "' + objectfile + '", nreads=' + str(nreads) + ', flats="/home/lmanrique/lib_AMM/17jul24/bicep2_8058/solvepol/flat_bias_combine.fits", \
				       bias="/home/lmanrique/lib_AMM/17jul24/bicep2_8058/solvepol/bias_zero.fits", fluxsigma = 5., polsigma = 5., astrometry="y"', file=f)
			#print('   solvepol, "' + objectfile  + '", nreads=' + str(nreads) + ', fluxsigma = 5., astrometry="y", polsigma = 5.', file=f)	
			print('end', file=f)
		owd = os.getcwd()
		os.chdir(path_utils)
		os.system('idl < ' + path_utils + 'in.pro')	
		os.chdir(owd)
		os.chdir('..')
		sys.exit()

		for obj in list(objects)[1:]:
			os.chdir(obj)
			objectfile = os.path.dirname(os.getcwd()) + '/' + obj + '/' + obj + '_no_path.list'
			nreads = numkin(objectfile)

			print('##############################################################')
			print('Running solvepol (nread = ' + str(nreads) + ') in the directory:')
			print('CD, "' + os.path.dirname(os.getcwd()) + '/' + obj + '"')
			print('##############################################################')

			with open(path_utils + 'run_solvepol.pro', 'w') as f:
				print('pro run_solvepol', file=f)
				print('CD, "' + os.path.dirname(os.getcwd()) + '/' + obj + '"', file=f)
				#print('   solvepol, "' + objectfile + '", nreads=' + str(nreads) + ', flats="' + os.path.dirname(os.getcwd()) + '/flat/flat.list", bias="' + 
				#	   os.path.dirname(os.getcwd()) + '/bias/bias.list", fluxsigma = 5., polsigma = 5., astrometry="y"', file=f)
				print('   solvepol, "' + objectfile  + '", nreads=' + str(nreads) + ', fluxsigma = 5., astrometry="y", polsigma = 5.', file=f)		
				print('end', file=f)
			owd = os.getcwd()
			os.chdir(path_utils)
			os.system('idl < ' + path_utils + 'in.pro')	
			os.chdir(owd)
			os.chdir('..')
		os.chdir('..')

def printDir(listDir):
	for ld in listDir:
		print(os.path.abspath(sys.argv[1]) + '/' + ld)

#Checking if the argument is a valid directory 
if not validate():
	print('You must specify a valid directory.')
	sys.exit()

#Creating a list of valid subdirectories using the pattern YY/month/DD
listDir = createList(sys.argv[1])

#Listing found directories 
print('The following directories will be processed by solvepol')
printDir(listDir)
time.sleep(3)
print('')

solvepol()