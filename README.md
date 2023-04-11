# CNVdetector

## **Introduction**

This script is used to extract copy number variations (CNVs) from BAM files and classify them according to their type using annotation files in BED and VCF formats. This code was developed as a specific solution for CHU de Nîmes and may require adjustments to work in other environments.

## **Prerequisites**

This project requires Python to be installed on your system. Make sure to have Python version 3.7.4 or above installed before running the code.
This script requires the following Python libraries :

    os
    pysam
    pandas
    datetime

## **Usage**

Make sure that the BAM, VCF, and BED files are in the same directory as the script CNVdetector.py and avoid using shortcuts.

Run the script in a terminal by navigating to the directory containing the script by the following the python command :

    CNVdetector.py

The output of the script will be saved in a CSV file with the format cnv_listing_yyyy-mm-dd_HH-MM-SS.csv where yyyy-mm-dd_HH-MM-SS is the current date and time. If the output file already exists, you will be prompted to overwrite it or choose a different name.

## **Input**

The script requires the following files in the same directory:

    A BAM file containing aligned sequencing reads
    A VCF file containing variants
    A BED file containing annotations of genomic regions

## **Output**

The script outputs a CSV file containing the following columns:

    Chromosome
    Start position
    End position
    Length
    Type of CNV
