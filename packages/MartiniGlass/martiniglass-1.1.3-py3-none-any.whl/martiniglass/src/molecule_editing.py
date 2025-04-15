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

import copy
from os.path import isfile
from vermouth.gmx import write_molecule_itp
from .network_writer import network_writer
from vermouth.graph_utils import make_residue_graph

def molecule_editor(ff, topol_lines,
                    virtual_sites=True, ext=False,
                    elastic=False,
                    go=False, go_nb_file=''):
    # iterate over the molecules to make visualisation topologies
    keep = ['bonds', 'constraints', 'pairs', 'virtual_sitesn',
            'virtual_sites2', 'virtual_sites3']
    print("Writing visualisable topology files")

    written_mols = []
    mol_bonds = {}
    mol_lens = {}

    for molname, block in ff.blocks.items():
        # write vis topols for molecules we're actually interested in
        try:
            assert molname in [i['name'] for i in topol_lines['molecules']]
        except AssertionError:
            continue

        bonds_list = []
        # delete the interactions which are not bonds
        for interaction_type in list(block.interactions):
            if interaction_type not in keep:
                del block.interactions[interaction_type]

        # remove meta (i.e. the #IFDEF FLEXIBLE) from the bonds
        for bond in block.interactions['bonds']:
            bond.meta.clear()
        if elastic:

            res_graph = make_residue_graph(block)
            res_dict = {}
            for node in res_graph.nodes:
                for bead in res_graph.nodes[node]['graph'].nodes:
                    res_dict[bead] = node

            for bond in list(block.interactions['bonds']):
                # this should introduce actual parameters into the block if the bonds have been given by
                # a #define statement elsewhere
                if len(bond.parameters) < 3:
                    atoms = bond.atoms
                    # paras = bond.parameters[0]
                    block.remove_interaction('bonds', bond.atoms)
                    # strictly the interaction here should be system_defines[paras], but it doesn't matter
                    block.add_interaction('bonds', atoms, ['1', '1', '1000'],
                                          meta={"comment": "external bond definition"})
                    continue

                else:
                    at1 = bond.atoms[0]
                    at2 = bond.atoms[1]
                    if abs(res_dict[at1] - res_dict[at2]) > 1:
                        bonds_list.append([bond.atoms[0], bond.atoms[1]])
                        block.remove_interaction('bonds', bond.atoms)

            ff_en_copy = copy.deepcopy(ff)
            en_written = network_writer(ff_en_copy, molname, bonds_list, ext, 'en')
            written_mols.append(en_written)

        # this should then keep any constraints which don't have IFDEF statements
        # e.g. alpha helices are described by constraints without these.
        # however, the remove_interactions function doesn't work atm.
        for bond in list(block.interactions['constraints']):
            if bond.meta.get('ifndef'):
                block.remove_interaction('constraints', bond.atoms)
            else:
                block.add_interaction('bonds', bond.atoms, bond.parameters + ['10000'])
                block.remove_interaction('constraints', bond.atoms)

        # rewrite pairs as bonds for visualisation
        for bond in block.interactions['pairs']:
            block.add_interaction('bonds', bond.atoms, bond.parameters[:2] + ['10000'])
        del block.interactions['pairs']

        # make bonds between virtual sites and each of the constructing atoms
        go_dict = {}
        for vs_type in ['virtual_sitesn', 'virtual_sites2', 'virtual_sites3']:
            if virtual_sites:
                for vs in block.interactions[vs_type]:
                    site = vs.atoms[0]
                    constructors = vs.atoms[1:]
                    # this avoids pointless bonds between a virtual site directly on top of
                    # its singular constructing atom
                    block.nodes[site]['mass'] = 1
                    if go:
                        # make a dictionary of atype: node index
                        # this is for later so the 'bond' can be drawn properly.
                        # assert that this site has the name CA to check it's a go site and not another VS.
                        aname = block.nodes[site]['atomname']
                        atype = block.nodes[site]['atype']
                        if (aname.split('_')[0] == 'molecule') or (aname == 'CA'):
                            go_dict[atype] = site
                    else:
                        for constructor in constructors:
                            # completely arbitrary parameters, the bond just needs to exist
                            block.add_interaction('bonds', [site, constructor],
                                                  ['1', '1', '1000'], meta={"comment": "bonded virtual site"})
            if block.interactions[vs_type]:
                del block.interactions[vs_type]

        if go:

            if not isfile(go_nb_file):
                raise FileNotFoundError("Gō nonbonded itp does not exist. Specify using -gf")

            with open(go_nb_file, "r") as f:
                nb_lines = f.readlines()
            nb_lines = [line.split(';')[0].split(' ') for line in nb_lines if '[' not in line]
            # TODO this causes problems when we're not actually in the correct block that's
            # associated with the go model! ignore the exception for now.
            try:
                for i in nb_lines:
                    try:
                        assert i[0] in go_dict
                        assert i[1] in go_dict
                        bonds_list.append([go_dict[i[0]], go_dict[i[1]]])  # , '1', i[3], '1000'])
                    except AssertionError:
                        pass
            except KeyError:
                pass
            ff_go_copy = copy.deepcopy(ff)
            go_written = network_writer(ff_go_copy, molname, bonds_list, ext, "go")
            written_mols.append(go_written)

        # write out the molecule with an amended name
        mol_out = block.to_molecule()
        mol_out.meta['moltype'] = molname + '_vis'

        if ext:

            ext_bonds_list = [i.atoms for i in mol_out.interactions['bonds']]
            stout = ''.join([f'{i[0]}\t{i[1]}\n' for i in ext_bonds_list])
            with open(f'{molname}_bonds.txt', 'w') as bonds_list_out:
                bonds_list_out.write(stout)

        header = [f'Visualisation topology for {molname}', 'NOT FOR SIMULATIONS']

        with open(molname + '_vis.itp', 'w') as fout:
            write_molecule_itp(mol_out, outfile=fout, header=header)
            written_mols.append(fout.name)

        mol_bonds[molname] = bonds_list
        mol_lens[molname] = len(block.nodes)

    return written_mols, mol_bonds, mol_lens
