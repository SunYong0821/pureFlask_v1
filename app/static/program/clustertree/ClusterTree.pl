#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$count1Col,$vs,$method, $width, $height);
GetOptions (
	"i:s" => \$infile,
	"expcol:s" => \$count1Col,
	"prefix:s"  => \$vs,
	"method:s"  => \$method,
	"width:s" => \$width,
	"height:s" => \$height
);

unless($method){
	$method="complete";
}
if (!$infile  || !$count1Col || !$vs || !$method) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Generate cluster tree using R cluster package
Usage:
	perl $0 [options]
Options:
	* -i			input Diff Analysis Results
	* -expcol		expression columns of sample1 or group1 in input Diff Analysis Results(3-5)
	* -prefix		prefix for outfiles and the title in the images
	* -method		cluster method,can be:
				"ward.D"---离差平方和法
				"ward.D2"---离差平方和法，与ward.D区别在于每次聚类更新前将离差进行了平方
				"single"---最短距离法
				"complete"---最长距离法,默认选项
				"average"---类平均法，同"UPGMA"
				"mcquitty"---Mcquitty相似法,同"WPGMA"
				"median"---中间距离法,同"WPGMC"
				"centroid"---重心法,同"UPGMC"
E.g.:
		perl $0 -i example.xls -expcol 1-9 -prefix a
=============================================================================
USAGE
	die;
}
$infile=abs_path($infile);
my $odir=dirname($infile);
my $check="$odir/out";
unless(-d $check){
        mkdir($check);
}
open LOG,">$odir/run2.log";
my $Rscript="Rscript";

&check_parameters($count1Col);

open IN,$infile;
#<IN>;
chdir"$odir";
open OUT,">$vs.matrix";
while(<IN>){
	chomp;
	my @a=split /\t/,$_;
	my $a=\@a;
	my (@exp)=&getexp($a,$count1Col);
	my $exp=join("\t",@exp);
	print OUT "$exp\n";
}
close IN;
close OUT;


system("$Rscript $Bin/cluster.R $vs.matrix out/$vs.pdf $method $width $height");
close LOG;
my $obj=Archive::Zip->new();
my $fff="out/$vs.pdf";
$obj->addFile($fff);
$obj->writeToFileNamed("out.zip");

sub getexp{
	my ($a,$column)=@_;
	my @a=@$a;
	if($column=~/^\d+-\d+$/){
		my ($start,$end)=split /-/,$column;
		my ($min,$max)=($start-1,$end-1);
		if($min>$max){
			($max,$min)=($start-1,$end-1);
		}
		if($max>$#a){
			print LOG "exp column out of range!\n";
			die;
		}
		my @exp;
		for(my $i=$min;$i<=$max;$i++){
			push @exp,$a[$i];
		}
		return(@exp);
	}
	else{
		$column--;
		if($column>$#a){
			print LOG "exp column out of range!\n";
			die;
		}
		my @exp;
		push @exp,$a[$column];
		return(@exp);
	}
}

sub check_parameters{
	my ($fpkm1)=@_;
	if($fpkm1!~/^\d+-\d+$/){
		print LOG "EXP column error!\n";
		die;
	}
	return(1);
}
