#!/usr/bin/perl -w
use strict;
use Getopt::Long;
my($in,$out);
GetOptions(
 "i:s" =>\$in,
 "o:s" =>\$out
);
open IN,"$in" or die $!;
open OUT,">$out";
my $head=<IN>;
print OUT $head;
while(<IN>){
	chomp;
	my@line=split/\t/,$_;
	print OUT $line[0];
	for my$u(1..$#line){
		my$num=$line[$u]*100;
		print OUT "\t$num";
	}
	print OUT "\n";
}close IN;close OUT;
