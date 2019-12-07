from IPython.core.magic import cell_magic, magics_class, Magics
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)

from htools import timebox, TimeExceededError


@magics_class
class TimeboxMagic(Magics):

    @cell_magic
    @magic_arguments()
    @argument('-t', type=int,
              help='Max number of seconds before throwing error.')
    @argument('-p', action='store_true',
              help='Boolean flag: if provided, use permissive '
                   'execution (if the cell exceeds the specified '
                   'time, no error will be thrown, meaning '
                   'following cells can still execute.) If '
                   'flag is not provided, default behavior is to '
                   'raise a TimeExceededError and halt notebook '
                   'execution.')
    def timebox(self, line=None, cell=None):
        args = parse_argstring(self.timebox, line)
        with timebox(args.t) as tb:
            if args.p:
                cell = self._make_cell_permissive(cell)
            get_ipython().run_cell(cell)

    @staticmethod
    def _make_cell_permissive(cell):
        robust_cell = (
            'try:\n\t' + cell.replace('\n', '\n\t')
            + '\nexcept:\n\tprint("Time exceeded. '
            '\\nWARNING: Mutable objects may have changed during execution.")'
        )
        return robust_cell


get_ipython().register_magics(TimeboxMagic)
