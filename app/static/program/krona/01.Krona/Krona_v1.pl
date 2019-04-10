#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($input_file,$type,$outdir);
GetOptions(
 "i:s" =>\$input_file,
 "type:s" =>\$type,
 "outdir:s" =>\$outdir
);
if(!$input_file || !$outdir) {
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
	die;
}
system("mkdir -p $outdir/out");
if(!$type){
	$type="txt";
}
open LOG,">$outdir/run.log";
my $column_num=0;
my$time=0;
if($type eq "txt"){
	open IN,"$input_file" or die $!;
	while(<IN>){
		chomp;
		my@line=split/\t/,$_;
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
perl $Bin/ImportRDP.pl $input_file -o $outdir/out/krona.html -n root
EOF
	print OUT $cmd;
	close OUT;
}elsif($type eq "biom"){
	open OUT,">$outdir/krona.sh";
	my$cmd=<<EOF;
/usr/bin/biom convert -i $input_file -o $outdir/otu_table.txt --to-tsv --header-key taxonomy
sed -i '1d' $outdir/otu_table.txt
cat $outdir/otu_table.txt|sed 's/; /;/g'|sed 's/taxonomy/Taxonomy/' > $outdir/Krona.txt
perl $Bin/ImportRDP.pl $outdir/Krona.txt -o $outdir/out/krona.html -n root
EOF
	print OUT $cmd;
	close OUT;
}
system("sh $outdir/krona.sh");

my $obj=Archive::Zip->new();
my $fff="out/krona.html";
$obj->addFile($fff);
$obj->writeToFileNamed("out.zip");
#system("zip -r $outdir/out.zip out");
