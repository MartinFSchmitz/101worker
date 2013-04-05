# -*- coding: utf-8 -*-

import json
import commands
import os
import sys
sys.path.append('../../libraries/101meta')
import const101

def exists(path):
    fullPath = os.path.join(const101.sRoot, path)
    return os.path.exists(fullPath)

def getMetadata(filePath):
    locator, extractor, geshi = None, None, None
    matchesFile = os.path.join(const101.tRoot, filePath + '.matches.json')

    if os.path.exists(matchesFile):
        matches = json.load(open(matchesFile))

        for unit in matches:
            if 'locator' in unit['metadata']  : locator = unit['metadata']['locator']
            if 'extractor' in unit['metadata']: extractor = unit['metadata']['extractor']
            if 'geshi' in unit['metadata']    : geshi = unit['metadata']['geshi']
    return locator, extractor, geshi

def getTerms(file):
    terms = []
    predicatesFile = os.path.join(const101.tRoot, file + '.predicates.json')

    if os.path.exists(predicatesFile):
        predicates = json.load(open(predicatesFile, 'r'))

        for unit in predicates:
            if 'term' in unit['metadata']:
                terms.append(unit['metadata']['term'])
            if 'phrase' in unit['metadata']:
                terms += unit['metadata']['phrase']
        terms = list(set(terms))
    return terms

def getFragment(file, fragment, locator):
    fullFile = os.path.join(const101.sRoot, file)
    fullLocator = os.path.join(const101.sRoot, locator)
    command = '{0} {1} < {2}'.format(fullLocator, fragment, fullFile)
    status, output = commands.getstatusoutput(command)
    if not status == 0: raise Exception('Fragment location failed: {0}'.format(output))

    return json.loads(output)

def getFacts(file, extractor):
    #since the extractor module isn't ready to deal with the new form of communicating, I commented the file lookup out
    #for now
    #extractorFile = os.path.join(const101.tRoot, file + '.extractor.json')
    #if os.path.exists(extractorFile):
    #    return json.load(open(extractorFile, 'r'))

    fullFile = os.path.join(const101.sRoot, file)
    fullExtractor = os.path.join(const101.sRoot, extractor)
    command = '{0} < {1}'.format(fullExtractor, fullFile)
    status, output = commands.getstatusoutput(command)
    if not status == 0: raise Exception('Fact extraction failed: {0}'.format(output))

    return json.loads(output)

def isDir(dir):
    path = os.path.join(const101.sRoot, dir)
    return os.path.isdir(path)

def getDirContent(dir):
    files, dirs = [], []
    path = os.path.join(const101.sRoot, dir)
    if os.path.exists(path):
        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path, f)):
                dirs.append(f)
            else:
                files.append(f)

    files.sort()
    dirs.sort()

    return files, dirs

def getMembers(dir):
    path = os.path.join(const101.tRoot, dir, 'members.json')
    if os.path.exists(path):
        members = json.loads(open(path, 'r').read().decode('utf-8'))
        members.sort()
        return members
    return []

def getGithub(namespace, member):
    pullRepoDump = json.load(open(const101.pullRepoDump, 'r'))
    if member in pullRepoDump:
        return pullRepoDump[member]

    path = os.path.join(namespace, member)
    if os.path.exists(os.path.join(const101.sRoot,path)):
        return os.path.join(const101.url101repo, path)
    return None

def read(filePath, lines=None):
    fullPath = os.path.join(const101.sRoot, filePath)
    fp = open(fullPath, 'r')
    if lines:
        txt = [x for i, x in enumerate(fp) if i in lines]
    else:
        txt = fp.readlines()
    return ''.join(txt)

def getCommitInfo(filePath):
    initiator, contributors = None, None
    commitFile = os.path.join(const101.tRoot, filePath+'.commitInfo.json')
    if os.path.exists(commitFile):
        data = json.load(open(commitFile, 'r'))
        if len(data) > 0:
            initiator = data[0]
            contributors = data[1:]
    return initiator, contributors