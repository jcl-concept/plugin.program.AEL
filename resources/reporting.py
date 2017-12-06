from abc import ABCMeta, abstractmethod

from utils import *
from utils_kodi import *

class Reporter(object):
    __metaclass__ = ABCMeta

    def __init__(self, launcher, decoratorReporter = None):

        self.launcher = launcher
        self.decoratorReporter = decoratorReporter

    @abstractmethod
    def open(self):
        pass
    
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def _write_message(self, message):
        pass

    def write(self, message):
        
        self._write_message(message)

        if self.decoratorReporter:
            self.decoratorReporter.write(message)

class LogReporter(Reporter):
       
    def open(self, report_title):
        return super(LogReporter, self).close()

    def close(self):
        return super(LogReporter, self).close()

    def _write_message(self, message):
        log_info(message)

class FileReporter(Reporter):
    
    def __init__(self, reports_dir, launcher, decoratorReporter = None):
        
        self.report_file = reports_dir.pjoin(launcher['roms_base_noext'] + '_report.txt')
        super(FileReporter, self).__init__(launcher, decoratorReporter)

    def open(self, report_title):

        log_info('Report file OP "{0}"'.format(self.report_file.getOriginalPath()))

        self.report_file.open('w')

        # --- Get information from launcher ---
        launcher_path = FileName(self.launcher['rompath'])
        launcher_exts = self.launcher['romext']
        
        self.write('*** Report: {} ... ***\n'.format(report_title))
        self.write('  Launcher name "{0}"\n'.format(self.launcher['m_name']))
        self.write('  Launcher type "{0}"\n'.format(self.launcher['type'] if 'type' in self.launcher else 'Unknown'))
        self.write('  launcher ID   "{0}"\n'.format(self.launcher['id']))
        self.write('  ROM path      "{0}"\n'.format(launcher_path.getPath()))
        self.write('  ROM ext       "{0}"\n'.format(launcher_exts))
        self.write('  Platform      "{0}"\n'.format(self.launcher['platform']))
    
    def close(self):
        self.report_file.close()

    def _write_message(self, message):
        self.report_file.write(message + '\n')