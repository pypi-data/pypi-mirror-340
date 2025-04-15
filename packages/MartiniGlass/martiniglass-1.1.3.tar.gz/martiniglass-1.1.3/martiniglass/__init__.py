# Copyright 2024 University of Groningen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Find the data directory once.
try:
    from importlib.resources import files, as_file
    import atexit
    from contextlib import ExitStack
except ImportError:
    from pathlib import Path
    DATA_PATH = Path(__file__).parent / 'data'
    del Path
else:
    ref_data = files('martiniglass') / 'data'
    file_manager = ExitStack()
    atexit.register(file_manager.close)
    DATA_PATH = file_manager.enter_context(as_file(ref_data))

    del files, as_file, atexit, ExitStack

from .src.system_reading import system_reading
from .src.index_writer import index_writing
from .src.molecule_editing import molecule_editor
from .src.topology import topol_writing
from .src.cylinders_tcl import file_write as cylinders
from .src.output_file_append import output_file_append

from martiniglass.martiniglass import main