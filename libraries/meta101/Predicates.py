import imp
import os
import re
import json
import sys
from   .Phase import Phase
from   .util  import tolist
from   .Matches   import Matches

"""
Predicates 101rules matches phase.
"""

class Predicates(Phase):
    """
    The predicates 101rules matches phase - see Phase. The suffix for this
    phase is ``.predicates.json''.
    """
    suffix = ".predicates.json"
    regex  = re.compile(r"^\w+$")


    def __init__(self, *args):
        """
        Adds a set of predicates to the regular phase.
        """
        super(Predicates, self).__init__(*args)
        self.predicates = set()


    def dump(self):
        """
        Converts the set of predicates into a list and adds it to the dump.
        """
        dump = super(Predicates, self).dump()
        dump["predicates"] = sorted(list(self.predicates))
        return dump


    def applicable(self, rule):
        """
        Returns true if the given rule contains a predicate key.
        """
        return "predicate" in rule


    def keys(self):
        """
        Adds a predicate key to the end of the regular phase's keys.
       """
        return super(Predicates, self).keys() + ["language","predicate"]


    def checkpredicate(self, predicate, rule, filename, **kwargs):
        """
        Checks if a specific predicate is safe to execute (module and predicate description are valid)
        and finnaly execute the predicate with the specific arguments. The result of the execution will be returned
        """
        if not self.regex.match(predicate):
            raise ValueError("weird predicate name: " + predicate)

        args = tolist(rule["args"]) if "args" in rule else []
        path = os.path.join(os.environ["predicates101dir"],
                            predicate, "predicate.py")
        descriptionpath = path[:-2] +  "json"

        if(self.resolvedpredicatedependencies(descriptionpath) == False):
            return False
        numargs = self.getnumargs(descriptionpath)

        self.predicates.add(predicate)

        module = imp.load_source("PREDICATE_" + predicate, path)
        #The '+1' here is because there is also the filename a part of the argument
        if (numargs is not None):
            if (numargs[0] is not None and numargs[0] > len(args) + 1):
                 print >> sys.stderr, "We expected more arguments"
                 return False
            if (numargs[1] is not None and numargs[1] < len(args)):
                print >> sys.stderr, "We expected less arguments"
                return False

        return module.run(filename, *args)

    def findlanguage(self, matchespath):
        """
        Returns the language of the file that is analysed right now. It does that by reading the matched files
        """
        if os.path.isfile(matchespath):
            with open(matchespath) as f:
                matches = json.load(f)

            for match in matches:
                if "language" in match["metadata"]:
                    return match["metadata"]["language"]
        return ""

    def checklanguage(self, language, rule, filename, result, targetbase, **kwargs):
        """
        Checks if the language in the rule matches the language of the file
        """
        return language == self.findlanguage(targetbase + Matches.suffix)


    def resolvedpredicatedependencies(self, descriptionfile):
            """
            Returns True if all module dependencies of the predicate description are as well part of the module description
            """
            with open(descriptionfile) as f:
                matches = json.load(f)
                predicatedependencies    = matches["dependencies"]
            moduldescription = os.environ["predicates101deps"]
            with open(moduldescription) as f:
                modul = json.load(f)
                modulDependencies  = modul["dependencies"]

            for dependency in predicatedependencies:
                if dependency not in modulDependencies:
                    print >> sys.stderr, "Error! The Module " + dependency + " should be part of the modul dependencies in predicate101. " \
                           "We will continue the execution though "
                    return False
            return True

    def getnumargs(self, descriptionfile):
         """
         Returns the number of arguments that the predicate expects according to the predicate description
         """
         with open(descriptionfile) as f:
                matches = json.load(f)
                numargs            = matches["args"]
         return numargs