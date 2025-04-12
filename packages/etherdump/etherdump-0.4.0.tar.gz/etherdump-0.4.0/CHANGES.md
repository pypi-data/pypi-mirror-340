CHANGE LOG
================


2022 02 11
----------------

2022 Revisiting etherdump code to really consider what's used and deprecate useless / questionable subcommands.
ALSO in order to add new commands for pre/post processing + magic words...

Does it makes sense to use scons internally?


### tested / useful

* list
* listauthors
* deletepad
* pull
* index
* init
* pushhtml
* sethtml
* settext
* revisionscount (sub behaviour of showmeta?)
* gettext
* status OK it's there to work like git, but is it used?
* dumpcsv
* template
* html5tidy
* preprocess


### deprecate?

* showmeta: only opens a .meta.json file from padid, rather lame and misleading -- or improve it!?
* join
* appendmeta

variations on pull?
	creatediffhtml
	gethtml

### magicwords

How to do in a *porous* way... ie could magicwords by (python/bash) scripts!
And how could they (best) be defineable external to etherdump...

Dynamic import.. but would be cool to have a mix of built in (basis) behavious like {{NOPUBLISH}}





