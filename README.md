CS411Project
============

Authors: Gary Foreman, Halie Rando, Kavya Kannan, and Assma Boughoula  
email: gforema2@illinois.edu, rando2@illinois.edu, kkannan2@illinois.edu, boughou1@illinois.edu  
[FoxDB website](http://gforema2.pythonanywhere.com/)  

Description
-----------

Web application that integrates genotype data with pedigree records to allow researchers to access and interpret their data without requiring significant experience with computers. It will provide outputs in the formats they need for downstream bioinformatic software, and will allow them to tag biological samples as belonging to particular “sets” of interest (much like applying a label in GMail). However, the greatest attraction of the application we are building is that it will use pedigree information to run a quality check of SNPs or microsatellites based on the basic principles of genetic inheritance, and will flag those which appear to be anomalous due to a number of possible mistakes including sequencing error, mislabeling of a sample, or misattributed paternity. The application will be broadly relevant to all research that integrates SNP or microsatellite assays with pedigree data, but will need to be adjusted slightly for individual data sets. We will design a streamlined application catered to the work of the [Kukekova Lab](http://ansci.illinois.edu/labs/kukekova-lab) in the Animal Sciences department here at UIUC.

Current Functionality
---------------------

Ability to query the database and insert, update, and delete tuples from database tables through the web-based frontend. Visualization of pedigree trees and genotype inheritance. 

Directory Layout
----------------

* `FoxDB/` contains all code used for the web application (implemented using Flask).  
* `DBinit/` contains scripts for initializing the database.  
* `tempCode/` contains code to be incorporated into the web application.
