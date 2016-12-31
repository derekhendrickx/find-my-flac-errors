import re

errorFile = open('samples/foobar2000-errors.txt', 'r')
errors = errorFile.readlines()

index = -1
for i in range(len(errors)):
	line = errors[i]
	if re.search(r'List of undecodable items:', line):
		index = i

nbErrorsFoobar = 0
for i in range(index, len(errors)):
	line = errors[i]
	match = re.search(r'"(.*.flac)"', line)
	if match:
		nbErrorsFoobar += 1
		print(match.group(1))

errorFile.close()

errorFile = open('samples/dbpoweramp-errors.txt', 'r')
errors = errorFile.readlines()

index = -1
nbErrorsDbPowerAmp = 0
for i in range(len(errors)):
	line = errors[i]
	match = re.search(r'/.+/[^/]+.flac', line)
	if match:
		print(match.group())
	if (re.search(r'Encountered', line) or re.search(r'md5 did not match decoded data, file is corrupt.', line)):
		nbErrorsDbPowerAmp += 1

print(nbErrorsFoobar, 'FLAC errors from foobar2000')
print(nbErrorsDbPowerAmp, 'FLAC errors from dbPowerAmp')