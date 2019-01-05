#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$n11,$n12,$n21,$n22,$method,$prefix);
GetOptions (
	"i:s" => \$infile,
	"n11:i" => \$n11,
	"n12:i" => \$n12,
	"n21:i"  => \$n21,
	"n22:i" => \$n22,
	"method:s" => \$method,
	"prefix:s" => \$prefix
);

if (!$infile  || !$n11 || !$n12 || !$n21 || !$n22 || !$method || !$prefix) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Fisher's exact Test
Usage:
	perl $0 [options]
Options:
	* -i			input Analysis Results
	* -n11			column of the number of times <word1><word2> occur together
	* -n12			column of the number of times <word1> occurs with some word other than word2
	* -n21			column of the number of times <word2> occurs with some word other than word1
	* -n22			column of the number of times some word other than word1 occurs and some word other than word2 occurs
	* -method		can be left,right,twotailed
	* -prefix		output prefix
E.g.:
		perl $0 -i infile -count1col 2-4 -count2col 5-7 -genecol 1 -prefix A-vs-B
=============================================================================
USAGE
	die;
}
#use if CONDITION, MODULE => ARGUMENTS;
if($method eq "left"){
	#use Text::NSP::Measures::2D::Fisher::left;
	require("$Bin/left.pm");
}
elsif($method eq "right"){
	#use Text::NSP::Measures::2D::Fisher::right.pm;
	require("$Bin/right.pm");
}
else{
	#use Text::NSP::Measures::2D::Fisher::twotailed.pm;
	require("$Bin/twotailed.pm");
}
$infile=abs_path($infile);
my $odir=dirname($infile);
my $check="$odir/out";
unless(-d $check){
        mkdir($check);
}
open LOG,">$odir/run2.log";

&check_parameters($n11,$n12,$n21,$n22);

open IN,$infile;
my $head=<IN>;
chomp($head);
chdir"$odir";
open OUT,">out/$prefix.xls";
print OUT "$head\tFisher $method Pvalue\n";
while(<IN>){
	chomp;
	my @a=split /\t/,$_;
	if($n11>$#a+1){
		print LOG "n11 column out of range!\n";
		die;
	}
	if($n12>$#a+1){
                print LOG "n12 column out of range!\n";
                die;
        }
	if($n21>$#a+1){
                print LOG "n21 column out of range!\n";
                die;
        }
	if($n22>$#a+1){
                print LOG "n22 column out of range!\n";
                die;
        }
	#print OUT "$a[$geneCol-1]\t$exp1\t$exp2\n";
	if($a[$n11-1]!~/^\d+$/){
		print LOG "$_\nn11 value error!\n";
		die;
	}
	if($a[$n12-1]!~/^\d+$/){
                print LOG "$_\nn12 value error!\n";
                die;
        }
	if($a[$n21-1]!~/^\d+$/){
                print LOG "$_\nn21 value error!\n";
                die;
        }
	if($a[$n22-1]!~/^\d+$/){
                print LOG "$_\nn22 value error!\n";
                die;
        }
	my $n1p=$a[$n11-1]+$a[$n12-1];
	my $np1=$a[$n11-1]+$a[$n21-1];
	my $npp=$a[$n11-1]+$a[$n12-1]+$a[$n21-1]+$a[$n22-1];
	my $pvalue=calculateStatistic(n11=>$a[$n11-1],n1p=>$n1p,np1=>$np1,npp=>$npp);
	print OUT "$_\t$pvalue\n";
}
close IN;
close OUT;


my $obj=Archive::Zip->new();
my $fff="out/$prefix.xls";
$obj->addFile($fff);
$obj->writeToFileNamed("out.zip");
close LOG;
sub check_parameters{
	my ($fpkm1,$fpkm2,$pC,$bv)=@_;
	if($bv!~/^\d+$/){
		print LOG "n22 column error!\n";
		die;
	}
	if($pC!~/^\d+$/){
		print LOG "n21 column error!\n";
		die;
	}
	if($fpkm1!~/^\d+$/){
		print LOG "n11 column error!\n";
		die;
	}
	if($fpkm2!~/^\d+$/){
		print LOG "n12 column error!\n";
		die;
	}
	return(1);
}
