#!/usr/bin/perl
use strict;
use warnings;

use Path::Class;
use autodie; # die if problem reading or writing a file

my $dir = dir("./samples"); # /tmp

my $file = $dir->file("foobar2000-errors.txt");

# Read in the entire contents of a file
my $content = $file->slurp();

# openr() returns an IO::File object to read from
my $file_handle = $file->openr();

# Read in line at a time
my $nbError = 0;
my $item = "";
my $error = "";
my %filesWithError;
while (my $line = $file_handle->getline()) {
	if ($line =~ /"(.*.flac)"/) {
		$item = "$1";
	}
	if ($item ne '' && $line =~ m/Error: Corrupted FLAC stream/) {
		$filesWithError{"$item"} = 1;
		$nbError++;
	}
}

print "$nbError errors from foobar2000\n";

$nbError = 0;
$file = $dir->file("dbpoweramp-errors.txt");
$content = $file->slurp();
$file_handle = $file->openr();

while (my $line = $file_handle->getline()) {
	if ($line =~ /'(\/.+\/[^\/]+.flac)'/) {
		$item = "$1";
	}
	if ($line =~ m/Encountered/ || $line =~ m/md5 did not match decoded data, file is corrupt./) {
		$filesWithError{"$item"} = 1;
		$nbError++;
	}
}

$file = $dir->file("results.txt"); # /tmp/file.txt

# Get a file_handle (IO::File object) you can write to
$file_handle = $file->openw();

my @result = keys %filesWithError;
foreach my $line ( @result ) {
    # Add the line to the file
    $file_handle->print($line . "\n");
}

print "$nbError errors from dbPowerAmp\n";