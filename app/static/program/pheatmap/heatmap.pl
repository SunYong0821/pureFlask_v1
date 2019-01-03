#!/usr/bin/env perl
use warnings;
use strict;
use Getopt::Long;
use File::Basename;
use FindBin '$Bin';
use Cwd qw(abs_path);
use Archive::Zip;


my ($in,$scale,$cluster_rows,$cluster_cols, $show_rownames, $show_colnames, $display_numbers, $width, $height, $outpre, $namecol, $datacol);
GetOptions(
	"in=s"=>\$in,
    "namecol=s"=>\$namecol,
    "datacol=s"=>\$datacol,
	"scale=s"=>\$scale,
    "cluster_rows=s"=>\$cluster_rows,
    "cluster_cols=s"=>\$cluster_cols,
    "show_rownames=s"=>\$show_rownames,
    "show_colnames=s"=>\$show_colnames,
    "display_numbers=s"=>\$display_numbers,
    "width=s"=>\$width,
    "height=s"=>\$height,
    "prefix=s"=>\$outpre,
);

if (!$in) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Generate cluster tree using R cluster package
Usage:
	perl $0 [options]
Options:
	* -i			input Diff Analysis Results
E.g.:
		perl $0 -in example.xls
=============================================================================
USAGE
	die;
}

my $infile=abs_path($in);
my $filedir=dirname($infile);
my $outdir = "$filedir/out";

my @group = split /,/, $datacol;
my @cols;
foreach(@group)
{
    if($_ =~ /-/)
    {
        my ($s, $e) = split /-/, $_;
        foreach my $i($s..$e)
        {
            push @cols, $i - 1;
        }
    }else{
        push @cols, $_ - 1;
    }
}

open FA, $infile;
chdir $filedir;
open OUT, "> format.txt";
my $head = <FA>;
chomp($head);
my @line = split /\t/, $head;
my $oh = $line[$namecol - 1];
foreach my $i(@cols)
{
    $oh .= "\t$line[$i]";
}
print OUT "$oh\n";
while(<FA>)
{
    chomp;
    my @tmp = split;
    my $os = $tmp[$namecol - 1];
    my $zero = 0;
    foreach my $i(@cols)
    {
        $os .= "\t$tmp[$i]";
        $zero += $tmp[$i];
    }
    if($zero == 0)
    {
        next;
    }
    print OUT $os."\n";
}

my $inlast = "format.txt";

system("Rscript $Bin/heatmap.r $scale $cluster_rows $cluster_cols $show_rownames $show_colnames $display_numbers $width $height $outpre.pdf $inlast");

my $obj=Archive::Zip->new();
$obj->addFile("out/$outpre.pdf");
$obj->writeToFileNamed("out.zip");