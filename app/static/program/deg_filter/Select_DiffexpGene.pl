#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$fc,$fccolumn,$pvalue,$pcolumn,$fdr,$fcolumn,$head,$split,$prefix);
GetOptions (
	"i:s" => \$infile,
	"fc:f" => \$fc,
	"fccolumn:i" =>\$fccolumn,
	"pvalue:f"	=>\$pvalue,
	"pcolumn:i"	=>\$pcolumn,
	"fdr:f"	=>\$fdr,
	"fdrcolumn:i" =>\$fcolumn,
	"head!"   =>\$head,
	"split!"	  =>\$split,
	"prefix:s"	=>\$prefix
);

if (!$infile || !$fc || !$fccolumn || !$prefix) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Select Diff Analysis Results
Usage:
	perl $0 [options]
Options:
	* -i			input Diff Analysis Results
	* -fc			log2 fold change used for select Diff Analysis Results
	* -fccolumn		fold change column in input Diff Analysis Results
	  -pvalue		pvalue used for select Diff Analysis Results
	  -pcolumn		pvalue column in input Diff Analysis Results
	  -fdr			FDR used for select Diff Analysis Results
	  -fdrcolumn		FDR column in input Diff Analysis Results
	  -head			only active when files with header
	  -split		split up(fc>0) and down(fc <0) to corresponding files
	* -prefix		prefix for outfiles,E.g:A-vs-B, the result file is A-vs-B.Diffexp.xls
E.g.:
	Use FDR && FC to select results:
		perl $0 -i infile -fc 1 -fccolumn 9 -fdr 0.05 -fdrcolumn 11 -head -split -prefix test
	Use Pvalue && FC to select results:
		perl $0 -i infile -fc 1 -fccolumn 9 -pvalue 0.05 -fdrcolumn 10 -head -split -prefix A-vs-B
Attention:
	if Both Pvalue and FDR are used to select Diff Analysis Results, We will only use FDR to select Diff Analysis Results!
=============================================================================
USAGE
	die;
}
$infile=abs_path($infile);
my $odir=dirname($infile);
$fc=abs($fc);
&checknum($fc);
##my ($infile,$fc,$fccolumn,$pvalue,$pcolumn,$fdr,$fcolumn,$head,$split,$prefix);
&checknum($fccolumn);
open IN,$infile;
my $check="$odir/out";
unless(-d $check){
	mkdir($check);
}
open OUT,">$odir/out/$prefix.Diffexp.xls";
open LOG,">$odir/run2.log";
my @files;
#push @files,"out/run.log";
push @files,"out/$prefix.Diffexp.xls";
if(defined $split){
	open UP,">$odir/out/$prefix.Diffexp_up.xls";
	open Down,">$odir/out/$prefix.Diffexp_down.xls";
	push @files,"out/$prefix.Diffexp_up.xls";
	push @files,"out/$prefix.Diffexp_down.xls";
}
if (defined $head){
	my $header=<IN>;
	chomp($header);
	print OUT "$header\n";
	if(defined $split){
		print UP "$header\n";
		print Down "$header\n";
	}
}

while(<IN>){
	chomp;
	my $l=$_;
	my @a=split /\t/,$_;
	if($fccolumn>$#a+1){
		print LOG "Fold change column out of range!\n";
		die;
	}
####my ($infile,$fc,$fccolumn,$pvalue,$pcolumn,$fdr,$fcolumn,$head,$split,$prefix);
	&checknum($a[$fccolumn-1]);
	if($a[$fccolumn-1]!~/\d+/){
		print LOG "Fold change column error:\n$l\n";
		die;
	}
	if(abs($a[$fccolumn-1])<$fc){
		next;
	}
	if($fdr){
		&checknum($fcolumn);
		if($fcolumn>$#a+1){
			print LOG "FDR column out of range!\n";
			die;
		}
		if($a[$fcolumn-1]!~/\d+/){
			print LOG "FDR column error:\n$l\n";
			die;
		}
		if($a[$fcolumn-1]<=$fdr){
			print OUT "$l\n";
			if(defined $split){
				if($a[$fccolumn-1]>0){print UP "$l\n";}
				else{print Down "$l\n";}
			}
		}
	}
	elsif($pvalue){
		&checknum($pcolumn);
		if($pcolumn>$#a+1){
			print LOG "Pvalue column out of range!\n";
			die;
		}
		if($a[$pcolumn-1]!~/\d+/){
			print LOG "Pvalue column error:\n$l\n";
			die;
		}
		if($a[$pcolumn-1]<=$pvalue){
			print OUT "$l\n";
			if(defined $split){
				if($a[$fccolumn-1]>0){print UP "$l\n";}
				else{print Down "$l\n";}
			}
		}
	}
}
close IN;
close UP;
close Down;
close OUT;
close LOG;
my $obj=Archive::Zip->new();
chdir"$odir";
foreach(@files){
	my $file=$_;
	$obj->addFile($file);
}
$obj->writeToFileNamed("out.zip");

sub checknum{
	my ($num)=@_;
	$num=~s/\.//g;
	$num=~s/-//g;$num=~s/e//i;
	if($num=~/^\d+$/){
		return(1);
	}
	else{
		die;
	}
}
