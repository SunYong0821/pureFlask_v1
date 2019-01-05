#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$count1Col,$count2Col,$vs,$geneCol,$name1,$name2);
our $Algorithm;
GetOptions (
	"i:s" => \$infile,
	"exp1col:s" => \$count1Col,
	"name1:s"   => \$name1,
	"exp2col:s" => \$count2Col,
	"name2:s"   => \$name2,
	"prefix:s"  => \$vs,
	"genecol:i" => \$geneCol,
	"method:s"    => \$Algorithm
);

if (!$infile  || !$count1Col || !$count2Col || !$vs || !$geneCol || !$Algorithm) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Differently Expression Analysis using edgeR software
Usage:
	perl $0 [options]
Options:
	* -i			input Diff Analysis Results
	* -exp1col		expression column(s) of sample1 or group1 in input Results(E.g:3 or 3-5)
	* -name1		sample name(s) of sample1 or group1 in input Results(E.g:A or A1,A2)
	* -exp2col		expression column(s) of sample2 or group2 in input Results(E.g:3 or 3-5)
	* -name2		sample name(s) of sample2 or group2 in input Results(E.g:B or B1,B2)
	* -genecol		Gene name column
	* -prefix		prefix for outfiles and the title in the images
	* -method		pearson or spearman
E.g.:
	With no Biological duplication sample
		perl $0 -i example_input.xls -exp1col 2 -name1 ZH1 -exp2col 7 -name2 PH3 -genecol 1 -prefix test -method pearson
	With Biological duplication sample
		perl $0 -i example_input.xls -exp1col 2-4 -name1 ZH1,ZH2,ZH3 -exp2col 5-7 -name2 PH1,PH2,PH3 -genecol 1 -prefix test -method pearson
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
my $mode=&check_parameters($count1Col,$count2Col,$geneCol,$name1,$name2);
our %exp;
if($mode eq "Single"){
	open IN,$infile;
	<IN>;
	chdir"$odir";
	open OUT,">$vs.matrix";
	print OUT "GeneID\tA\tB\n";
	my %checkgene;
	while(<IN>){
		chomp;
		my @a=split /\t/,$_;
		my $a=\@a;
		my (@exp1)=&getexp($a,$count1Col);
		my (@exp2)=&getexp($a,$count2Col);
		if($geneCol>$#a+1){
			print LOG "Gene column out of range!\n";
			die;
		}
		if($checkgene{$a[$geneCol-1]}){
			print LOG "$a[$geneCol-1]:\tthere are same genes in the Gene column!\n";
			die;
		}
		$checkgene{$a[$geneCol-1]}=1;
		my $exp1=join("\t",@exp1);
		my $exp2=join("\t",@exp2);
		print OUT "$a[$geneCol-1]\t$exp1\t$exp2\n";
	}
	close IN;
	close OUT;
	system("Rscript $Bin/single.R $vs.matrix out/$vs.correlation $name1 $name2 $Algorithm");
	my $obj=Archive::Zip->new();
	my $fff="out/$vs.correlation.pdf";
	$obj->addFile($fff);
	$obj->writeToFileNamed("out.zip");
}
else{
	my @samples;
	my @s1=split /,/,$name1;
	foreach(@s1){
		push @samples,$_;
	}
	my @s2=split /,/,$name2;
	foreach(@s2){
		push @samples,$_;
	}
	open IN,$infile;
	<IN>;
	chdir"$odir";
	my %checkgene;
	while(<IN>){
		chomp;
		my @a=split /\t/,$_;
		my $a=\@a;
		my (@exp1)=&getexp($a,$count1Col);
		my (@exp2)=&getexp($a,$count2Col);
		if($geneCol>$#a+1){
			print LOG "Gene column out of range!\n";
			die;
		}
		if($checkgene{$a[$geneCol-1]}){
			print LOG "$a[$geneCol-1]:\tthere are same genes in the Gene column!\n";
			die;
		}
		$checkgene{$a[$geneCol-1]}=1;
		for(my $i=0;$i<=$#exp1;$i++){
			$exp{$a[$geneCol-1]}{$s1[$i]}=$exp1[$i];
		}
		for(my $i=0;$i<=$#exp2;$i++){
			$exp{$a[$geneCol-1]}{$s2[$i]}=$exp2[$i];
		}
	}
	close IN;
	my %cor = ();
	my $min_value = 1;
	foreach my $i (0..$#samples){
		foreach my $j ($i..$#samples){
			my $cor;
			if ($j eq $i){
				$cor=1;
			}
			else{
				$cor = CalculateCorrelation($samples[$i],$samples[$j]);
			}
			$min_value = ($min_value > $cor) ? $cor : $min_value;
			$cor{$samples[$i]}{$samples[$j]} = $cor;
		}
	}
	open my $fh_stat,">","AllSamples.correlation.xls" or die $!;
	print $fh_stat join("\t",("Sample",@samples)),"\n";
	foreach my $k (@samples){
		my $outinfo = $k;
		foreach my $m (@samples){
			if (exists $cor{$k}{$m}){
				$outinfo .= "\t$cor{$k}{$m}";
			}
			else{
				$outinfo .= "\t$cor{$m}{$k}";
			}
		}
		print $fh_stat "$outinfo\n";
	}
	close $fh_stat;

	my $cellsize = 480 / @samples;
	my $fontsize = ($cellsize > 15) ? 15 : $cellsize;
	open my $fh_rcode,">","correlation-heatmap.R" or die $!;
print $fh_rcode <<CODE;
library("pheatmap")
data<-read.table("./AllSamples.correlation.xls",head=TRUE)
rownames(data)<-data[,1]
colnames(data)<-c("Sample",rownames(data))
len<-length(data)
data<-as.matrix(data[,2:len])
mycolors <- colorRampPalette(c("white","blue"))(1001)
pheatmap(data,show_rownames=TRUE,show_colnames=TRUE,col=mycolors,cluster_rows=FALSE,cluster_cols=FALSE,legend=TRUE,fontsize=$fontsize,main="Correlation between Samples(method=$Algorithm)",display_numbers=TRUE,number_format = "\%.2f",cellwidth = $cellsize,cellheight = $cellsize,breaks=seq($min_value,1,(1-$min_value)/1000),border_color="black",filename ="out/$vs.correlation.pdf")
CODE
	system("Rscript correlation-heatmap.R");
	my $obj=Archive::Zip->new();
        my $fff="out/$vs.correlation.pdf";
        $obj->addFile($fff);
        $obj->writeToFileNamed("out.zip");
}
close LOG;
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
###&check_parameters($foldchange,$conut1Col,$conut2Col,$geneCol);
	my ($fpkm1,$fpkm2,$pC,$n1,$n2)=@_;
	my $mode="Single";
	if($pC!~/^\d+$/){
		print LOG "Gene name column error!\n";
		die;
	}
	my @n1=split /,/,$n1;
	my $num1=1;
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
		$mode="Muti";
		my @tmp=split /-/,$fpkm1;
		$num1=abs($tmp[0]-$tmp[1])+1;
	}
	if($num1!=$#n1+1){
		print LOG "EXP1 column and sample number not match!\n";
		die;
	}
	my @n2=split /,/,$n2;
	my $num2=1;
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
		$mode="Muti";
		my @tmp=split /-/,$fpkm2;
		$num2=abs($tmp[0]-$tmp[1])+1;
        }
	if($num2!=$#n2+1){
		print LOG "EXP2 column and sample number not match!\n";
		die;
	}
	return($mode);
}

sub CalculateCorrelation {
        my ($sa,$sb) = @_;
        my ($exp_a,$exp_b);
        foreach my $g (keys %exp) {
                next if (!exists $exp{$g}{$sa} && !exists $exp{$g}{$sb});
                $exp_a .= ($exp{$g}{$sa}) ? "$exp{$g}{$sa}," : "0.001,";
                $exp_b .= ($exp{$g}{$sb}) ? "$exp{$g}{$sb}," : "0.001,";
        }
        chop $exp_a;
        chop $exp_b;
        open my $fh_rcode,">$sa-vs-$sb.correlation.R" or die $!;
        print $fh_rcode "x <- c($exp_a)\n y <- c($exp_b)\ncor(x, y, method = \"$Algorithm\")\n";
        close $fh_rcode;
        my ($index,$value) = split /\s+/, `$Rscript $sa-vs-$sb.correlation.R && rm $sa-vs-$sb.correlation.R`;
        chomp $value;
        return $value;
}
