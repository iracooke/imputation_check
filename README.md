# Check genotype imputation

Programs like beagle and shapeit will atempt to impute genotypes by inferring the most likely haplotype based on neighbouring loci.

The accuracy of this process is heavily dependent on accuracy of other genotypes in the file and presumably other factors such as snp density, but neither beagle or shapeit give reliable measures of accuracy for this process.

If you have genotypes that you know are accurate (eg from deep sequencing) you can assess imputation accuracy as follows;


Assume you have a file with genotype calls for many individuals from deep sequencing called `deep.vcf`

1. Prepare the input vcf by extracting a single contig/scaffold 
	```bash
	vcftools --vcf deep.vcf  --chr sc01 --recode --recode-INFO-all --stdout > sc01_deep.vcf
	```
2. Create a filtered genotype set
	```bash
	prune_vcf.py sc01_deep.vcf -l 500000 --save-filtered sc01_deep_null.txt > sc01_deep_null.vcf
	```

This produces a new vcf file `sc01_deep_null.vcf` that can be used for imputation because it still contains all the individuals.  In addition the genotypes that were removed get written to a text file like this;

```asis
record	CHROM	POS	sample_index	GQ	GT	RO	AO
139	Sc0000000	7041	78	None	./.	None	None
149	Sc0000000	7308	35	28	0/0	2	0
285	Sc0000000	12407	120	29	0/0	2	0
360	Sc0000000	14049	120	25	0/0	1	0
407	Sc0000000	15830	57	33	0/0	5	0
439	Sc0000000	16734	101	33	0/0	4	0
446	Sc0000000	16807	84	0	./.	0	2
488	Sc0000000	17978	23	0	./.	0	2
```

Note that it keeps track of the position and also the index of the sample that was removed.  This is important for later because you might only have a subset of samples with deep coverage that you want to use as your reference benchmark.

3. Perform your imputation. Eg with shapeit or beagle.  As input you should use the filtered file `sc01_deep_null.vcf` .  As output you should get a fully imputed vcf.  Let's assume it is called `sc01_haps.txt.vcf`

4. Compare the imputed with the original result

```bash
compare_vcf.py Sc0000000_haps.txt.vcf Sc0000000_null.txt > Sc0000000_null.imputed.txt
join Sc0000000_null.refalt.txt Sc0000000_null.imputed.txt | tr '|' '/' > Sc0000000_null.compare.tsv

```
