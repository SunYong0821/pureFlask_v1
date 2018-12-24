#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$Log2Col,$Exp1Col,$Exp2Col,$vs,$pCol);
our ($foldchange,$pvalue);
GetOptions (
	"i:s" => \$infile,
	"f:f" => \$foldchange,
	"log2col:i" => \$Log2Col,
	"exp1col:s" => \$Exp1Col,
	"exp2col:s" => \$Exp2Col,
	"pvalue:f"  => \$pvalue,
	"pCol:i"    => \$pCol,
	"prefix:s"  => \$vs
);

if (!$infile || !$Log2Col || !$Exp1Col || !$Exp2Col || !$vs || !$pvalue || !$pCol ||!$foldchange) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Generate MA plot
Usage:
	perl $0 [options]
Options:
	* -i			input Diff Analysis Results
	* -f			fold change cutoff
	* -log2col		log2 fold column in input Diff Analysis Results
	* -exp1col		expression column(s) of sample1 or group1 in input Diff Analysis Results(E.g:3 or 3-5)
	* -exp2col		expression column(s) of sample2 or group2 in input Diff Analysis Results(E.g:3 or 3-5)
	* -pvalue		pvalue/FDR for DEG
	* -pCol			pvalue/FDR column in input Diff Analysis Results
	* -prefix		prefix for outfiles and the title in the images
    Note:  fold change cutoff,pvalue and pCol pamameters were set to determine which gene is Differently Expressed. By default log2FC above 0 is Up, log2FC below 0 is Down.
E.g.:
	With no Biological duplication sample
		perl $0 -i infile -log2col 5 -exp1col 3 -exp2col 4 -pvalue 0.01 -pCol  11 -prefix A-vs-B -f 1
	With Biological duplication sample
		perl $0 -i infile -log2col 9 -exp1col 3-5 -exp2col 6-8 -pvalue 0.01 -pCol  11 -prefix A-vs-B -f 1
    Attention:
        When chose With Biological duplication sample Mode, the average expression value of each group will be use to do further analysis.
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
my $Xlab="A";
my $Ylab="M";
my $Rscript="$Bin/Rscript";
$foldchange=abs($foldchange);
&check_parameters($Log2Col,$Exp1Col,$Exp2Col,$pvalue,$pCol,$foldchange);

open IN,$infile;
<IN>;
chdir"$odir";
open OUT,">$vs.MA";
print OUT "logFC\t0\tUp/Down-Regulation\n";
my $upnum=0;
my $downnum=0;
my $nodeg=0;
while(<IN>){
	chomp;
	my @a=split /\t/,$_;
	my $a=\@a;
	my $type=&gettype($a,$Log2Col,$pCol);
	my $exp1=&getexp($a,$Exp1Col);
	my $exp2=&getexp($a,$Exp2Col);
	if($type eq "Up"){
		$upnum++;
	}
	elsif($type eq "Down"){
		$downnum++;
	}
	else{
		$nodeg++;
	}
	my $ma=$exp1*$exp2;
	print OUT "$a[$Log2Col-1]\t$ma\t$type\n";
}
close IN;
close OUT;

open OUT,">$vs.MA.R";
print OUT <<CMD;
pdf("out/$vs.MA-plot.pdf",width=10,height=10,pointsize=15)
data <- read.table("./$vs.MA", sep = "\\t", skip = 1)
no_degs_x <- data\$V2[ grepl("\\\\*",data\$V3,perl=TRUE) ]
no_degs_y <- data\$V1[ grepl("\\\\*",data\$V3,perl=TRUE) ]
degs_x <- data\$V2[ grepl("[^\\\\*]",data\$V3,perl=TRUE) ]
degs_y <- data\$V1[ grepl("[^\\\\*]",data\$V3,perl=TRUE) ]

no_degs_x <- 0.5 * log2(no_degs_x)
degs_x <- 0.5 * log2(degs_x)

xmin <- min(c(no_degs_x,degs_x)[grepl("\\\\d+",c(no_degs_x,degs_x),perl=TRUE)])
xmax <- max(c(no_degs_x,degs_x)[grepl("\\\\d+",c(no_degs_x,degs_x),perl=TRUE)])
ymin <- min(c(no_degs_y,degs_y)[grepl("\\\\d+",c(no_degs_y,degs_y),perl=TRUE)])
ymax <- max(c(no_degs_y,degs_y)[grepl("\\\\d+",c(no_degs_y,degs_y),perl=TRUE)])

plot(0,0,pch="",xlim=c(xmin,xmax),ylim=c(ymin,ymax),ylab="$Ylab",xlab="$Xlab",main="MA plot of $vs")
for (i in 1 : length(no_degs_x)) {
        points(no_degs_x[i], no_degs_y[i], col = "black", pch = ".", cex = 3)
}
for (j in 1 : length(degs_x)) {
        if (degs_y[j] > 0) {
                points(degs_x[j], degs_y[j], col = "red", pch = ".", cex = 3)
        }else {
                points(degs_x[j], degs_y[j], col = "blue", pch = ".", cex = 3)
        }
}
lines(c(xmin-1,xmax+1),c(0,0),col="black")
legend("topright",c("Up-Regulated Genes:$upnum","Down-Regulated Genes:$downnum", "non-DEGs:$nodeg"),col=c("red","blue","black"),pch=15,bty="n")
dev.off()
CMD
close LOG;
system("$Rscript $vs.MA.R 2>>run.log");
system("rm $vs.MA.R $vs.MA");
my $obj=Archive::Zip->new();
my $fff="out/$vs.MA-plot.pdf";
$obj->addFile($fff);
$obj->writeToFileNamed("out.zip");

sub gettype{
	my ($a,$l1,$l2)=@_;
	my @a=@$a;
	my $tt;
	if($l1-1>$#a or $l2-1 >$#a){
		print LOG "column out of range!\n";
		die;
	}
	if(abs($a[$l1-1])<$foldchange){
		$tt="*";
	}
	else{
		if($a[$l2-1]>$pvalue){
			$tt="*";
		}
		else{
			if($a[$l1-1]>0){
				$tt="Up";
			}
			else{
				$tt="Down";
			}
		}
	}
	return($tt);
}

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
		my $exp=0;
		for(my $i=$min;$i<=$max;$i++){
			if($a[$i]==0){
				$a[$i]=0.001;
			}
			$exp+=$a[$i];
		}
		$exp=sprintf("%.4f",$exp/$num);
		return($exp);
	}
	else{
		$column--;
		if($column>$#a){
			print LOG "exp column out of range!\n";
			die;
		}
		if($a[$column]==0){
			$a[$column]=0.001;
		}
		return($a[$column]);
	}
}

sub check_parameters{
	my ($log,$fpkm1,$fpkm2,$pv,$pC,$fvalue)=@_;
	if($log!~/^\d+$/){
		print LOG "fold change column error!\n";
		die;
	}
	if($pC!~/^\d+$/){
		print LOG "pvalue/fdr column error!\n";
		die;
	}
	$pv=~s/\.//;
	if($pv!~/^\d+$/){
		print LOG "pvalue error!\n";
		die;
	}
	$fvalue=~s/\.//;
	if($fvalue!~/^\d+$/){
		print LOG "$fvalue\nfold change value error!\n";
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
