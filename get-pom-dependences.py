#!/usr/bin/python
# This script helps to find all dependencies in maven pom files.
# Usage:
# find /code_dir -iname pom.xml | ./get-pom-dependencies.py | sort | uniq
# ./get-pom-dependencies.py -l
# with -l arg, the path of pom.xml will be printed.
import sys
import os
from xml.etree import ElementTree
import re


def parse(pom_files):
    for line in pom_files:
        pom_file = os.path.abspath(line.rstrip())

        ns = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}

        tree = ElementTree.parse(pom_file)
        root = tree.getroot()

        deps = root.findall(".//xmlns:dependency", namespaces=ns)
        for d in deps:
            group_id = (d.find("xmlns:groupId", namespaces=ns)
                        .text.strip(' \n\t'))

            artifact_id = (d.find("xmlns:artifactId", namespaces=ns)
                           .text.strip(' \n\t'))

            version = ''
            version_element = d.find("xmlns:version", namespaces=ns)
            if version_element is not None:
                version = version_element.text.strip(' \n\t')
                p = re.compile(r'\${(.*)}')
                if p.match(version) is not None:
                    version_ref = ".//xmlns:" + p.findall(version)[0]
                    ref_element = root.find(version_ref, namespaces=ns)
                    if ref_element is not None:
                        version = ref_element.text

            yield pom_file, group_id, artifact_id, version


if len(sys.argv) > 1 and sys.argv[1] == '-l':
    for pom_file, group_id, artifact_id, version in parse(sys.stdin):
        sys.stdout.write('{0}\t{1}\t{2}\t{3}\n'
                         .format(group_id, artifact_id, version, pom_file))
else:
    for pom_file, group_id, artifact_id, version in parse(sys.stdin):
        sys.stdout.write('{0}\t{1}\t{2}\n'
                         .format(group_id, artifact_id, version))
