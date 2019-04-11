#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my($in,$outdir,$map,$pre);
GetOptions(
 "i:s" =>\$in,
 "pre:s" =>\$pre,
 "map:s" =>\$map
);
if( !$in || !$map ){
        print STDERR <<USAGE;
=============================================================================
Descriptions: plot bar_tree
Usage:
        perl $0 [options]
Options:
        * -i            input abundance table
	* -map		group list
        * -outdir       output dir
        * -pre          title of plot
E.g.:
        perl $0 -i otu_table.txt -outdir bar_plot.pdf -pre geuns -map map.txt
=============================================================================
USAGE
        die;
}
$in=abs_path($in);
$outdir=dirname($in);
open IN,"$in" or die $!;
open LOG,">$outdir/run.log";
system("mkdir -p $outdir/out");
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
open OUT,">$outdir/tax_tree.sh";
my $cmd=<<EOF;
Rscript $Bin/bar_tree.R $in $map $pre $outdir/out
EOF
print OUT $cmd;
close OUT;
system("sh $outdir/tax_tree.sh");
#my $obj=Archive::Zip->new();
#my $fff="out/$pre\_bar_tree.pdf";
system(" cd $outdir && zip -r $outdir/out.zip out");
