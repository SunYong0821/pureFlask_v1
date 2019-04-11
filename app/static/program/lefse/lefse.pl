#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
my($in,$map,$help,$lda,$outdir);
GetOptions(
 "i:s" =>\$in,
 "map:s" =>\$map,
 "LDA:s" =>\$lda,
 "help:s" =>\$help,
 "outdir:s" =>\$outdir
);
if( !$in || !$map || $help ){
	print STDERR <<USAGE;
=============================================================================
Descriptions: LEfSe analysis
Usage:
	perl $0 [options]
Options:
	* -i		input otu_tax_table
	* -LDA		set the threshold on the absolute value of the logarithmic LDA score
	* -map		group list
	* -outdir	output idr
	* -help		help
E.g.:
	perl $0 -i otu_tax_table.txt -map group.txt -LDA 2 -outdir /path/to/output
=============================================================================
USAGE
	die;
}
if(!$lda){
	$lda="2.0";
}
system("mkdir -p $outdir/out");
open LOG,">$outdir/run.log";
my $column_num=0;
my$time=0;
open IN,"$in" or die $!;
while(<IN>){
	chomp;
	$time++;
	my@line=split/\t/,$_;
	if($column_num == 0){
		$column_num=$#line;
	}else{
		if($line[-1] eq ""){
			print LOG "The last column is NULL\n";
			die;
		}
	}
	if($#line ne $column_num){
		my $column_real_num=$column_num+1;
		print LOG "Line $time is not $column_real_num columns\n";
		die;
	}
}close IN;

open OUT,">$outdir/lefse.sh";
my $cmd=<<EOF;
perl $Bin/lefse_input.pl -i $in -map $map -type tax -o $outdir/lefse_input.txt
$Bin/LEfSe/format_input.py $outdir/lefse_input.txt $outdir/LDA.in -c 1 -u 2 -o 1000000
$Bin/LEfSe/run_lefse.py $outdir/LDA.in $outdir/LDA.res -l $lda
$Bin/LEfSe/plot_res.py $outdir/LDA.res $outdir/out/LDA.pdf --format pdf --dpi 150 --width 16
$Bin/LEfSe/plot_cladogram.py $outdir/LDA.res $outdir/out/LDA.cladogram.pdf --format pdf --dpi 150 
convert -density 200 $outdir/out/LDA.pdf $outdir/out/LDA.png
convert -density 200 $outdir/out/LDA.cladogram.pdf $outdir/out/LDA.cladogram.png
EOF
print OUT $cmd;
close OUT;
system("sh $outdir/lefse.sh");

