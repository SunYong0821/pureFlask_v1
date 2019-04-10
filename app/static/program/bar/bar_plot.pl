#!/usr/bin/perl -w
use strict;
use FindBin '$Bin';
use Getopt::Long;
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
#my($in,$outdir,$prefix,$type);
my($in,$prefix,$type);
GetOptions(
 "i:s" =>\$in,
 "pre:s" =>\$prefix,
# "outdir:s" =>\$outdir,
 "type:s" =>\$type
);
#if( !$in || !$outdir  ){
if( !$in){
	print STDERR <<USAGE;
=============================================================================
Descriptions: plot bar_plot
Usage:
	perl $0 [options]
Options:
	* -i		input abundance table
	* -outdir	output dir
	* -pre		title of plot
	* -type		1 or 100(%)
E.g.:
	perl $0 -i otu_table.txt -outdir bar_plot.pdf -pre geuns -type 100
=============================================================================
USAGE
	die;
}
$in=abs_path($in);
my$outdir=dirname($in);
open LOG,">$outdir/run.log";
system("mkdir -p $outdir/out");
open IN,"$in" or die $!;
if(!$type){
	$type=100;
}
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
open OUT,">$outdir/bar_plot.sh";
if($type == 100 ){
	my $cmd=<<EOF;
Rscript $Bin/bar_plot.R $in $prefix $outdir/out
EOF
	print OUT $cmd;
	close OUT;
}else{
	my$cmd=<<EOF;
perl  $Bin/hundred.pl -i $in -o $outdir/change_table.txt
Rscript $Bin/bar_plot.R $outdir/change_table.txt $prefix $outdir/out
EOF
	print OUT $cmd;
	close OUT;
}

system("sh $outdir/bar_plot.sh");
#my $obj=Archive::Zip->new();
#my $fff="out/$prefix\_bar.pdf";
#my $fff="out";
#$obj->addFile($fff);
#$obj->writeToFileNamed("out.zip");
print "$outdir";
system("cd $outdir/ && zip -r $outdir/out.zip out");
