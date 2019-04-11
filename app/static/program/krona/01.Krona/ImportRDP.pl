#! /usr/bin/perl

# Copyright © 2011, Battelle National Biodefense Institute (BNBI);
# all rights reserved. Authored by: Brian Ondov, Nicholas Bergman, and
# Adam Phillippy
#
# See the LICENSE.txt file included with this software for license information.


use strict;
#use lib "/WORK/MICRO/chenjunru/software/KronaTools-2.4/lib";
use FindBin qw($Bin);
use lib $Bin;

use lib (`ktGetLibPath`);
use KronaTools;

setOption('name', 'root');
setOption('out', 'rdp.krona.html');

my @options =
qw(
	out
	name
	combine
	minConfidence
	depth
	hueBad
	hueGood
	local
	url
	postUrl
);

getKronaOptions(@options);

if(	@ARGV < 1){
    print "**********************************************************************************************************\n
    Description: ImportRDP.pl modify script
    NewUsage: perl $0 <otu_table.txt> [rdp_details] [sel_OTUsID.list] [--options]
    Note: The old usage was failure, but the options are effective\n\n",
    "****************************************************************************************************************\n\n";
	printUsage
	(
		'Creates a Krona chart from RDP classifications.',
		'rdp_details',
		'RDP assignment details downloaded as text from the RDP Classifier web
portal or output by the command line RDP Classifier or Multiclassifier.',
		0,
		1,
		\@options
	);
	exit 0;
}
for(@ARGV){(-s $_) || die$!;}
my ($otu_table, $rdp_detail,$otu_selist) = @ARGV;
my (%otu_selh,%otu_taxh);
($otu_selist && -s $otu_selist) && (%otu_selh = split/\s+/,`awk '{print \$1,1}' $otu_selist`);
my @Ranks = qw(domain phylum class order family genus);
my @Score = (1.00) x @Ranks;
greengene_tax($rdp_detail,\%otu_taxh,%otu_selh ? \%otu_selh : 0,\@Ranks) ||
rdp_tax($rdp_detail,\%otu_taxh,%otu_selh ? \%otu_selh : 0);
my $tree = newTree();
my @datasetNames;
open IN,$otu_table || die$!;
while(<IN>){
    chomp;
    my @l = split/\t/;
    my $queryID = shift @l;
    if(!@datasetNames){
        ($l[-1] eq "Taxonomy") && (pop @l);
        @datasetNames = @l;
    }elsif(/^#/){
        next;
    }
    %otu_selh && !$otu_selh{$queryID} && next;
    my (@lineage,@ranks,@scores);
    if($otu_taxh{$queryID}){
        @lineage = @{$otu_taxh{$queryID}->[0]};
        @ranks = @{$otu_taxh{$queryID}->[1]};
        @scores = @{$otu_taxh{$queryID}->[2]};
    }else{
        get_str_tax($l[-1],\@Ranks,\@lineage);
        @ranks = @Ranks;
        @scores = @Score;
    }
    for my $set (0 .. $#datasetNames){
#		addByLineage($tree, $set, \@lineage, $queryID, $l[$set], \@scores, \@ranks);
		$l[$set] && addByLineage($tree, $set, \@lineage, undef, $l[$set], \@scores, \@ranks);
	}
}
close IN;

my @attributeNames = ('count', 'unassigned', 'score', 'rank');

my @attributeDisplayNames = ('Count', 'Unassigned', 'Avg. % Confidence', 'Rank');

writeTree
(
	$tree,
	\@attributeNames,
	\@attributeDisplayNames,
	\@datasetNames,
	getOption('hueBad'),
	getOption('hueGood')
);
#*********************************************************************************************
#SUB
#*********************************************************************************************
sub greengene_tax{
    my ($tax_txt,$ref_taxh,$ref_sel,$Ranks) = @_;
    ($tax_txt && -s $tax_txt) || return(0);
    chomp(my $frank = `awk '{print NF;exit;}' $tax_txt`);
    ($frank == 3 || $frank==4) || return(0);
    open TAX,$tax_txt || die$!;
    while(<TAX>){
        /\S/ || next;
        chomp;
        my ($queryID,$str,$score) = split /\t/;
        ($frank==4) && ($score = 1.00);
        $ref_sel && !$ref_sel->{$queryID} && next;
        my @lineage;
        get_str_tax($str,$Ranks,\@lineage);
        my @scores = ($score) x @lineage;
        $ref_taxh->{$queryID} = [[@lineage], $Ranks, [@scores]];
    }
    close TAX;
    1;
}
sub get_str_tax{
    my ($str,$Ranks,$lineage) = @_;
    my @ranks = split /;/,$str;
    for my $i(0..$#$Ranks){
        if($ranks[$i] && $ranks[$i] =~ /^\w\__(.+)/){
            my $tax = $1;
            $tax =~ s/^\[|\]$//g;
            push @$lineage, $tax;
        }else{            
            push @$lineage, "Unclassified";
        }
    }
}

sub rdp_tax{
    my ($tax_txt,$ref_taxh,$ref_sel) = @_;
    ($tax_txt && -s $tax_txt) || return(0);
    open TAX,$tax_txt || die$!;
    while(<TAX>){
        /\S/ || next;
        chomp;
		my @fields = split /"?\t"?/;
		my $queryID = $fields[0];
        $ref_sel && !$ref_sel->{$queryID} && next;    
        my (@lineage, @ranks, @scores);
        my $aa = 0;
		for ( my $i = 2; $i < @fields; $i += 3 ){ 
		    if ( $fields[$i] eq 'Root' || $fields[$i+1]=~/^sub/){
                if($fields[$i+1]=~/^sub/){
                    $lineage[-1] .= "/".$fields[$i];
                    $scores[-1] = $fields[$i + 2] * 100;
                    $aa = 1;
                }
			    next;
		    }
#            if($fields[$i] eq 'Root'){next;}		    
		    push @lineage, $fields[$i];
		    push @ranks, $fields[$i + 1];
		    push @scores, $fields[$i + 2] * 100;
            $ref_taxh->{$queryID} = [[@lineage], [@ranks], [@scores]];
		}
	}
    close TAX;
    1;
}
