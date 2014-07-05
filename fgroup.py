import os
from os import path, listdir, access, getcwd
from os.path import isfile, isdir, normpath, basename, splitext, commonprefix
import sys
import numpy as np

#def getargs():
#	if len(sys.argv)>1:
#		return sys.argv[1:]
#	else:
#		return [getcwd()]
def hasriffhead(path):
	f=open(path,"rt")
	ascii4c = f.read(4)
	return ascii4c=="RIFF"
	
def fname(path):
	return splitext(basename(path))[0]
	
############################################################
# Group wave audio files by common prefix
#
# - returns two lists: outPaths and outNames
# - outPaths is a list of groups of paths to files with
#   similar prefixes
# - outNames is a list of the prefixes for file groups in
#   outPaths
#
# outPaths = [["C:\l1.wav", "C:\l2.wav"], ["C:\r1.wav", "C:\r2.wav"]]
# outNames = ["l", "r"]
#
#  NOT FULLY FUNCTIONAL!!
#  ARRAYS CREATED BY rec_divide NEED TO BE SPLIT BASED
#  ON THE LENGTH OF THE COMMON PREFIX BEFORE FLATTENING!!
#
############################################################
def fgrp(pth, debug=False):
	pth=normpath(pth)
	if not isdir(pth):
		print "Not a path!"
		return
	files = listdir(pth)
	if debug:
		print "name: isfile, isdir"
	
	wavs = []
	fnames = []
	for arg in files:
		fpath=path.join(pth,arg)
		if debug:	
			print arg,": ",isfile(fpath),", ",isdir(fpath)
		
		if isfile(fpath) and access(fpath, os.R_OK) and hasriffhead(fpath):
			wavs.append((fpath,fname(fpath)))
			fnames.append(fname(fpath))
	
	outNames = rec_divide(fnames,0)
	outPaths=outNames
	for pth,fn in wavs:
		print "fn: ",fn," , fpath: ",pth
		outPaths = rec_replace(outPaths,fn,pth)
	
	
	
	for idx,arr in enumerate(outNames):
		outNames[idx]=commonprefix(arr)
	
	return outPaths, outNames
	
	
	return wavs
def unique(l):
	return list(set(l))
def rec_divide(inputArr,depth=0):
	searchArr = []
	skipped=0
	for input in inputArr:
		if(len(input)>depth):
			searchArr.append(input[depth])
		else:
			skipped+=1		
	searchArr=unique(searchArr)
	if len(searchArr)==len(inputArr)-skipped:
		return inputArr #everything at this depth is unique already, return
	outArr=[]
	for idx,uq in enumerate(searchArr):
		dArr = []
		for input in inputArr:
			if(len(input)>depth) and input[depth]==uq:
				dArr.append(input)
		outArr.append(dArr)
	for idx,arr in enumerate(outArr):
		outArr[idx]=rec_divide(arr,depth+1)
	return rec_dflatten(outArr,1)
#flatten to a set depth
def rec_dflatten(inArr, maxdepth=1):
	outArr=[]
	if(maxdepth==0):
		return rec_flatten(inArr)
	for arr in inArr:
		if not isinstance(arr,basestring):
			outArr.append(rec_dflatten(arr,maxdepth-1))
		else:
			outArr.append(rec_flatten(arr))
	return outArr
def rec_flatten(inArr):
	outArr = []
	if len(inArr)>0 and not isinstance(inArr,basestring):
		for arr in inArr:
			if isinstance(arr, basestring):
				outArr.append(arr)
			else:
				outArr.extend(rec_flatten(arr))
		return outArr
	return inArr
def rec_replace(inputArr, original, replacement):
	if isinstance(inputArr, basestring):
		if inputArr==original:
			return replacement
		return original
	outputArr=[]
	for arr in inputArr:
		if isinstance(arr, basestring):
			if arr==original:
				outputArr.append(replacement)
			else:
				outputArr.append(arr)
		else:
			outputArr.append(rec_replace(arr,original,replacement))
	return outputArr

	
#def main():
#	fpath=getargs()[0]
#	print fgrp(fpath)
	

#if __name__=="__main__":
#	main()

