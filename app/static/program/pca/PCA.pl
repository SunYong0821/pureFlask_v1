#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$count1Col,$vs,$geneCol);
GetOptions (
	"i:s" => \$infile,
	"expcol:s" => \$count1Col,
	"prefix:s"  => \$vs,
	"genecol:i" => \$geneCol,
);

if (!$infile  || !$count1Col || !$vs || !$geneCol ) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Differently Expression Analysis using DeSeq2 software
Usage:
	perl $0 [options]
Options:
	* -i			input Analysis Results
	* -expcol		expression columns of sample1 or group1 in input Analysis Results(E.g:3-5)
	* -genecol		Gene name column
	* -prefix		prefix for outfiles and the title in the images
E.g.:
		perl $0 -i infile -expcol 2-7 -genecol 1 -prefix A
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

&check_parameters($count1Col,$geneCol);

open IN,$infile;
my $head=<IN>;
chomp($head);
my @head=split /\t/,$head;
my $phead=\@head;
my @names=&getexp($phead,$count1Col);
chdir"$odir";
open OUT,">$vs.matrix";
print OUT "#ID";
my $outhead=join("\t",@names);
print OUT "\t$outhead\n";
for(my $i=0;$i<=$#names;$i++){
	$names[$i]="\"$names[$i]\"";
}
my $rnames=join(",",@names);
$rnames="c($rnames)";
while(<IN>){
	chomp;
	my @a=split /\t/,$_;
	my $a=\@a;
	my (@exp)=&getexp($a,$count1Col);
	if($geneCol>$#a+1){
		print LOG "Gene column out of range!\n";
		die;
	}
	my $exp=join("\t",@exp);
	print OUT "$a[$geneCol-1]\t$exp\n";
}
close IN;
close OUT;

open OUT,">$vs.pca.R";
print OUT <<RCODE;
library(ggplot2)
dat <- read.delim("./$vs.matrix", row.names = 1, header=TRUE,check.names=F,sep="\\t")
pca <- prcomp(t(dat))
result <- as.data.frame(pca\$x)
result\$rep <- $rnames
xmax=max(result\$PC1)*1.4
xmin=min(result\$PC1)
##p <- ggplot(result) + geom_point(aes(x=result\$PC1,y=result\$PC2,color=result\$rep)) + geom_text(aes(x=result\$PC1, y=result\$PC2, label=rownames(result),hjust=-0.65, color=result\$rep,size=.5))
p <- ggplot(result) + geom_point(aes(x=result\$PC1,y=result\$PC2,color=result\$rep)) + geom_text(aes(x=result\$PC1, y=result\$PC2, label=rownames(result),hjust=-0.05, color=result\$rep),size=4)+xlim(xmin,xmax)
p <- p + theme_bw()
p <- p + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) 
p <- p + theme(legend.title=element_blank()) + xlab("PC1") + ylab("PC2")
p <- p + theme(legend.position = "none")
pdf(file="out/$vs.pca.pdf")
print(p)
dev.off()
RCODE

system("$Rscript $vs.pca.R");

my $obj=Archive::Zip->new();
my $fff="out/$vs.pca.pdf";
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
		return(1,@exp);
	}
}

sub check_parameters{
	my ($fpkm1,$pC)=@_;
	if($pC!~/^\d+$/){
		print LOG "Gene name column error!\n";
		die;
	}
	if($fpkm1!~/^\d+-\d+$/){
		print LOG "EXP1 column error!\n";
		die;
	}
	return(1);
}
