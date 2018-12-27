#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$count1Col,$count2Col,$vs,$geneCol,$bcv);
GetOptions (
	"i:s" => \$infile,
	"count1col:s" => \$count1Col,
	"count2col:s" => \$count2Col,
	"prefix:s"  => \$vs,
	"genecol:i" => \$geneCol,
	"bcv:f"	    => \$bcv
);

if (!$infile  || !$count1Col || !$count2Col || !$vs || !$geneCol || !$bcv) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Differently Expression Analysis using edgeR software
Usage:
	perl $0 [options]
Options:
	* -i			input Diff Analysis Results
	* -count1col		expression read counts column(s) of sample1 or group1 in input Diff Analysis Results(E.g:3 or 3-5)
	* -count2col		expression read counts column(s) of sample2 or group2 in input Diff Analysis Results(E.g:3 or 3-5)
	* -genecol		Gene name column
	* -prefix		prefix for outfiles and the title in the images
	* -bcv			square-rootdispersion. 
				datasets arising from well-controlled experiments are 0.3 for human data,0.1 for data on genetically identical model organisms 				       or 0.01 for technical replicates
E.g.:
	With no Biological duplication sample
		perl $0 -i infile -count1col 2 -count2col 3 -genecol 1 -prefix A-vs-B 
	With Biological duplication sample
		perl $0 -i infile -count1col 2-4 -count2col 5-7 -genecol 1 -prefix A-vs-B
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
open LOG,">$odir/run.log";
my $Rscript="Rscript";

&check_parameters($count1Col,$count2Col,$geneCol,$bcv);

open IN,$infile;
<IN>;
chdir"$odir";
open OUT,">$vs.matrix";
my $ffff=0;
my %checkgene;
my ($group1,$group2);
while(<IN>){
	chomp;
	my @a=split /\t/,$_;
	my $a=\@a;
	my ($num1,@exp1)=&getexp($a,$count1Col);
	my ($num2,@exp2)=&getexp($a,$count2Col);
	($group1,$group2)=($num1,$num2);
	if($geneCol>$#a+1){
		print LOG "Gene column out of range!\n";
		die;
	}
	if($checkgene{$a[$geneCol-1]}){
		print LOG "$a[$geneCol-1]:\tthere are same genes in the Gene column!\n";
		die;
	}
	$checkgene{$a[$geneCol-1]}=1;
	if($ffff==0){
		$ffff++;
		for(my $i=1;$i<=$num1;$i++){
			print OUT "\tCase$i";
		}
		for(my $i=1;$i<=$num2;$i++){
			print OUT "\tControl$i";
		}
		print OUT "\n";
	}
	my $exp1=join("\t",@exp1);
	my $exp2=join("\t",@exp2);
	print OUT "$a[$geneCol-1]\t$exp1\t$exp2\n";
}
close IN;
close OUT;

my $disp=$bcv*$bcv;

system("$Rscript $Bin/edgeRdiff_new.R $vs.matrix tpmp.edgeR A $group1 B $group2 $disp");
my %result;
open IN,"tpmp.edgeR";
<IN>;
while(<IN>){
	chomp;
	my @a=split /\t/,$_;
	$result{$a[0]}="$a[1]\t$a[3]\t$a[4]";
}
close IN;

open IN,$infile;
open OUT,">out/$vs.edgeR.xls";
my $head=<IN>;
chomp($head);
print OUT "$head\tlogFC\tPValue\tFDR\n";
while(<IN>){
	chomp;
	my $gene=(split /\t/,$_)[$geneCol-1];
	if($result{$gene}){
		print OUT "$_\t$result{$gene}\n";
	}
}
close IN;
close OUT;

my $obj=Archive::Zip->new();
my $fff="out/$vs.edgeR.xls";
$obj->addFile($fff);
$obj->writeToFileNamed("out.zip");

sub getexp{
	my ($a,$column)=@_;
	my @a=@$a;
	if($column=~/^\d+-\d+$/){
		my ($start,$end)=split /-/,$column;
		my $num=abs($end-$start)+1;
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
		return($num,@exp);
	}
	else{
		$column--;
		if($column>$#a){
			print LOG "exp column out of range!\n";
			die;
		}
		my @exp;
		push @exp,$a[$column];
		return(1,@exp);
	}
}

sub check_parameters{
###&check_parameters($foldchange,$conut1Col,$conut2Col,$geneCol);
	my ($fpkm1,$fpkm2,$pC,$bv)=@_;
	$bv=~s/-//;
	$bv=~s/\.//;
	if($bv!~/^\d+$/){
		print LOG "BCV value error!\n";
		die;
	}
	if($pC!~/^\d+$/){
		print LOG "Gene name column error!\n";
		die;
	}
	if($fpkm1!~/-/){
		if($fpkm1!~/^\d+$/){
			print LOG "EXP1 column error!\n";
			die;
		}
	}
	else{
		if($fpkm1!~/^\d+-\d+$/){
			print LOG "EXP1 column error!\n";
			die;
		}
	}
	if($fpkm2!~/-/){
                if($fpkm2!~/^\d+$/){
			print LOG "EXP2 column error!\n";
                        die;
                }
        }
        else{
                if($fpkm2!~/^\d+-\d+$/){
			print LOG "EXP1 column error!\n";
                        die;
                }
        }
	return(1);
}
