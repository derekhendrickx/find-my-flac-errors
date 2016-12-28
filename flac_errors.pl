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
while (my $line = $file_handle->getline()) {
	# if ($line =~ m/Error converting/) {
	# 	$nbError++;
	# }
	if ($line =~ /"(.*.flac)"/) {
		$item = "$1";
	}
	if ($item ne '' && $line =~ m/Error: Corrupted FLAC stream/) {
		print "$item\tCorrupted FLAC\n";
		$nbError++;
	}
}

print "$nbError errors\n";