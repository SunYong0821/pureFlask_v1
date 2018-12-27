#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$pathcol,$genecol,$backgroundcol,$pvaluecol,$prefix);
GetOptions (
	"i:s" => \$infile,
	"pathcol:i" => \$pathcol,
	"genecol:i" => \$genecol,
	"background:i"  => \$backgroundcol,
	"pcol:i"    => \$pvaluecol,
	"prefix:s"  => \$prefix
);

if (!$infile || !$pathcol || !$genecol || !$backgroundcol || !$pvaluecol || !$prefix) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Generate top 20 Pathway Enrichment Figure
Usage:
	perl $0 [options]
Options:
	* -i			input Enrich Analysis Results
	* -pathcol		pathway description columm in Enrich Analysis Results
	* -genecol		gene number column in Enrich Analysis Results
	* -background		background gene number column in Enrich Analysis Results
	* -pcol			pvalue/FDR column in Enrich Analysis Results
	* -prefix		prefix for outfiles and the title in the images
E.g.:
		perl $0 -i infile pathcol 3 -genecol 5 -background 6 -pcol 8 -prefix AA
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
&check_parameters($pathcol,$genecol,$backgroundcol,$pvaluecol);

open IN,$infile;
<IN>;
chdir"$odir";
open OUT,">$prefix.matrix";
print OUT "Pathway\tGene_number\tBackgroud_gene_number\tRichFactor\tQvalue\n";
my $id=0;
my %checkpath;
while(<IN>){
	chomp;
	my @a=split /\t/,$_;
	$id++;
	if($pathcol>$#a+1){
		print LOG "Pathway column out of range!\n";
		die;
	}
	if($genecol>$#a+1){
		print LOG "Gene column out of range!\n";
		die;
	}
	if($backgroundcol>$#a+1){
		print LOG "Background gene column out of range!\n";
		die;
	}
	if($pvaluecol>$#a+1){
		print LOG "Pvalue/FDR column out of range!\n";
		die;
	}
	my $genenum=$a[$genecol-1];
	if($genenum!~/^\d+$/){
		print LOG "Gene column with no numberic value!\n";
		die;
	}
	my $backnum=$a[$backgroundcol-1];
	if($backnum!~/^\d+$/){
		print LOG "background Gene column with no numberic value!\n";
		die;
	}
	my $pathway=$a[$pathcol-1];
	if($checkpath{$pathway}){
		print LOG "$pathway ----Pathway error! duplicate names!\n";
		die;
	}
	$checkpath{$pathway}=1;
	my $pvalue=$a[$pvaluecol-1];
	my $richfactor=sprintf("%.4f",$genenum/$backnum);
	print OUT "$pathway\t$genenum\t$backnum\t$richfactor\t$pvalue\n";
	if($id>19){
		last;
	}
}

close IN;
close OUT;

open RS,">$prefix.R";
print RS <<QT;
library(ggplot2);
options(bitmapType='cairo')
x <- read.table("$prefix.matrix", head = T, sep = "\t")
pdf(file="out/$prefix.enrichment.pdf",width=10,height=10)
p <- ggplot(x,aes(x=-log10(Qvalue),y=reorder(Pathway,Qvalue)))
p + geom_point(aes(size=Gene_number, colour=RichFactor))+theme(axis.text=element_text(color='black'),panel.background = element_rect(fill='transparent'),panel.grid=element_line(color='grey'),panel.border=element_rect(fill='transparent',color='black'),axis.title=element_text(size=15))+ylab("Pathway")+scale_color_gradient(low="springgreen",high="#E41A1C")
dev.off()
QT
close RS;
system("$Rscript $prefix.R");
close LOG;
my $obj=Archive::Zip->new();
my $fff="out/$prefix.enrichment.pdf";
$obj->addFile($fff);
$obj->writeToFileNamed("out.zip");


sub check_parameters{
	##&check_parameters($pathcol,$genecol,$backgroundcol,$pvaluecol);
	my ($c1,$c2,$c3,$c4)=@_;
	if($c1!~/^\d+$/){
		print LOG "pathway description column error!\n";
		die;
	}
	if($c4!~/^\d+$/){
		print LOG "pvalue/fdr column error!\n";
		die;
	}
        if($c2!~/^\d+$/){
                print LOG "gene column error!\n";
                die;
        }
        if($c3!~/^\d+$/){
                print LOG "background gene column error!\n";
                die;
        }
	return(1);
}
