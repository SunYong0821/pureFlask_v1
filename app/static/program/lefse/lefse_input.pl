#!/usr/bin/perl -w
use strict;
use Getopt::Long;
my($in,$map,$out,$type);
GetOptions(
 "i:s" =>\$in,#dos
 "map:s" =>\$map,
 "type:s" =>\$type,#tax or func or gene
 "o:s" =>\$out
);
if(!$out || !$in || !$map || !$type){
	print STDERR <<USAGE;
=============================================================================
Usage:
	*-type	
	 tax	#input OTU tax table,the last column:taxonomy
	 func	#input function table,the last column:function
	 gene	#input gene abundance table,the last column:not gene description
=============================================================================
USAGE
	exit;
}
open MAP,"$map" or die $!;
my %sample;
while(<MAP>){
	chomp;
	my @group=split/\t/,$_;
	$sample{$group[0]}=$group[-1];
}close MAP;
open IN,"$in" or die $!;
open OUT,">$out";
my$head=<IN>;
chomp($head);
my @head=split/\t/,$head;
if($type eq 'tax'){
	print OUT $head[-1];
	for(my $i=1;$i<=$#head-1;$i++){
		print OUT "\t".$sample{$head[$i]};
	}
	print OUT "\n";
}elsif($type eq 'func'){
	print OUT $head[0];
	for(my $i=1;$i<=$#head-1;$i++){
		print OUT "\t".$sample{$head[$i]};
	}
	print OUT "\n";
}elsif($type eq 'gene'){
	print OUT $head[0];
	for(my $i=1;$i<=$#head;$i++){
		print OUT "\t".$sample{$head[$i]};
	}
	print OUT "\n";
}
my %tax;my %hash;
while(<IN>){
	chomp;
	my @line=split/\t/,$_;
	if($type eq 'tax'){
		my @taxon=split/\; /,$line[-1];
		my @level=();
		for(my $i=0;$i<=$#taxon;$i++){
			#uncultivated
			if($taxon[$i] !~ /uncultured|Unknown|unidentified|metagenome|Ambiguous_taxa/){
				push(@level,$taxon[$i]);
				if(!exists $tax{join("\|",@level)}){
					for(my $j=1;$j<=$#head-1;$j++){
						$hash{join("\|",@level)}{$head[$j]}=$line[$j];
					}
				$tax{join("\|",@level)}=1;
				}else{
					for(my $j=1;$j<=$#head-1;$j++){
						$hash{join("\|",@level)}{$head[$j]}+=$line[$j];
					}
				}
			}else{
				last;
			}	
		}
	}elsif($type eq 'func'){
		print OUT $line[0];
		for(my $i=1;$i<=$#line-1;$i++){
			print OUT "\t".$line[$i];
		}
		print OUT "\n";
	}elsif($type eq 'gene'){
		print OUT $_."\n";
	}
}close IN;
if($type eq 'tax'){
	foreach my $key(sort{$a cmp $b}keys %tax){
		print OUT $key;
		for(my $i=1;$i<=$#head-1;$i++){
			print OUT "\t".$hash{$key}{$head[$i]};
		}
		print OUT "\n";
	}
}
close OUT;
