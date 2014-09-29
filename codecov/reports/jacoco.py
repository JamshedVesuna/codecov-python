import os


def from_xml(xml, path=None):
    """
    nr = line number
    mi = missed instructions
    ci = covered instructions
    mb = missed branches
    cb = covered branches
    """
    coverage, stats = {}, {"branches":{},"methods":{},"classes":{},"instructions":{}}
    for package in xml.getElementsByTagName('package'):
        for sourcefile in package.getElementsByTagName('sourcefile'):
            file_name = "%s/%s" % (package.getAttribute('name'), sourcefile.getAttribute('name'))
            lines = [(int(f.getAttribute('nr')), True if f.getAttribute('cb')!='0' else int(f.getAttribute('ci'))) for f in sourcefile.getElementsByTagName('line')]
            coverage[file_name] = [None] * (max(map(lambda a: a[0], lines))+1)
            for line in lines:
                coverage[file_name][line[0]] = line[1]
            for c in sourcefile.getElementsByTagName('counter'):
                typ = dict(INSTRUCTION="instructions",BRANCH="branches",METHOD="methods",CLASS="classes").get(c.getAttribute('type'))
                if typ:
                    stats[typ][file_name] = int(c.getAttribute('missed')) + int(c.getAttribute('covered'))
    
    # find a source file to append report path
    if path:
        a_file_path = coverage.keys()[0]
        # look for that path
        try:
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    if os.path.exists(os.path.join((root, a_file_path))):
                        path = root
                        raise Exception
        except:
            pass

    return dict(coverage=coverage, 
                stats=stats,
                meta=dict(report="jacoco.xml", path=path))
