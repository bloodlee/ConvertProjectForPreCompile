# THis file is for convert the current source file to pre-compile status.

import os
import sys
import re

sourceRe=re.compile(r'"\S+.cpp"')
headerRe=re.compile(r'"\S+[.]h"')
wxlibRe=re.compile(r'#include "wx(/|\\)\S+.h"')
stdRe=re.compile(r'#include <\S+>')

def parseProjFile(filename):
    try:
        fileObj=open(filename,'r')
    except:
        print u'File read error! Can not find %s ' % filename
        exit(1)
        
    buffer=fileObj.readlines(50)
    headers=[]
    sources=[]
    while buffer:

        for index in range(len(buffer)):
            #print buffer[index]
            m=sourceRe.findall(buffer[index])
            if m:
                for i in range(len(m)):
                    line=m[i]
                    sources.append(line[1:-1])

            m=headerRe.findall(buffer[index])
            if m:
                for i in range(len(m)):
                    line=m[i]
                    headers.append(line[1:-1])
        
        buffer=fileObj.readlines(50)
    fileObj.close()

    return (sources, headers)

def parseSingleFile(backup_dirname, filename, allincludes):
    try:
        fileObj=open(filename,'r')
    except:
        print u'File read error! Can not find %s ' % filename
        print u'SKIP this file and CONTINUE...'
        return

    newfilename=backup_dirname+filename
    
    try:
        outfileObj=open(newfilename+'', 'w')
    except:
        index1=newfilename.rfind('\\')
        index2=newfilename.rfind('/')
        
        if index1 == -1 and index2 == -1:
            print u"Can not find symbol indicated the directory!"
            exit(1)
        
        if index1 > index2:
            index=index1
        else:
            index=index2
        
        if newfilename[0:index].find('util') != -1 or newfilename[0:index].find('render') != -1:
            print u'Skip the file under folder "util" or "render"'
            return
        
        try:
            os.mkdir(newfilename[0:index])
        except:
            print u'Making directory %s Error!' % newfilename[0:index]
            print u'Current file: %s' % newfilename
            print u'Current index: %s' % index
            print u'Continue...'
            return
        
        try:
            outfileObj=open(newfilename+'', 'w')
        except:
            print u'File write error! The path (%s) is invalid!' % (backup_dirname+filename)
            exit(1)

    if filename[-3:]=='cpp':
        outfileObj.write('#include "stdwx.h"\n')

    buffer=fileObj.readlines(50)
    while buffer:
        for lineIndex in range(len(buffer)):
            m=wxlibRe.findall(buffer[lineIndex])
            if m:
                for i in range(len(m)):
                    allincludes.add(buffer[lineIndex])

            m2=stdRe.findall(buffer[lineIndex])
            if m2:
                for i in range(len(m2)):
                    allincludes.add(buffer[lineIndex])

            if not m and not m2:
                outfileObj.write(buffer[lineIndex])
                    
        buffer=fileObj.readlines(50)

    fileObj.close()
    outfileObj.close()

#os.remove(filename)
#os.rename(filename+'.bak', filename)

def genPreCompileFiles(backup_dirname, allincludes):
    fileObj=open(backup_dirname + r'stdwxtmp.h', 'w')

    print len(allincludes)
    for line in allincludes:
        fileObj.write(line)

    fileObj.close()

    fileObj=open(backup_dirname + r'stdwxtmp.cpp','w')

    fileObj.write(r'#include "stdwxtmp.h"')

    fileObj.close()
    
# Real process begins here...

if (len(sys.argv) != 2):
    print u'Usage: ConvertFileForPreCompile.py [vcproject filename or source file list]'
    exit(1)

#Get the filename
filename=sys.argv[1]

#backup_dir=raw_intput(u'Where to put the new generated files? ')
backup_dirname='..\\newGUI3\\'

if filename[-6:]=='vcproj':
    print u'Start parsing the vc project file...'
    sources, headers=parseProjFile(filename)

    print u'Finish pre-processing.'
    
    allincludes=set()
    allfiles=sources+headers
    count=len(allfiles)
    for i in range(count):
        print u'Begin parsing file:%s(%d/%d)...' % (allfiles[i], i+1, count)
        parseSingleFile(backup_dirname, allfiles[i], allincludes)

    print u'Finish every single source/header file.'

    genPreCompileFiles(backup_dirname, allincludes)
    
    print u'Finish generating pre-compile header/source files.'


