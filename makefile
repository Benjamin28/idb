#!/bin/bash
FILES :=                              \
	.gitignore                        \
	.travis.yml                       \
	apiary.apib                       \
	IDB.log                          \
	app/models.py                     \
	tests.py                          \
	IDB1.pdf                          \
	apiary.apib

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

html:
	python3 -m pydoc -w app/models.py

versions:
	# this does nothing right now

log:
	git log > IDB3.log

restart:
	service apache2 reload
	service apache2 restart

permissions:
	chmod go+wr database.db

unittest:
	python3 ./tests.py

unittestReturn:
	python3 ./tests.py &> testResults

unittestClean:
	rm testResults

test: html log check
