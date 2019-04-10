#!/usr/bin/perl -w
use strict;
use FindBin '$Bin';
use Getopt::Long;
my($in,$outdir,$prefix,$type);
GetOptions(
 "i:s" =>\$in,
 "outdir:s" =>\$outdir
);
if( !$in || !$outdir  ){
	print STDERR <<USAGE;
=============================================================================
Descriptions: plot spearman_heatmap
Usage:
	perl $0 [options]
Options:
	* -i		input abundance table
	* -outdir	output dir
E.g.:
	perl $0 -i otu_table.txt -outdir /path/to/output
=============================================================================
USAGE
	die;
}
open LOG,">$outdir/run.log";
system("mkdir -p $outdir/out");
open IN,"$in" or die $!;
my $column_num=0;
my $time=0;
my $head=<IN>;
my@head_id=split/\t/,$head;
while(<IN>){
        chomp;
        $time++;
        my@line=split/\t/,$_;
        if($column_num == 0){
                $column_num=$#line;
        }
        if($#line ne $column_num){
                my $column_real_num=$column_num+1;
                print LOG "Line $time is not $column_real_num columns\n";
                die;
        }
	for my$u(1..$#line){
		if($line[$u] eq " "){
			my$co=$u+1;
			print LOG "Line $time column $co is NULL\n";
			die;
		}
	}
	
}close IN;
open OUT,">$outdir/spearman.sh";
my $cmd=<<EOF;
Rscript $Bin/diff_spearman.R $in $outdir/out
EOF
	print OUT $cmd;
	close OUT;
system("sh $outdir/spearman.sh");
