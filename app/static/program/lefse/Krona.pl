#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
my ($input_file,$type,$outdir);
GetOptions(
 "i:s" =>\$input_file,
 "t:s" =>\$type,
 "outdir:s" =>\$outdir
);
if(!$input_file) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Krona analysis
Usage:
	perl $0 [options]
Options:
	* -i		otu_table
	* -type		txt or biom
	* -outdir	output dir
E.G.:
	perl $0 -i otu_table.biom -type biom -outdir /path/to/output
=============================================================================
USAGE
}
if(defined $type){
	$type="txt";
}
open LOG,">$outdir/run.log";
system("mkdir -p $outdir");
my $column_num=0;
my$time=0;
if($type eq "txt"){
	open IN,"$input_file" or die $!;
	while(<IN>){
		chomp;
		$time++;
		if($column_num == 0){
			$column_num=$#line;
		}
		if($#line ne $column_num){
			my $column_real_num=$column_num+1;
			print LOG "Line $time is not $column_real_num columns\n";
			die;
		}
	}close IN;
	open OUT,">$outdir/krona.sh";
	my$cmd=<<EOF;
perl $Bin/ImportRDP.pl $input_file -o $outdir/krona.html -n root
EOF
	print OUT $cmd;
	close OUT;
}elsif($type eq "biom"){
	open OUT,">$outdir/krona.sh";
	my$cmd=<<EOF;
source $Bin/otu.env
biom convert -i $input_file -o $outdir/otu_table.txt --to-tsv --header-key taxonomy
sed -i '1d' $outdir/otu_table.txt
cat $outdir/otu_table.txt|sed 's/; /;/g'|sed 's/taxonomy/Taxonomy/' > $outdir/Krona.txt
perl $Bin/ImportRDP.pl $outdir/Krona.txt -o $outdir/krona.html -n root
EOF
	print OUT $cmd;
	close OUT;
}
