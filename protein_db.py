
import os
import re
import numpy as np
import markdown_to_json
from markdown_to_json.vendor.docopt import docopt
from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
import json
import subprocess as sp

def shell(cmd, shell=False):

    if shell:
        p = sp.Popen(cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    else:
        cmd = cmd.split()
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

    output, err = p.communicate()
    return output

def get_coordinates_xyz(filename):
    """
    Get coordinates from filename and return a vectorset with all the
    coordinates, in XYZ format.

    Parameters
    ----------
    filename : string
        Filename to read

    Returns
    -------
    atoms : list
        List of atomic types
    V : array
        (N,3) where N is number of atoms

    """

    f = open(filename, 'r')
    V = list()
    atoms = list()
    n_atoms = 0

    # Read the first line to obtain the number of atoms to read
    try:
        n_atoms = int(f.readline())
    except ValueError:
        exit("Could not obtain the number of atoms in the .xyz file.")

    # Skip the title line
    f.readline()

    # Use the number of atoms to not read beyond the end of a file
    for lines_read, line in enumerate(f):

        if lines_read == n_atoms:
            break

        atom = re.findall(r'[a-zA-Z]+', line)[0]
        atom = atom.upper()

        numbers = re.findall(r'[-]?\d+\.\d*(?:[Ee][-\+]\d+)?', line)
        numbers = [float(number) for number in numbers]

        # The numbers are not valid unless we obtain exacly three
        if len(numbers) == 3:
            V.append(np.array(numbers))
            atoms.append(atom)
        else:
            exit("Reading the .xyz file failed in line {0}. Please check the format.".format(lines_read + 2))

    f.close()
    atoms = np.array(atoms)
    V = np.array(V)
    return atoms, V


def get_markdown_ast(markdown_file):
    f = open(markdown_file, 'r')
    return CommonMark.DocParser().parse(f.read())

nester = CMarkASTNester()
renderer = Renderer()

def md2json():
    ast = get_markdown_ast(filename)
    nested = nester.nest(ast)
    rendered = renderer.stringify_dict(nested)
    return json

def get_charge(filename):

    if not os.path.isfile(filename):
        filename = filename.replace("README", "readme")

    cmd = 'grep "Total charge on system is" '+filename
    out = shell(cmd, shell=True)

    if out == "":
        print "no charge"
        print cmd

    charge = out.split()
    charge = charge[-1]
    charge = int(charge)

    return charge

def get_models(foldername):
    csvfiles = [name.replace(".csv", "") for name in os.listdir(foldername) if "csv" in name]
    return csvfiles


def get_model_files(foldername, modelname):
    csvfiles = [name for name in os.listdir(foldername) if modelname in name and "xyz" in name]
    csvfiles = [name.replace(".xyz", "").replace(modelname + "_", "") for name in csvfiles]
    return csvfiles

def get_protein(pdbid, foldername="./proteins/"):

    if foldername[-1] != "/":
        foldername += "/"

    foldername += pdbid

    if not os.path.isdir(foldername):
        quit("not exists: " + foldername)

    db = {}

    charge = get_charge(foldername + "/README.md")
    db['charge'] = charge

    models = get_models(foldername)
    models.sort()
    db['models_keys'] = models

    db['models'] = {}
    for model in models:

        csvfile = open(foldername + "/" + model + ".csv", 'r')
        header = csvfile.next()
        header = [x.lower().strip() for x in header.split(",")]

        db['models'][model] = {}

        # TODO Energies?
        data = []
        for line in csvfile:
            line = line.strip()
            line = line.split(",")
            eps = line[0]
            data.append(line[-len(header[1:]):])

        data = np.array(data, dtype=float)

        for i, head in enumerate(header[1:]):

            filename = foldername + "/" + model + "_"+head+".xyz"

            energies = data[:,i]

            try:
                atoms, coordinates = get_coordinates_xyz(filename)
            except IOError:
                filename = filename.replace("c1", "")
                filename = filename.replace("c2", "")
                atoms, coordinates = get_coordinates_xyz(filename)

            db['models'][model][head] = {}
            db['models'][model][head]['atoms'] = atoms
            db['models'][model][head]['xyz'] = coordinates
            db['models'][model][head]['energies'] = energies


    return db

def get_all_pdbs(foldername):

    foldername += "/"
    folders = [name for name in os.listdir(foldername) if os.path.isdir(foldername + name)]

    return folders


def main():

    enzymes = get_all_pdbs('proteins')

    for enzyme in enzymes:

        print enzyme

        edb = get_protein(enzyme)

        # TODO Generate energy diagram

        quit()


    return



if __name__ == "__main__":
    main()


