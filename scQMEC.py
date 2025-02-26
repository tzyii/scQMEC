#!/bin/env python3

import os, re, subprocess
import numpy as np
from copy import copy

# Constants in Gaussian 16
Bohr, Hartree = 0.52917721092, 27.2114

# START: from phonopy
atom_data = [
    [0, "X", "X", None],  # 0
    [1, "H", "Hydrogen", 1.00794],  # 1
    [2, "He", "Helium", 4.002602],  # 2
    [3, "Li", "Lithium", 6.941],  # 3
    [4, "Be", "Beryllium", 9.012182],  # 4
    [5, "B", "Boron", 10.811],  # 5
    [6, "C", "Carbon", 12.0107],  # 6
    [7, "N", "Nitrogen", 14.0067],  # 7
    [8, "O", "Oxygen", 15.9994],  # 8
    [9, "F", "Fluorine", 18.9984032],  # 9
    [10, "Ne", "Neon", 20.1797],  # 10
    [11, "Na", "Sodium", 22.98976928],  # 11
    [12, "Mg", "Magnesium", 24.3050],  # 12
    [13, "Al", "Aluminium", 26.9815386],  # 13
    [14, "Si", "Silicon", 28.0855],  # 14
    [15, "P", "Phosphorus", 30.973762],  # 15
    [16, "S", "Sulfur", 32.065],  # 16
    [17, "Cl", "Chlorine", 35.453],  # 17
    [18, "Ar", "Argon", 39.948],  # 18
    [19, "K", "Potassium", 39.0983],  # 19
    [20, "Ca", "Calcium", 40.078],  # 20
    [21, "Sc", "Scandium", 44.955912],  # 21
    [22, "Ti", "Titanium", 47.867],  # 22
    [23, "V", "Vanadium", 50.9415],  # 23
    [24, "Cr", "Chromium", 51.9961],  # 24
    [25, "Mn", "Manganese", 54.938045],  # 25
    [26, "Fe", "Iron", 55.845],  # 26
    [27, "Co", "Cobalt", 58.933195],  # 27
    [28, "Ni", "Nickel", 58.6934],  # 28
    [29, "Cu", "Copper", 63.546],  # 29
    [30, "Zn", "Zinc", 65.38],  # 30
    [31, "Ga", "Gallium", 69.723],  # 31
    [32, "Ge", "Germanium", 72.64],  # 32
    [33, "As", "Arsenic", 74.92160],  # 33
    [34, "Se", "Selenium", 78.96],  # 34
    [35, "Br", "Bromine", 79.904],  # 35
    [36, "Kr", "Krypton", 83.798],  # 36
    [37, "Rb", "Rubidium", 85.4678],  # 37
    [38, "Sr", "Strontium", 87.62],  # 38
    [39, "Y", "Yttrium", 88.90585],  # 39
    [40, "Zr", "Zirconium", 91.224],  # 40
    [41, "Nb", "Niobium", 92.90638],  # 41
    [42, "Mo", "Molybdenum", 95.96],  # 42
    [43, "Tc", "Technetium", None],  # 43
    [44, "Ru", "Ruthenium", 101.07],  # 44
    [45, "Rh", "Rhodium", 102.90550],  # 45
    [46, "Pd", "Palladium", 106.42],  # 46
    [47, "Ag", "Silver", 107.8682],  # 47
    [48, "Cd", "Cadmium", 112.411],  # 48
    [49, "In", "Indium", 114.818],  # 49
    [50, "Sn", "Tin", 118.710],  # 50
    [51, "Sb", "Antimony", 121.760],  # 51
    [52, "Te", "Tellurium", 127.60],  # 52
    [53, "I", "Iodine", 126.90447],  # 53
    [54, "Xe", "Xenon", 131.293],  # 54
    [55, "Cs", "Caesium", 132.9054519],  # 55
    [56, "Ba", "Barium", 137.327],  # 56
    [57, "La", "Lanthanum", 138.90547],  # 57
    [58, "Ce", "Cerium", 140.116],  # 58
    [59, "Pr", "Praseodymium", 140.90765],  # 59
    [60, "Nd", "Neodymium", 144.242],  # 60
    [61, "Pm", "Promethium", None],  # 61
    [62, "Sm", "Samarium", 150.36],  # 62
    [63, "Eu", "Europium", 151.964],  # 63
    [64, "Gd", "Gadolinium", 157.25],  # 64
    [65, "Tb", "Terbium", 158.92535],  # 65
    [66, "Dy", "Dysprosium", 162.500],  # 66
    [67, "Ho", "Holmium", 164.93032],  # 67
    [68, "Er", "Erbium", 167.259],  # 68
    [69, "Tm", "Thulium", 168.93421],  # 69
    [70, "Yb", "Ytterbium", 173.054],  # 70
    [71, "Lu", "Lutetium", 174.9668],  # 71
    [72, "Hf", "Hafnium", 178.49],  # 72
    [73, "Ta", "Tantalum", 180.94788],  # 73
    [74, "W", "Tungsten", 183.84],  # 74
    [75, "Re", "Rhenium", 186.207],  # 75
    [76, "Os", "Osmium", 190.23],  # 76
    [77, "Ir", "Iridium", 192.217],  # 77
    [78, "Pt", "Platinum", 195.084],  # 78
    [79, "Au", "Gold", 196.966569],  # 79
    [80, "Hg", "Mercury", 200.59],  # 80
    [81, "Tl", "Thallium", 204.3833],  # 81
    [82, "Pb", "Lead", 207.2],  # 82
    [83, "Bi", "Bismuth", 208.98040],  # 83
    [84, "Po", "Polonium", None],  # 84
    [85, "At", "Astatine", None],  # 85
    [86, "Rn", "Radon", None],  # 86
    [87, "Fr", "Francium", None],  # 87
    [88, "Ra", "Radium", None],  # 88
    [89, "Ac", "Actinium", None],  # 89
    [90, "Th", "Thorium", 232.03806],  # 90
    [91, "Pa", "Protactinium", 231.03588],  # 91
    [92, "U", "Uranium", 238.02891],  # 92
    [93, "Np", "Neptunium", None],  # 93
    [94, "Pu", "Plutonium", None],  # 94
    [95, "Am", "Americium", None],  # 95
    [96, "Cm", "Curium", None],  # 96
    [97, "Bk", "Berkelium", None],  # 97
    [98, "Cf", "Californium", None],  # 98
    [99, "Es", "Einsteinium", None],  # 99
    [100, "Fm", "Fermium", None],  # 100
    [101, "Md", "Mendelevium", None],  # 101
    [102, "No", "Nobelium", None],  # 102
    [103, "Lr", "Lawrencium", None],  # 103
    [104, "Rf", "Rutherfordium", None],  # 104
    [105, "Db", "Dubnium", None],  # 105
    [106, "Sg", "Seaborgium", None],  # 106
    [107, "Bh", "Bohrium", None],  # 107
    [108, "Hs", "Hassium", None],  # 108
    [109, "Mt", "Meitnerium", None],  # 109
    [110, "Ds", "Darmstadtium", None],  # 110
    [111, "Rg", "Roentgenium", None],  # 111
    [112, "Cn", "Copernicium", None],  # 112
    [113, "Uut", "Ununtrium", None],  # 113
    [114, "Uuq", "Ununquadium", None],  # 114
    [115, "Uup", "Ununpentium", None],  # 115
    [116, "Uuh", "Ununhexium", None],  # 116
    [117, "Uus", "Ununseptium", None],  # 117
    [118, "Uuo", "Ununoctium", None],  # 118
]

symbol_map = {
    "H": 1,
    "He": 2,
    "Li": 3,
    "Be": 4,
    "B": 5,
    "C": 6,
    "N": 7,
    "O": 8,
    "F": 9,
    "Ne": 10,
    "Na": 11,
    "Mg": 12,
    "Al": 13,
    "Si": 14,
    "P": 15,
    "S": 16,
    "Cl": 17,
    "Ar": 18,
    "K": 19,
    "Ca": 20,
    "Sc": 21,
    "Ti": 22,
    "V": 23,
    "Cr": 24,
    "Mn": 25,
    "Fe": 26,
    "Co": 27,
    "Ni": 28,
    "Cu": 29,
    "Zn": 30,
    "Ga": 31,
    "Ge": 32,
    "As": 33,
    "Se": 34,
    "Br": 35,
    "Kr": 36,
    "Rb": 37,
    "Sr": 38,
    "Y": 39,
    "Zr": 40,
    "Nb": 41,
    "Mo": 42,
    "Tc": 43,
    "Ru": 44,
    "Rh": 45,
    "Pd": 46,
    "Ag": 47,
    "Cd": 48,
    "In": 49,
    "Sn": 50,
    "Sb": 51,
    "Te": 52,
    "I": 53,
    "Xe": 54,
    "Cs": 55,
    "Ba": 56,
    "La": 57,
    "Ce": 58,
    "Pr": 59,
    "Nd": 60,
    "Pm": 61,
    "Sm": 62,
    "Eu": 63,
    "Gd": 64,
    "Tb": 65,
    "Dy": 66,
    "Ho": 67,
    "Er": 68,
    "Tm": 69,
    "Yb": 70,
    "Lu": 71,
    "Hf": 72,
    "Ta": 73,
    "W": 74,
    "Re": 75,
    "Os": 76,
    "Ir": 77,
    "Pt": 78,
    "Au": 79,
    "Hg": 80,
    "Tl": 81,
    "Pb": 82,
    "Bi": 83,
    "Po": 84,
    "At": 85,
    "Rn": 86,
    "Fr": 87,
    "Ra": 88,
    "Ac": 89,
    "Th": 90,
    "Pa": 91,
    "U": 92,
    "Np": 93,
    "Pu": 94,
    "Am": 95,
    "Cm": 96,
    "Bk": 97,
    "Cf": 98,
    "Es": 99,
    "Fm": 100,
    "Md": 101,
    "No": 102,
    "Lr": 103,
    "Rf": 104,
    "Db": 105,
    "Sg": 106,
    "Bh": 107,
    "Hs": 108,
    "Mt": 109,
    "Ds": 110,
    "Rg": 111,
    "Cn": 112,
    "Uut": 113,
    "Uuq": 114,
    "Uup": 115,
    "Uuh": 116,
    "Uus": 117,
    "Uuo": 118,
}
# END: from phonopy


class Mole(object):
	def __init__(self, moleTypeName, symbols, coordinates, charges):
		self.__MoleTypeName = moleTypeName
		self.__AtomicSymbols = tuple(symbols)
		self.__AtomicNumbers = tuple([symbol_map[symbol] for symbol in self.__AtomicSymbols])
		self.__AtomicWeights = tuple([atom_data[num][3] for num in self.__AtomicNumbers])
		self.__AtomicCharges = tuple(charges)
		self.__AtomicCoordinates = np.array(coordinates, dtype=np.double)
		self.__MoleCharge = 0
		self.__MoleSpin = 0.0

		weights = np.array(self.__AtomicWeights)
		self.__MoleMass = weights.sum()
		self.__MassCenter = np.sum(self.__AtomicCoordinates * weights.reshape((-1, 1)), axis=0) / self.__MoleMass

	def getMoleTypeName(self):
		return self.__MoleTypeName

	def natoms(self):
		return len(self.__AtomicSymbols)

	def getMoleCharge(self):
		return self.__MoleCharge

	def getMoleSpin(self):
		return self.__MoleSpin

	def setMoleCharge(self, charge):
		self.__MoleCharge = charge

	def setMoleSpin(self, spin):
		self.__MoleSpin = spin

	def getAtomicCoordinates(self, move=np.array([0.0, 0.0, 0.0], dtype=np.double), factor=1):
		return (self.__AtomicCoordinates + move) * factor

	def getAtomicSymbols(self):
		return self.__AtomicSymbols

	def getAtomicCharges(self):
		return self.__AtomicCharges

	def getMoleMass(self):
		return self.__MoleMass

	def getMassCenter(self):
		return self.__MassCenter.copy()

	def renewAtomicCharges(self, newCharges):
		self.__AtomicCharges = tuple(newCharges)

	def move(self, vector=np.array([0.0, 0.0, 0.0], dtype=np.double)):
		ret = copy(self)
		ret.__AtomicCoordinates = ret.__AtomicCoordinates + vector
		ret.__MassCenter = ret.__MassCenter + vector
		return ret

def loadcar(file):
	'''
	Extract molecular informations from .car file
	return a list of instances of Mole class
	'''
	with open(file, 'r') as f:
		lines = [line.rstrip() for line in f.readlines()]

	if lines[1] == 'PBC=ON':
		if lines[4][63:80].strip() != '(P1)':
			raise ValueError('The symmetry of structure described in .car file should be P1')
		box = np.zeros((3, 3), dtype=np.double)
		a, b, c, alpha, beta, gamma = map(float, \
			[lines[4][3:13], lines[4][13:23], lines[4][23:33], lines[4][33:43], lines[4][43:53], lines[4][53:63]])
		box[0, 0] = a
		box[1, :2] = b * np.cos(np.deg2rad(gamma)), b * np.sin(np.deg2rad(gamma))
		box[2, 0] = c * np.cos(np.deg2rad(beta))
		box[2, 1] = (b * c * np.cos(np.deg2rad(alpha)) - box[2, 0] * box[1, 0]) / box[1, 1]
		box[2, 2] = np.sqrt(c * c - box[2, 0] * box[2, 0] - box[2, 1] * box[2, 1])
		index = 5
	elif lines[1] == 'PBC=OFF':
		box = None
		index = 4
	else:
		raise ValueError('The second line should be \'PBC=ON\' or \'PBC=OFF\'')

	moles = []
	while lines[index][:3] != 'end':
		typename = lines[index][51:55].strip()
		symbols, coordinates, charges = [], [], []
		while lines[index][:3] != 'end':
			symbols.append(lines[index][71:73].strip())
			coordinates.append(lines[index][6:50].strip().split())
			charges.append(float(lines[index][74:].strip()))
			index += 1
		moles.append(Mole(typename, symbols, np.array(coordinates, dtype=np.double), charges))
		index += 1

	return box, moles

def loadgro(file):
	'''
	Extract molecular informations from .gro file
	return a list of instances of Mole class
	'''
	with open(file, 'r') as f:
		lines = [line.rstrip() for line in f.readlines()]

	moles = []
	natoms = int(lines[1])
	boxv = np.array(list(map(float, lines[2 + natoms].split()))) * 10
	box = np.diag(np.array(boxv)[:3])
	if len(boxv) > 3:
		box[0, 1:] = boxv[3:5]
		box[1, ::2] = boxv[5:7]
		box[2, :2] = boxv[7:]
	if not np.any(box): box = None
	atoms = lines[2 : 3 + natoms]
	n = 0
	while n < natoms:
		name = atoms[n][:10].strip()
		typename = atoms[n][5:10].strip()
		coordinates = []
		symbols = []
		for nextn in range(n, natoms + 1):
			coordinates.append(list(map(float, atoms[nextn][20:44].split())))
			symbols.append(re.sub(r'[0-9]+.*', '' ,atoms[nextn][10:15]).strip())
			if nextn + 1 == natoms or atoms[nextn + 1][:10].strip() != name:
				break
		n = nextn + 1
		moles.append(Mole(typename, symbols, np.array(coordinates) * 10, [0.0 for sym in symbols]))

	return box, moles

class cluster(object):
	def __init__(self, moles):
		if not isinstance(moles, (tuple, list, str)):
			raise ValueError('The argument \'mole\' should be tuple, list or str')
		if isinstance(moles, str):
			sufix = moles[-4:]
			if moles[-4:] != '.car':
				raise ValueError('The structure file should in .car format')
			box, moles = loadcar(moles)
			if box is not None:
				raise ValueError('Periodic system is not supported')

		masscenters = np.array([mole.getMassCenter() for mole in moles], dtype=np.double)
		rn = []
		r = masscenters - masscenters[0]
		rn = np.linalg.norm(r, axis=1)
		sortIndex = self.__argsort(rn)
		moles = [moles[index] for index in sortIndex]
		self.__Moles = moles
		self.__Distances = rn[sortIndex]

	def __argsort(self, iterable, reverse=False):
		length = len(iterable)
		return sorted(range(length), key=lambda index: round(iterable[index], 8), reverse=reverse)

	def nmoles(self):
		return len(self.__Moles)

	def natoms(self):
		return sum([mole.natoms() for mole in self.__Moles])

	def setMoleCharge(self, charge):
		self.__Moles[0].setMoleCharge(charge)

	def setMoleSpin(self, spin):
		self.__Moles[0].setMoleSpin(spin)

	def renewAtomicCharges(self, index, charges):
		self.__Moles[index].renewAtomicCharges(charges)

	def getMoleNames(self):
		return [mole.getMoleTypeName() for mole in self.__Moles]

	def polarize(self, centerCalculator, polCalculator, polRadius, tolerance=1E-05):

		polRegion = np.where(self.__Distances <= polRadius)[0].tolist()

		converged = False
		nloop = 0
		while True:
			QMindex = 0; MMindexs = [idx for idx in range(self.nmoles()) if idx != QMindex]
			QMMole = self.__Moles[QMindex]; MMMoles = [self.__Moles[index] for index in MMindexs]
			e, charges = centerCalculator.run(QMMole, MMMoles, jobname='mole-{:d}'.format(QMindex))
			self.__Moles[QMindex].renewAtomicCharges(charges)

			E = e
			if nloop == 0:
				print('Iteration {:02d}: E = {: .10f}'.format(nloop, E), flush=True)
			else:
				dE = E - lastE
				print('Iteration {:02d}: E = {: .10f}  dE = {: .10f}'.format(nloop, E, dE), flush=True)
				if abs(dE) < tolerance:
					converged = True

			if converged:
				print('Converged!', flush=True)
				break

			lastE = E
			nloop += 1

			for index in polRegion:
				if index == QMindex: continue
				QMindex = index; MMindexs = [idx for idx in range(self.nmoles()) if idx != QMindex]
				QMMole = self.__Moles[QMindex]; MMMoles = [self.__Moles[idx] for idx in MMindexs]
				e, charges = polCalculator.run(QMMole, MMMoles, jobname='mole-{:d}'.format(QMindex))
				self.__Moles[QMindex].renewAtomicCharges(charges)

			self.dumpCar('cluster-{:02d}.car'.format(nloop))
			os.system('mkdir log-{:02d}; mv mole-*.log log-{:02d}; cp mole-0.chk log-{:02d}'.format(nloop, nloop, nloop))

	def dumpCar(self, fcar='cluster.car'):
		atomNameformat = '{:s}{:d}'.format
		atomInfoformat = '{0:5s} {1[0]:14.9f} {1[1]:14.9f} {1[2]:14.9f} {2:4s} 1      xx      {3:2s} {4:9.6f}'.format

		nmole = 0
		carlines = ['!BIOSYM archive 3', 'PBC=OFF', 'CAR File', '!DATE Thu May 01 00:00:00 2019']
		for mole in self.__Moles:
			nmole += 1
			natom = 0
			moleName = mole.getMoleTypeName()
			for sym, coordinate, charge in zip(mole.getAtomicSymbols(), mole.getAtomicCoordinates(), mole.getAtomicCharges()):
				natom += 1
				atomName = atomNameformat(sym, natom)
				carlines.append(atomInfoformat(atomName, coordinate, moleName, sym, charge))
			carlines.append('end')
		carlines.append('end')
		with open(fcar, 'w') as f: f.writelines(['\n'.join(carlines), '\n'])

class Box(object):
	def __init__(self, carfile):
		self.__Box = None
		self.__Moles = None
		sufix = carfile[-4:]
		if sufix == '.car':
			self.__Box, self.__Moles = loadcar(carfile)
		elif sufix == '.gro':
			self.__Box, self.__Moles = loadgro(carfile)
		else:
			raise ValueError('The structure file should in .car or .gro format')
		if self.__Box is None:
			raise ValueError('The structure is not a periodic system')

	def nmoles(self):
		return len(self.__Moles)

	def genCluster(self, center, radius):
		def genCellVectors(n):
			cells = set()
			for i in range(0, n + 1):
				for j in range(0, n + 1 - i):
					k = n - i - j
					cells.add(( i,  j,  k)); cells.add((-i, -j, -k))
					cells.add((-i,  j,  k)); cells.add(( i, -j, -k))
					cells.add(( i, -j,  k)); cells.add((-i,  j, -k))
					cells.add(( i,  j, -k)); cells.add((-i, -j,  k))
			return np.matmul(np.array([cell for cell in cells]), self.__Box)

		nMole = self.nmoles()
		moles = [self.__Moles[center].move(np.array([0, 0, 0]))]
		masscenters = np.array([mole.getMassCenter() for mole in self.__Moles], dtype=np.double)

		for mole_index in range(nMole):
			notfound = 0
			curMole = self.__Moles[mole_index]
			i = 0
			while True:
				notfound += 1
				aimCellVector = genCellVectors(i)
				r = aimCellVector + masscenters[mole_index] - masscenters[center]
				rn = np.linalg.norm(r, axis=1)
				for index in np.where((rn <= radius) & (rn > 0.01))[0]:
					moles.append(curMole.move(aimCellVector[index]))
					notfound = 0
				i += 1
				if notfound > 3: break

		return cluster(moles)

class GauCalculator(object):
	gauformat = '\
%cpu=0-{ppn:d}\n\
%mem={mem:d}GB\n\
%chk={jobname:s}\n\
{methods:s}\n\
\n\
{jobname:s}\n\
\n\
{chgspin:s}\n\
{atomicInfo:s}\n\
\n'.format

	extchargeformat = '\
{extcharge:s}\n\
\n'.format

	def __init__(self, maxThreads, maxMem=48, basis='def2svp', method='b3lyp', otheropts=''):
		self.__MaxThreads = maxThreads
		self.__MaxMem = maxMem
		self.__QmMethods = '# {:s}/{:s} nosymm pop=mk iop(6/41=10,6/42=17) {:s}'.format(method.strip(), basis.strip(), otheropts)
		self.__MoleType = dict()

	def __dumpAtomicInfo(self, mole, start=1):
		atomicinfo = []

		infoformat = ' {0:5s} {1[0]:15.9f} {1[1]:15.9f} {1[2]:15.9f}'.format

		for sym, coordinate in zip(mole.getAtomicSymbols(), mole.getAtomicCoordinates()):
			atomicinfo.append(infoformat(sym, coordinate))

		return atomicinfo

	def __dumpPointCharge(self, mole):
		pchginfo = []
		pchginfoformat = ' {0[0]:15.9f} {0[1]:15.9f} {0[2]:15.9f} {1:15.9f}'.format
		for coordinate, chg in zip(mole.getAtomicCoordinates(), mole.getAtomicCharges()):
			pchginfo.append(pchginfoformat(coordinate, chg))
		return pchginfo

	def procedure(self):
		return 'Gaussian'

	def maxThreads(self):
		return self.__MaxThreads

	def run(self, QMMole, MMMoles=None, jobname='cluster'):
		if not isinstance(QMMole, Mole):
			raise ValueError('QMMole should be a Mole object')

		if not isinstance(MMMoles, (list, tuple)) and not None:
			raise ValueError('MMMoles should be a list, tuple or None')

		if MMMoles is not None and len(MMMoles) == 0: MMMoles = None

		atomicinfo, pchginfo = [], []
		charge, spin = 0, 0.0
		start = 1

		ainfo = self.__dumpAtomicInfo(QMMole, start=start)
		atomicinfo.extend(ainfo)
		start += QMMole.natoms()
		charge += QMMole.getMoleCharge()
		spin += QMMole.getMoleSpin()

		nqmatom = start - 1

		if MMMoles is not None:
			for mole in MMMoles:
				if not isinstance(mole, Mole):
					raise TypeError('Element in MMMoles is not an instance of \'Mole\'')
				pinfo = self.__dumpPointCharge(mole)
				pchginfo.extend(pinfo)

		chgspinstr = '{:d} {:d}'.format(charge, int(abs(spin) * 2 + 1))

		methodstr = self.__QmMethods
		if len(pchginfo) > 0: methodstr += ' charge'

		if os.access('.'.join([jobname, 'chk']), os.F_OK):
			methodstr += ' guess=read'

		inptxt = self.gauformat(ppn=self.__MaxThreads - 1, mem=self.__MaxMem, methods=methodstr, \
			jobname=jobname, chgspin=chgspinstr, atomicInfo='\n'.join(atomicinfo))
		if len(pchginfo) > 0: pchginfo[-1] += '\n\n'; inptxt += '\n'.join(pchginfo)

		finp = '.'.join([jobname, 'gjf'])
		fout = '.'.join([jobname, 'log'])

		with open(finp, 'w') as f:
			f.write(inptxt)
		with open(fout, 'wb') as f:
			exitcode = subprocess.call(['g16', finp], stdout=f)

		if exitcode != 0:
			print('{:s} terminated abnormally...'.format(self.procedure()), flush=True)
			exit()

		with open(fout, 'r') as f: txt = f.read()
		esps = re.findall(r' ESP charges:\n.*?\n(.*?)(?=\n Sum of ESP charges)', txt, re.S)[-1].splitlines()
		charges = [float(esp.split()[-1]) for esp in esps][:nqmatom]
		try:
			eqm = float(re.findall(r' Total Energy, E\(TD-HF/TD-DFT\).*?(-?[0-9]+\.[0-9]+)', txt)[-1])
		except:
			eqm = float(re.findall(r' SCF Done.*?(-?[0-9]+\.[0-9]+)', txt)[-1])

		if len(pchginfo) > 0:
			ecc = float(re.findall(r' Self energy of the charges.*?(-?[0-9]+\.[0-9]+)', txt, re.S)[-1])
		else:
			ecc = 0.0
		return eqm - ecc, charges

