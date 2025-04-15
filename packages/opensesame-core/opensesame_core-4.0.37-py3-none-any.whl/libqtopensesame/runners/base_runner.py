# -*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import traceback
from qtpy import QtWidgets
from libqtopensesame.misc.config import cfg
from libopensesame.oslogging import oslogger
from libopensesame.experiment import Experiment
from libopensesame.py3compat import *
from libqtopensesame.misc.translate import translation_context
_ = translation_context('base_runner', category='core')


class BaseRunner:
    """
    A runner implements a specific way to execute an OpenSesame experiment from
    within the GUI. The base_runner is an abstract runner that is inherited by
    actual runners.

    Parameters
    ----------
    main_window : QtOpenSesame
    """
    
    valid_logfile_extensions = '.csv', '.txt', '.dat', '.log', '.json'
    supports_kill = False

    def __init__(self, main_window):
        self.main_window = main_window
        self.paused = False

    @property
    def console(self):
        return self.main_window.console

    @property
    def tabwidget(self):
        return self.main_window.tabwidget

    def execute(self):
        """
        Executes the experiments. This function should be transparent and leave
        no mess to clean up for the GUI.

        Returns:
        None if the experiment finished cleanly, or an Exception (any kind) if
        an exception occurred.
        """
        pass

    def get_logfile(self, quick=False, subject_nr=0, file_extension='.csv'):
        """
        Gets the logfile for the current session, either by falling back to a
        default value ('quickrun.csv') or through a pop-up dialogue.

        Parameters
        ----------
        quick : bool, optional
            A boolean to indicate whether default should be used for the
            log-file and subject number. Mostly useful while testing the
            experiment.
        subject_nr : int, optional
        file_extension : str, optional

        Returns
        -------
        str or None
            A pathname for the logfile or None if no logfile was chosen (i.e.
            the dialogue was cancelled).
        """
        remember_logfile = True
        if quick:
            logfile = os.path.join(
                cfg.default_logfile_folder,
                cfg.quick_run_logfile)
            try:
                open(logfile, 'w').close()
                os.remove(logfile)
            except Exception:
                import tempfile
                from libopensesame import misc
                oslogger.warning('failed to open %s' % logfile)
                logfile = os.path.join(
                    safe_decode(
                        tempfile.gettempdir(),
                        enc=sys.getfilesystemencoding()),
                    safe_decode(
                        tempfile.gettempprefix(),
                        enc=sys.getfilesystemencoding()
                    ) + f'quickrun{file_extension}')
                oslogger.warning('Using temporary file %s' % logfile)
                remember_logfile = False
        else:
            # Suggested filename
            suggested_path = os.path.join(
                cfg.default_logfile_folder,
                f'subject-{subject_nr}{file_extension}'
            )
            # Get the data file
            file_filter = f'Log file ({file_extension})'
            logfile = QtWidgets.QFileDialog.getSaveFileName(
                self.main_window.ui.centralwidget,
                _("Choose location for logfile (press 'escape' for default location)"),
                suggested_path, filter=file_filter)
            # In PyQt5, the QFileDialog.getOpenFileName returns a tuple instead
            # of a string, of which the first position contains the path.
            if isinstance(logfile, tuple):
                logfile = logfile[0]
            # An empty string indicates that the dialogue was cancelled, in
            # which case we fall back to a default location.
            if logfile == '':
                logfile = os.path.join(cfg.default_logfile_folder,
                                       f'defaultlog{file_extension}')
            # If a logfile was provided, but it did not have a proper
            # extension, we add a `.csv` extension.
            else:
                if os.path.splitext(logfile)[1].lower() not in \
                        self.valid_logfile_extensions:
                    logfile += file_extension
        # If the logfile is not writable, inform the user and cancel.
        try:
            open(logfile, 'w').close()
            os.remove(logfile)
        except Exception:
            self.main_window.notify(
                _(
                    "The logfile '%s' is not writable. Please choose "
                    "another location for the logfile."
                ) % logfile
            )
            return None
        if remember_logfile:
            # Remember the logfile folder for the next run
            cfg.default_logfile_folder = os.path.dirname(logfile)
        return logfile

    def get_subject_nr(self, quick=False):
        """Gets the subject number for the current session, either by falling 
        back to a default value of 999 (in quickmode) or through a pop-up 
        dialogue.

        Parameters
        ----------
        quick : bool, optional
            A boolean to indicate whether default should be used for the
            log-file and subject number. Mostly useful while testing the
            experiment.

        Returns
        -------
        int or None
            A subject number or None if no subject number was chosen (i.e. the
            dialogue was cancelled).
        """
        if quick:
            return 999
        subject_nr, ok = QtWidgets.QInputDialog.getInt(
            self.main_window.ui.centralwidget,
            _('Subject number'),
            _('Please enter the subject number'),
            min=0
        )
        if not ok:
            return None
        return subject_nr

    def init_experiment(self, quick=False, fullscreen=False):
        """Initializes a new experiment, which is a newly generated instance of
        the experiment currently active in the user interface.
        
        Parameters
        ----------
        quick : bool, optional
            A boolean to indicate whether default should be used for the
            log-file and subject number. Mostly useful while testing the
            experiment.
        fullscreen : bool, optional
            A boolean to indicate whether the window should be fullscreen.

        Returns
        -------
        bool
            True if the experiment was successfully initiated, False it was
            not.
        """
        # First tell the experiment to get ready, to apply any pending changes,
        # and then initialize the script. This can trigger errors.
        try:
            script = self.main_window.experiment.to_string()
        except Exception as e:
            md = _(
                '# Error\n\nFailed to generate experiment for the '
                'following reason:\n\n- '
            ) + e.markdown()
            self.console.write(e)
            self.tabwidget.open_markdown(md)
            return False
        # Get and set the subject number
        subject_nr = self.get_subject_nr(quick=quick)
        if subject_nr is None:
            return False
        # Get and set the logfile
        logfile = self.get_logfile(quick=quick, subject_nr=subject_nr)
        if logfile is None:
            return False
        # The experiment can be either the full path to the experiment file,
        # the folder of the experiment file, or None.
        if self.main_window.experiment.experiment_path is not None:
            experiment_path = self.main_window.experiment.experiment_path
            if self.main_window.current_path is not None:
                experiment_path = os.path.join(
                    experiment_path,
                    self.main_window.current_path
                )
        else:
            experiment_path = None
        # Build a new experiment. This can trigger a script error.
        try:
            self.experiment = Experiment(
                string=script,
                pool_folder=self.main_window.experiment.pool.folder(),
                experiment_path=experiment_path,
                fullscreen=fullscreen,
                subject_nr=subject_nr,
                logfile=logfile
            )
        except Exception as e:
            md = _('# Error\n\nFailed to parse experiment for the '
                   'following reason:\n\n- ') + safe_str(e)
            self.console.write(e)
            traceback.print_exc()
            self.tabwidget.open_markdown(md)
            return False
        return True

    def run(self, fullscreen=False, quick=False):
        """Runs the experiment.

        Parameters
        ----------
        fullscreen : bool, optional
            A boolean to indicate whether the window should be fullscreen.
        quick : bool, optional
            A boolean to indicate whether default should be used for the
            log-file and subject number. Mostly useful while testing the
            experiment.
        """
        self.main_window.set_run_status('running')
        self.main_window.extension_manager.fire(
            'run_experiment',
            fullscreen=fullscreen
        )
        if not self.init_experiment(quick=quick, fullscreen=fullscreen):
            self.main_window.extension_manager.fire('run_experiment_canceled')
            return
        ret_val = self.execute()
        # PsychoPy deletes the _ built-in
        if '_' not in __builtins__:
            oslogger.warning('re-installing missing gettext built-in')
            import gettext
            gettext.NullTranslations().install()
        self.main_window.set_run_status('finished')
        self.main_window.extension_manager.fire(
            'set_workspace_globals',
            global_dict=self.workspace_globals()
        )
        self.main_window.extension_manager.fire(
            'end_experiment',
            ret_val=ret_val
        )
        if ret_val is None:
            self.main_window.extension_manager.fire(
                'process_data_files',
                data_files=self.data_files()
            )

    def kill(self):
        """Kills an experiment, if the runner supports it."""
        pass

    def workspace_globals(self):
        r"""Returns the experiment's globals dictionary as it was when the
        experiment finished.

        Returns
        -------
        dict
            A globals dictionary.
        """
        return {}

    def data_files(self):

        return self.workspace_globals().get('data_files', [])

    def pause(self):
        r"""Is called when the experiment is paused."""
        self.console.set_workspace_globals(self.workspace_globals())
        print(
            'The experiment has been paused. Switch back to the experiment '
            'window and press space to resume.'
        )
        self.console.show_prompt()
        self.main_window.set_run_status('paused')
        self.main_window.extension_manager.fire('pause_experiment')
        self.paused = True

    def resume(self):
        r"""Is called when the experiment is resumed/ unpaused."""
        self.paused = False
        self.main_window.set_run_status('running')
        self.main_window.extension_manager.fire('resume_experiment')

    @staticmethod
    def has_heartbeat():
        r"""Gives True if the runner supports heartbeats, which are used to
        update the variable inspector, and False otherwise.
        """
        return False
