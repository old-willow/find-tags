#! /usr/bin/python
# -*- coding: utf-8 -*-

""" This little program parses trough html or any kind of ML file to find some
tags that user defined previousely in source code and returns all pairs of
open/closed tags, plus counts the number of tag pairs in the file.
Program uses recursive approach.

Usage:
    In console type:
        $: python find_tags.py >output

    then open the output file in your favourite text editor and enjoy the result!

file: find_tags.py
Author: Kolozsi Róbert
Date: Oct 21, 2011.
email: robert.kolozsi@gmail.com
"""

#import sys
import os

# These are global variables
startpattern = "<a href="  # Change this
endpattern = "</a>"        # and change this!

status = False
numlinks = 0
nestedlinks = 0
tmplist = []  # for storing elements of list (part of broken link in to separated lines)
startpatlen = len(startpattern)
endpatlen = len(endpattern)


# Functions
def open_file():
    """
    Change the string part of filename variable
    to the appropriate one on your computer.
    """
    filename = os.path.normpath('/home/name/index.html')
    fp = open(filename, 'r')
    content = fp.readlines()
    return content


def find_links():
    content = open_file()
    global numlinks
    result = []
    global tmplist
    #i = 0

    for line in content:
        check(result, line)

    for r in result:
        print r

    #print "tmplist:", tmplist
    print "Total number of links on this page are:", numlinks

    if nestedlinks is not 0:
        print "You have {0} unclosed links!".format(nestedlinks)


def check(result, s):
    """
    Function look up for open and closing tags in ML files.
    To change the tag names to one You are looking for:
        change the 'startpattern' and 'endpattern' variables in source code
        to the desired one at 26. and 27. lines.
    """
    slen = len(s)
    global status  # are we in link
    global numlinks
    global nestedlinks
    global tmplist
    global startpattern
    global startpatlen
    global endpattern
    global endpatlen

    if status is False:  # If we are not in link
        startloc = s.find(startpattern)

        if startloc is not -1:
            status = True
            numlinks += 1
            #print "NUMBER OF LINKS:", numlinks
            if startloc + startpatlen + 1 < slen:
                newstring = s[startloc:startloc + startpatlen].strip()
                tmplist.append(newstring)
                check(result, s[startloc + startpatlen:])
        else:
            tmplist = []  # This thing actualy doesn't do anything /can be cleaned/

    elif status is True:  # If we are in broken link in two or more lines or in nested link
        endloc = s.find(endpattern)
        startloc = s.find(startpattern)
        if endloc is not -1 and startloc is -1:  # Single line open/close tags or closing tag in nested tags
            newstring = s[:endloc + endpatlen].strip()
            tmplist.append(newstring)
            if nestedlinks > 0:
                nestedlinks -= 1
            else:
                finalstring = ''.join(tmplist)
                result.append(finalstring)
                tmplist = []
                status = False
            if endloc + endpatlen + 1 < slen:
                check(result, s[endloc + endpatlen:])

        elif endloc is -1 and startloc is not -1:  # Line with nested open tags broken in to multiply lines
            newstring = s[:startloc].strip()
            tmplist.append(newstring)
            numlinks += 1
            nestedlinks += 1
            newstring = s[startloc:startloc + startpatlen]
            tmplist.append(newstring)
            if startloc + startpatlen + 1 < slen:
                check(result, s[startloc + startpatlen:])

        elif endloc is not -1 and startloc is not -1:

            if endloc < startloc:  # Sequentialy occourance of open/close tags
                newstring = s[:endloc + endpatlen].strip()
                tmplist.append(newstring)
                finalstring = ''.join(tmplist)
                result.append(finalstring)
                tmplist = []
                status = False
                check(result, s[endloc + endpatlen:])

            elif endloc > startloc:  # Nested open/close tags
                newstring = s[:startloc + startpatlen].strip()
                tmplist.append(newstring)
                numlinks += 1
                nestedlinks += 1
                check(result, s[startloc + startpatlen:])

        else:
            '''If we are in link but no open and closing tags were found'''
            newstring = s[:].strip()
            tmplist.append(newstring)


def main():
    find_links()


if __name__ == '__main__':
    main()
