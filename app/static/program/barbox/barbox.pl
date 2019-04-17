#!usr/bin/perl -w
#
use strict;
use Getopt::Long;
use File::Basename;
use FindBin qw($Bin $Script);
use Cwd qw(abs_path);
use Archive::Zip;

my ($in,$dcol,$log,$group,$title,$xlab,$ylab,$out);
GetOptions(
	"in:s" => \$in,
	"dcol:s" => \$dcol,
	"log:s" => \$log,
	"group:s" => \$group,
	"title:s" => \$title,
	"xlab:s" => \$xlab,
	"ylab:s" => \$ylab,
	"out:s" => \$out,
	"h|help:s" => \&USAGE
) or &USAGE;

&USAGE unless ($in and $dcol and $out);

sub USAGE {
        my $usage = "
usage:
        perl $Script -in -dcol -out

        h               help
	in	<file>	input file
        dcol    <str>	data col or all
	log	<logical> 0 or 1
	group	<file>	group file
	title	<str>	image title
	xlab	<str>	xlab title
	ylab	<str>	ylab title
        out     <str>	output file name
";
print $usage;
exit;
}

##获取输入输出路径
$in = abs_path($in);
my $filedir = dirname($in);
$group = abs_path($group) if($group);
my $outdir = "$filedir/out";
mkdir $outdir if(! -d $outdir);

##设置默认参数
$log ||= 0;
$title ||= "Distribution of Gene Expression Values";
$xlab ||= "Samples";
$ylab ||= "Gene Expression";

##进入工作目录
chdir $filedir;

my $measure_str="";
if($dcol ne "all"){
	my @cols = split /,/,$dcol;
	$measure_str = "measure = c(";
	foreach my $col (@cols){
		$measure_str .= "\"$col\"";
	}
	$measure_str .= "),";
}

open OUT, ">$out.barbox.R";
print OUT "library(ggplot2)\n";
print OUT "library(reshape2)\n";
print OUT "data <- read.table(\"$in\",header=TRUE,sep=\"\\t\")\n";
print OUT "data.melt <- melt(data,$measure_str variable.name = \"melt_sample\", value.name = \"melt_value\")\n";
my $fill_str;
if($group){
	print OUT "group <- read.table(\"$group\",header=TRUE,sep=\"\\t\")\n";
	print OUT "names(group) <- c(\"group\",\"melt_sample\")\n";
	print OUT "data_merge <- merge(data.melt,group,by=\"melt_sample\",all.x=TRUE)\n";
	$fill_str = "fill=group";
}else{
	print OUT "data_merge <- data.melt\n";
	$fill_str = "fill=melt_sample";
}
print OUT "pdf(paste(\"out/\",\"$out.pdf\",sep=\"\"),height=6,width=10)\n";
my $ystr;
if($log){$ystr="log(data_merge\$melt_value)";} else {$ystr="melt_value";}
print OUT "p <- ggplot(data=data_merge,aes(x=melt_sample,y=$ystr,$fill_str),alpha=0.5) +\n";
print OUT "geom_boxplot() +\n";
print OUT "theme(axis.line = element_line(size=0.5,color=\"black\")) +\n";
print OUT "theme(axis.text.x = element_text(angle = 30, hjust = 0.5, vjust = 0.5,size=rel(1))) +\n";
print OUT "theme_bw()+theme(panel.grid.major= element_line(color = \"white\"),panel.grid.minor =element_line(color= \"white\"),legend.title = element_blank()) +\n";
print OUT "labs(title=\"$title\",x=\"$xlab\",y=\"$ylab\") +\n";
print OUT "theme(plot.title = element_text(hjust = 0.5))\n";
print OUT "p\n";
print OUT "dev.off()\n";

`Rscript $filedir/$out.barbox.R`;

my $obj=Archive::Zip->new();
$obj->addFile("out/$out.pdf");
$obj->writeToFileNamed("out.zip") 
