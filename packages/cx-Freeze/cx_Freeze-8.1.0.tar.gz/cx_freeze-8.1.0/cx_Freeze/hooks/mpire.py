"""A collection of functions which are triggered automatically by finder when
mpire (a multiprocessing wrapper) package is included.
"""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def xload_mpire(finder: ModuleFinder, module: Module) -> None:
    """Inject freeze_support.
    """
    if module.file.suffix == ".pyc":  # source unavailable
        return
    source = r"""
    # cx_Freeze patch start
    from multiprocessing.spawn import freeze_support
    from multiprocessing.spawn import is_forking as _is_forking
    import sys as _sys
    if _is_forking(_sys.argv):
        _sys.exit()
    
    # cx_Freeze patch end
    """
    code_string = dedent(source) + module.file.read_text(encoding="utf_8")
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )


def xload_mpire_context(finder: ModuleFinder, module: Module) -> None:
    """Monkeypath get_context to do automatic freeze_support."""
    if module.file.suffix == ".pyc":  # source unavailable
        return
    source = rf"""
    # cx_Freeze patch start
    def _freeze_support(self):
        from {module.root.name}.spawn import freeze_support
        from {module.root.name}.spawn import is_forking
        import sys
        if is_forking(sys.argv):
            print(__name__, "_freeze_support", file=sys.stderr)
        freeze_support()
    BaseContext.freeze_support = _freeze_support
    BaseContext._get_base_context = BaseContext.get_context
    def _get_base_context(self, method=None):
        self.freeze_support()
        return self._get_base_context(method)
    BaseContext.get_context = _get_base_context
    DefaultContext._get_default_context = DefaultContext.get_context
    def _get_default_context(self, method=None):
        self.freeze_support()
        return self._get_default_context(method)
    DefaultContext.get_context = _get_default_context
    # cx_Freeze patch end
    """
    code_string = module.file.read_text(encoding="utf_8") + dedent(source)
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )
