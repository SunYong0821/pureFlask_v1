#!perl
use warnings;
use strict;
use SVG;
use File::Basename qw(basename dirname);
use Cwd qw(abs_path);
use Archive::Zip;

die "perl $0 <a.fai,b.fai> <alabel,blabel> <collinearity(6 column)>  <outprefix> <touming>\n" if @ARGV != 5;
my ($alabel, $blabel) = split /,/, $ARGV[1];

my $infile=abs_path($ARGV[2]);
my $filedir=dirname($infile);
my $outdir = "$filedir/out";

my (%achr, %bchr, $sumlen, $asum, $bsum);
my @COL = ("#FF9900","#0099CC", "#CC9999","#99CC00");

my @fai = split /,/, $ARGV[0];
my $ab = 0;
foreach(@fai)
{
	open FAI, $_ or die $!;
	while(my $l = <FAI>)
	{
		chomp($l);
		my @tmp = split /\t/, $l;
		if($ab == 0)
		{
			$asum += $tmp[1];
			$achr{$tmp[0]} = $tmp[1];
		}else{
			$bsum += $tmp[1];
			$bchr{$tmp[0]} = $tmp[1];
		}
	}
	$ab ++;
}
if($asum >= $bsum)
{
	$sumlen = $asum;
}else{
	$sumlen = $bsum;
}

my (%hash);
open CL, $ARGV[2] or die $!;
while(<CL>)
{
	chomp;
	my @aaa = split;
	$aaa[1] = $aaa[1] * 1000 / $sumlen;
	$aaa[2] = $aaa[2] * 1000 / $sumlen;
	$aaa[4] = $aaa[4] * 1000 / $sumlen;
	$aaa[5] = $aaa[5] * 1000 / $sumlen;
	push @{$hash{$aaa[0]}{$aaa[3]}}, "$aaa[1]\t$aaa[2]\t$aaa[4]\t$aaa[5]";
}

my $W = 1200;
my $H = 600;
my $svg = SVG->new(width=>$W, height=>$H);

$svg->text(x => 119, y => 160, "font-family"=>"Arial", "font-size"=> "18", "text-anchor"=>"end", "-cdata" => "$alabel", fill=>"black");
$svg->text(x => 119, y => 450, "font-family"=>"Arial", "font-size"=> "18", "text-anchor"=>"end", "-cdata" => "$blabel", fill=>"black");

my $inix = 120;
my $n = 1;
my $last = 0;
my %fir;
foreach(sort {if($a =~ /^\d+$/ && $b =~ /^\d+$/){$a <=> $b}else{$a cmp $b}} keys %achr)
{
	my $l = $achr{$_} * 1000 / $sumlen;
	my $textx = $l / 2 + $last + 120;
	$svg->text(x => $textx, y => 145, "font-family"=>"Arial", "text-anchor"=>"middle","font-size"=> "12", "-cdata" => "$_", fill=>"black");
	$last += $l;
	foreach my $i(keys %{$hash{$_}})
	{
		for(my $j = 0; $j < @{$hash{$_}{$i}}; $j ++)
		{
			my ($s, $e, $at, $bt) = split /\t/, $hash{$_}{$i}[$j];
			my $sl = $s + $inix;
			my $el = $e + $inix;
			$fir{$i}{$_}[$j] =  "$sl\t$el\t$at\t$bt";
		 }
	}
	my $c = $n % 2 == 1 ? 1 : 0;
	$svg->rect(x => $inix, y => 150, width => $l, height => 10,fill => "$COL[$c]", "stroke-width"=>0);
	$inix = $l + $inix;
	$n ++;
}

$n = 1;
$inix = 120;
$last = 0;
my @loci;
foreach(sort {if($a =~ /^\d+$/ && $b =~ /^\d+$/){$a <=> $b}else{$a cmp $b}} keys %bchr)
{
	my $l = $bchr{$_} * 1000 / $sumlen;
	my $textx = $l / 2 + $last + 120;
	$svg->text(x => $textx, y => 465, "font-family"=>"Arial", "text-anchor"=>"middle","font-size"=> "12", "-cdata" => "$_", fill=>"black");
	$last += $l;
	foreach my $i(keys %{$fir{$_}})
	{
		for(my $j = 0; $j < @{$fir{$_}{$i}}; $j ++)
		{
			my ($at, $bt, $s, $e) = split /\t/, $fir{$_}{$i}[$j];
			my $sl = $s + $inix;
			my $el = $e + $inix;
			push @loci, "$at\t$bt\t$sl\t$el";
		}
	}
	my $c = $n % 2 == 1 ? 2 : 3;
	$svg->rect(x => $inix, y => 440, width => $l, height => 10,fill => "$COL[$c]", "stroke-width"=>0);
	$inix = $l + $inix;
	$n ++;
}

for(my $i = 0; $i < @loci; $i ++)
{
	my ($x1, $x2, $x3, $x4) = split /\t/, $loci[$i];
	my $x = [$x1, $x2, $x4, $x3];
	my $y = [160, 160, 440, 440];
	my $p = $svg->get_path(x => $x, y => $y, -type =>'polygon');
	my $pl = $svg->polygon(%$p, fill => "#000000", "stroke-width"=>0, "opacity" => $ARGV[4]);
}

my $out = $svg->xmlify;
open OUT,">$outdir/$ARGV[3]\.svg";
print OUT $out;
close OUT;

system("convert -density 200 $outdir/$ARGV[3]\.svg $outdir/$ARGV[3]\.png");

chdir($outdir);
my $obj=Archive::Zip->new();
my $f1="out/$ARGV[3]\.svg";
$obj->addFile($f1);
my $f2="out/$ARGV[3]\.png";
$obj->addFile($f2);
$obj->writeToFileNamed("$out.zip");