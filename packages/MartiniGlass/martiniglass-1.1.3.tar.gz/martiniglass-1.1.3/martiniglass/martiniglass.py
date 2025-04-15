#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


import argparse
from argparse import ArgumentDefaultsHelpFormatter
from martiniglass import system_reading, index_writing, molecule_editor, topol_writing, cylinders, output_file_append
from martiniglass import DATA_PATH
import os
from pathlib import Path
import shutil

def main():

    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", dest="topology", type=Path, help="input .top file used", default="topol.top")
    parser.add_argument("-f", dest="system", type=Path,
                        help=("Gromacs .gro file for which to write a non-water index file. "
                              "Equivalent to an index group of !W in gmx make_ndx. "
                              "Giving this option will automatically exclude W from your output vis.top")
                        )
    parser.add_argument("-traj", dest="trajectory", type=Path,
                        help=("Gromacs trajectory file to add to the visualisation state file.")
                        )
    parser.add_argument("-vs", default=True, action="store_false", dest='virtual_sites',
                        help=("Don't write bonds between virtual sites and their constructing atoms. "
                              " (Bonds are written by default. Specify this flag if you don't want them written.)")
                        )
    parser.add_argument("-el", default=False,
                        action="store_true", dest='elastic',
                        help="Write elastic network of input proteins to separate files"
                        )
    parser.add_argument("-go", default=False, action="store_true", dest='go',
                        help="Go network options")
    parser.add_argument("-gf", type=Path, dest='go_path', default='go_nbparams.itp',
                        help="Nonbonded parameter itp file for your go network")
    parser.add_argument("-vf", default=False, action="store_true",
                        help="Write out associated Visualisation Files (cg_bonds, vis.vmd) in the present directory")
    parser.add_argument("-pf", default=False, action="store_true",
                        help=("Write out the Protein File (protein.vmd) "
                             "for varying the bead size in proteins in addition to vis.vmd"))
    parser.add_argument("-ext", default=False, action="store_true",
                        help="Write system bonds to text files instead of topology files. Useful for non-VMD visualisation.")
    parser.add_argument("-cyl", default=False, action="store_true",
                        help="Write a tcl script to write out all network bonds for static images")

    args = parser.parse_args()

    if (args.cyl) and (args.system is None):
        raise ValueError("If you want a cylinder drawing tcl file"
                         " you must also give the coordinate file")

    if args.cyl:
        args.elastic = True

    ff, topol_lines, system_defines = system_reading(args.topology)

    written_mols, mol_bonds, mol_lens = molecule_editor(ff, topol_lines,
                                                        virtual_sites=args.virtual_sites,
                                                        ext=args.ext,
                                                        elastic=args.elastic,
                                                        go=args.go,
                                                        go_nb_file=args.go_path)

    if args.elastic:
        topol_writing(topol_lines, written_mols, 'en', w_include=args.system)
    if args.go:
        topol_writing(topol_lines, written_mols, 'go', w_include=args.system)
    topol_writing(topol_lines, written_mols, w_include=args.system)

    if args.system is not None:
        index_writing(args.system)
        if args.cyl:
            cylinders(args.system, topol_lines, mol_bonds, mol_lens)

    if args.vf:
        for file in os.listdir(DATA_PATH):
            if os.path.isfile(os.path.join(DATA_PATH, file)):
                if file == 'proteins.vmd' and not args.pf:
                    continue
                shutil.copy(os.path.join(DATA_PATH, file),
                            os.path.join(os.getcwd(), file))

        if args.elastic:
            if args.cyl:
                output_file_append(args.system, args.trajectory, args.pf, cylinders=True)
            else:
                output_file_append(args.system, args.trajectory, args.pf, elastic=True)
        if args.go:
            output_file_append(args.system, args.trajectory, args.pf, go=True)

    print('All done!')
    print("Please cite: Brasnett, C; Marrink, S J; J. Chem. Inf. Model. 2025, 65, 7, 3137–3141; 10.1021/acs.jcim.4c02277")

if __name__ == '__main__':
    main()
