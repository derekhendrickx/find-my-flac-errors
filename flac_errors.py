#!/usr/bin/env python

'''
Find the errors in reports from foobar2000 and dbPowerAmp
'''

import re

import trackWithError

class FindFLACErrors:
	def __init__(self):
		self.errorsDict = {}
		self.nbErrors = [0, 0]

	def findErrors(self, program, files):
		options = {
			'foobar': self.findErrorsFromFoobar,
			'dbpoweramp': self.findErrorsFromDbPowerAmp
		}
		options.get(program)(files)

	def findErrorsFromFoobar(self, files):
		errorFile = open(files[0], 'r')
		errors = errorFile.readlines()	

		index = -1
		for i in range(len(errors)):
			line = errors[i]
			if re.search(r'List of undecodable items:', line):
				index = i
				break

		for i in range(index, len(errors)):
			line = errors[i]
			match = re.search(r'[^".]+\\.+\\([^\\]+.flac)', line)
			if match:
				trackName = match.group(1)
				normalizedTrackName = trackWithError.TrackWithError.normalizeName(trackName)
				error = trackWithError.TrackWithError(trackName, match.group())
				if normalizedTrackName in self.errorsDict:
					error = self.errorsDict.get(normalizedTrackName)
					error.addCount()
				self.errorsDict[normalizedTrackName] = error
				self.nbErrors[0] += 1

		errorFile.close()

	def findErrorsFromDbPowerAmp(self, files):
		errorFile = open(files[0], 'r')
		errors = errorFile.readlines()

		for i in range(len(errors)):
			line = errors[i]
			if re.search(r'^\s{3}', line) == None:
				match = re.search(r'\/.+\/([^\/]+.flac)', line)
			if match and (re.search(r'Encountered', line) or re.search(r'md5 did not match decoded data, file is corrupt.', line) or re.search(r'indicated sample count does not match decoded sample count, possible file corruption', line)):
				trackName = match.group(1)
				normalizedTrackName = trackWithError.TrackWithError.normalizeName(trackName)
				error = trackWithError.TrackWithError(trackName, match.group())
				if normalizedTrackName in self.errorsDict:
					error = self.errorsDict.get(normalizedTrackName)
					if error.count == 1:
						self.nbErrors[1] += 1
					error.addCount()
				self.errorsDict[normalizedTrackName] = error

		errorFile.close()

		errorFile = open(files[1], 'r')
		errors = errorFile.readlines()

		for i in range(0, len(errors), 3):
			line = errors[i]
			match = re.search(r'\/.+\/([^\/]+.flac)', line)
			if match:
				trackName = match.group(1)
				normalizedTrackName = trackWithError.TrackWithError.normalizeName(trackName)
				error = trackWithError.TrackWithError(trackName, match.group())
				if normalizedTrackName in self.errorsDict:
					error = self.errorsDict.get(normalizedTrackName)
					if error.count == 1:
						self.nbErrors[1] += 1
					error.addCount()
				self.errorsDict[normalizedTrackName] = error

		errorFile.close()

	def writeResults(self, file):
		print(self.nbErrors[0], 'FLAC errors from foobar2000')
		print(self.nbErrors[1], 'FLAC errors from dbPowerAmp')
		print('Total', len(self.errorsDict), 'errors')

		resultFile = open(file, 'w')
		resultFile.write('Track name;Path;Count;\n')
		i = 0
		for k, v in self.errorsDict.items():
			errorFile.write(v.name + ';' + v.path + ';' + str(v.count) + ';\n')
		
		resultFile.close()

	def main(self):
		self.findErrors('foobar', ['samples/foobar2000-errors.txt'])
		self.findErrors('dbpoweramp', ['samples/dbpoweramp-errors.txt', 'samples/dbpoweramp-infos.txt'])
		self.writeResults('samples/results.txt')

if __name__ == "__main__":
	FindFLACErrors().main()
