#!/usr/bin/env python

import glob
import os
import re
import shutil
import urllib.request

from grs.Constants import CONST
from grs.Execute import Execute
from grs.Rotator import Rotator


class Seed(Rotator):
    """ doc here
        more doc
    """

    def __init__(self, stage_uri, tmpdir = CONST.TMPDIR, portage_configroot = \
            CONST.PORTAGE_CONFIGROOT, package = CONST.PACKAGE, logfile = CONST.LOGFILE):
        """ doc here
            more doc
        """
        self.stage_uri = stage_uri
        self.portage_configroot = portage_configroot
        self.package = package
        filename = os.path.basename(stage_uri)
        self.filepath = os.path.join(tmpdir, filename)
        self.logfile = logfile


    def seed(self):
        """ doc here
            more doc
        """
        # Rotate the old portage_configroot and package out of the way
        for directory in [self.portage_configroot, self.package]:
            self.rotate(directory)
            if os.path.isdir(directory):
                shutil.move(directory, '%s.0' % directory)
            os.makedirs(directory, mode=0o755, exist_ok=False)

        # Download a stage tarball if we don't have one
        if not os.path.isfile(self.filepath):
            request = urllib.request.urlopen(self.stage_uri)
            with open(self.filepath, 'wb') as f:
                shutil.copyfileobj(request, f)

        # Because python's tarfile sucks
        cmd = 'tar --xattrs -xf %s -C %s' % (self.filepath, self.portage_configroot)
        Execute(cmd, timeout=120, logfile=self.logfile)
        #os.unlink(self.filepath)
