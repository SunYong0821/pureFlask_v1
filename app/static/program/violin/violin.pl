#!usr/bin/perl -w
#
use strict;
use Getopt::Long;
use File::Basename;
use FindBin qw($Bin $Script);
use Cwd qw(abs_path);
use Archive::Zip;

my ($in,$type_col,$data_col,$out);
GetOptions(
	"in:s" => \$in,
	"tcol:s" => \$type_col,
	"dcol:s" => \$data_col,
	"out:s" => \$out,
	"h|help:s" => \&USAGE
) or &USAGE;

&USAGE unless ($in and $type_col and $data_col and $out);

sub USAGE {
        my $usage = "
usage:
        perl $Script -in -tcol -dcol -out

        h               help
	in	<file>	input file
        tcol	<int>	type col
        dcol    <int>	data col
        out     <str>	output file name
";
print $usage;
exit;
}

$in = abs_path($in);
my $filedir = dirname($in);
my $outdir = "$filedir/out";
mkdir $outdir if(! -d $outdir);

chdir $filedir;

`Rscript $Bin/violin.R $in $type_col $data_col $out`;

my $obj=Archive::Zip->new();
$obj->addFile("out/$out.pdf");
$obj->writeToFileNamed("out.zip") 
