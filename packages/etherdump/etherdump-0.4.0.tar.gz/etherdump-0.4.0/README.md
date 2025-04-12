etherdump
=========

Tool to help manage periodic publishing of [etherpads](http://etherpad.org/) to static files, preserving metadata. Uses the etherpad API (and so it requires having the APIKEY.txt contents of an etherpad installation).


Requirements
-------------
	* python3
	* html5lib
	* requests (settext)
	* python-dateutil, jinja2 (index subcommand)

Installation
-------------

    pip install python-dateutil jinja2 html5lib
    python setup.py install

Usage
---------------
	mkdir mydump
	cd myddump
	etherdump init

The program then interactively asks some questions:

	Please type the URL of the etherpad: 
		http://automatist.local:9001/
	The APIKEY is the contents of the file APIKEY.txt in the etherpad folder
	Please paste the APIKEY: 
		xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

The settings are placed in a file called .etherdump/settings.json and are used (by default) by future commands.


	etherdump list

You should see a list of pads.


subcommands
----------

* init
* pull
* list

* listauthors
* gettext
* settext
* gethtml
* creatediffhtml
* revisionscount
* index
* deletepad
* pushhtml

To get help on a subcommand:

	etherdump revisionscount --help


Cookbook
========================

Using etherdump to migrate from one etherpad instance to another
------------------------------------------------------------------

    mkdir instance1 && cd instance1
    etherdump init
    etherdump pull --html --meta

    (cd ..)
    mkdir instance2 && cd instance2
    etherdump init
    etherdump pushhtml --basepath ../instance1 ../instance1/p/*.meta.json

NB: sethtml/pushhtml seems to only work on the server itself, ie using API url such as localhost:9001.

NB: This command indescriminantly clobbers pads in instance2 with the HTML of the dumped versions from instance1.

This technique can be used to "reset" the database of a pad by recreating pads (without their history or editor info/colors) in a fresh database.


Magicwords
=================
Following the suggestions of sister project/friendly fork [etherpump](https://git.vvvvvvaria.org/varia/etherpump/), the magic word mechanism has been expanded (from the inital single hard coded \_\_NOPUBLISH__ value) to and generalized to allow a the use of text markers in the source text to control various options, including options for use in preprocessing and translation of markdown using pandoc.







Change log / notes
=======================

Originally designed for use at: [constant](http://etherdump.constantvzw.org/).


17 Oct 2016
-----------------------------------------------
Preparations for [Machine Research](https://machineresearch.wordpress.com/) [2](http://constantvzw.org/site/Machine-Research,2646.html)


6 Oct 2017
----------------------
Feature request from PW: When deleting a previously public document, generate a page / pages with an explanation (along the lines of "This document was previously public but has been marked .... maybe give links to search").

3 Nov 2017
---------------
machineresearch seems to be \_\_NOPUBLISH__ but still exists (also in recentchanges)

Jan 2018
-------------
Updated files to work with python3 (probably this has broken python2).

Jun 2019
-------------
Revised sethtml & added pushhtml

Sep 2021
-----------
Adding/updating general purpose magicwords
