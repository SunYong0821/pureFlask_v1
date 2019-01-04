#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin '$Bin';
use lib ("$Bin/perl5");
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use Archive::Zip;
my ($infile,$best,$prefix);
our ($stopflag,$nflag);
our($ffff,$rrrr);
GetOptions (
	"i:s" => \$infile,
	"best!" => \$best,
	"stop!" => \$stopflag,
	"n!"	=> \$nflag,
	"for!"  => \$ffff,
	"rev!"  => \$rrrr,
	"prefix:s"  => \$prefix
);

if (!$infile || !$prefix) {
	print STDERR <<USAGE;
=============================================================================
Descriptions: Trans CDS sequence to protein sequence
Usage:
	perl $0 [options]
Options:
	* -i			input fasta file
	* -best			whether to chose the longest as the best output result
	* -stop			whether to stop when termination codon occurs
	* -n			whethe ignore N bases. if set, stop when codon with "N" base, else codon with "N" base will translate as "-"
	* -for			only keep forward results
	* -rev			only keep reverse results
	* -prefix		prefix for outfiles and the title in the images
E.g.:
		perl $0 -i infile -best -prefix aaa
=============================================================================
USAGE
	die;
}
$infile=abs_path($infile);
my $odir=dirname($infile);
open LOG,">$odir/run.log";
my $check="$odir/out";
unless(-d $check){
	mkdir($check);
}

our %codon = (TTT=>"F", TTC=>"F", TCT=>"S", TCC=>"S", TAT=>"Y", TAC=>"Y", TGT=>"C", TGC=>"C", TTA=>"L", TCA=>"S", TAA=>"*", TGA=>"*", TTG=>"L", TCG=>"S", TAG=>"*", TGG=>"W", CTT=>"L", CTC=>"L", CCT=>"P", CCC=>"P", CAT=>"H", CAC=>"H", CGT=>"R", CGC=>"R", CTA=>"L", CTG=>"L", CCA=>"P", CCG=>"P", CAA=>"Q", CAG=>"Q", CGA=>"R", CGG=>"R", ATT=>"I", ATC=>"I", ACT=>"T", ACC=>"T", AAT=>"N", AAC=>"N", AGT=>"S", AGC=>"S", ATA=>"I", ACA=>"T", AAA=>"K", AGA=>"R", ATG=>"M", ACG=>"T", AAG=>"K", AGG=>"R", GTT=>"V", GTC=>"V", GCT=>"A", GCC=>"A", GAT=>"D", GAC=>"D", GGT=>"G", GGC=>"G", GTA=>"V", GTG=>"V", GCA=>"A", GCG=>"A", GAA=>"E", GAG=>"E", GGA=>"G", GGG=>"G");

open IN,$infile;
chdir($odir);
open OUT,">out/$prefix.pep.fa";
while(<IN>){
	chomp;
	my $id=(split)[0];
	$/=">";
	my $seq=<IN>;
	$/="\n";
	$id=~s/>//g;
	$seq=~s/>//g;
	$seq=~s/\s+//g;
	$seq=uc($seq);
	my $former1=$seq;
	my $former2=substr($seq,1,length($seq)-1);
	my $former3=substr($seq,2,length($seq)-2);
	my $cmpseq=&revcmp($seq);
	my $revseq1=$cmpseq;
	my $revseq2=substr($cmpseq,1,length($cmpseq)-1);
	my $revseq3=substr($cmpseq,2,length($cmpseq)-2);
	my @peplen;
	my $forpep1=&cds2pep($former1);
	unless($rrrr){push @peplen,length($forpep1);}
	my $forpep2=&cds2pep($former2);
	unless($rrrr){push @peplen,length($forpep2);}
	my $forpep3=&cds2pep($former3);
        unless($rrrr){push @peplen,length($forpep3);}

	my $revpep1=&cds2pep($revseq1);
	unless($ffff){push @peplen,length($revpep1);}
	my $revpep2=&cds2pep($revseq2);
        unless($ffff){push @peplen,length($revpep2);}
	my $revpep3=&cds2pep($revseq3);
        unless($ffff){push @peplen,length($revpep3);}
	
	my $peplen=\@peplen;
	my $max=&maxlen($peplen);
	if($best){
		if(length($forpep1)==$max){
			unless($rrrr){print OUT ">$id\_former1\n$forpep1\n";}
		}
		if(length($forpep2)==$max){
                        unless($rrrr){print OUT ">$id\_former2\n$forpep2\n";}
                }
		if(length($forpep3)==$max){
                        unless($rrrr){print OUT ">$id\_former3\n$forpep3\n";}
                }
		if(length($revpep1)==$max){
                        unless($ffff){print OUT ">$id\_reverse1\n$revpep1\n";}
                }
		if(length($revpep2)==$max){
                        unless($ffff){print OUT ">$id\_reverse2\n$revpep2\n";}
                }
		if(length($revpep3)==$max){
                        unless($ffff){print OUT ">$id\_reverse3\n$revpep3\n";}
                }
	}
	else{
		unless($rrrr){print OUT ">$id\_former1\n$forpep1\n";}
		unless($rrrr){print OUT ">$id\_former2\n$forpep2\n";}
		unless($rrrr){print OUT ">$id\_former3\n$forpep3\n";}
		unless($ffff){print OUT ">$id\_reverse1\n$revpep1\n";}
		unless($ffff){print OUT ">$id\_reverse2\n$revpep2\n";}
		unless($ffff){print OUT ">$id\_reverse3\n$revpep3\n";}
	}
}
close IN;
close OUT;
close LOG;

my $obj=Archive::Zip->new();
my $fff="out/$prefix.pep.fa";
$obj->addFile($fff);
$obj->writeToFileNamed("out.zip");

sub revcmp{
	my ($seq)=@_;
	$seq=reverse($seq);
	$seq=~tr/[ATCG]/[TAGC]/;
	return($seq);
}

sub maxlen{
        my ($nnn)=@_;
	my @num=@$nnn;
        my $max;
        foreach(@num){
                if($max){
                        if($_>$max){
                                $max=$_;
                        }
                }
                else{
                        $max=$_;
                }
        }
        return($max);
}

sub cds2pep{
        my ($seq)=@_;
        my $len=length($seq);
        my $a=int($len/3);
        #$seq=uc($seq);
        my @base=split //,$seq;
        my @p;
        for(my $i=0;$i<$a*3;$i+=3){
                my $code="$base[$i]"."$base[$i+1]"."$base[$i+2]";
		my $p;
		if($code=~/N/i){
			$p="-";
		}
                else{
			unless($codon{$code}){
				print LOG "$code:unexpected bases in cds sequences,please check!\n";
				die;
			}
			$p=$codon{$code};

		}
		if($nflag && $p eq "-"){
			last;
		}
                push @p,$p;
                if($stopflag && $p eq "*"){
                        last;
                }
        }
        my $protein=join("",@p);
        return($protein);
}
