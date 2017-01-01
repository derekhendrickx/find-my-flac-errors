import re

import trackWithError

def main():
	errorFile = open('samples/foobar2000-errors.txt', 'r')
	errors = errorFile.readlines()
	errorsDict = {}

	index = -1
	for i in range(len(errors)):
		line = errors[i]
		if re.search(r'List of undecodable items:', line):
			index = i
			break

	nbErrorsFoobar = 0
	for i in range(index, len(errors)):
		line = errors[i]
		match = re.search(r'[^".]+\\.+\\([^\\]+.flac)', line)
		if match:
			trackName = match.group(1)
			error = trackWithError.TrackWithError(trackName, match.group())
			if trackName in errorsDict:
				error = errorsDict.get(trackName)
				error.addCount()
			errorsDict[trackName] = error
			nbErrorsFoobar += 1

	errorFile.close()

	errorFile = open('samples/dbpoweramp-errors.txt', 'r')
	errors = errorFile.readlines()

	index = -1
	nbErrorsDbPowerAmp = 0
	for i in range(len(errors)):
		line = errors[i]
		match = re.search(r'/.+/([^/]+.flac)', line)
		if match:
			trackName = match.group(1)
			error = trackWithError.TrackWithError(trackName, match.group())
			if trackName in errorsDict:
				error = errorsDict.get(trackName)
				error.addCount()
			errorsDict[trackName] = error
		if (re.search(r'Encountered', line) or re.search(r'md5 did not match decoded data, file is corrupt.', line)):
			nbErrorsDbPowerAmp += 1

	errorFile.close()

	print(nbErrorsFoobar, 'FLAC errors from foobar2000')
	print(nbErrorsDbPowerAmp, 'FLAC errors from dbPowerAmp')
	print(len(errorsDict))

	errorFile = open('samples/results.txt', 'w')
	errorFile.write('Track name;Path;Count;\n')
	for k, v in errorsDict.items():
		errorFile.write(k + ';' + v.path + ';' + str(v.count) + ';\n')

if __name__ == "__main__":
	main()
