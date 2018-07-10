
import argparse
import pandas as pd
import os
import sys
import re

import fastaFile

PROG_VERSION = "1.0"
DEFAULT_PIVOT = 'C'
DEFAULT_ID_COL = 'ipi'
DEFAULT_SEQ_COL = 'sequence'

def main(argv):

    #setup args and parse
    parser = argparse.ArgumentParser(prog = 'getResidueNumbers',
                            epilog="parseCimage was written by Aaron Maurais.\n"
                                   "Email questions or bugs to aaron.maurais@bc.edu")

    parser.add_argument("--version", action='version', version='%(prog)s ' + PROG_VERSION)

    parser.add_argument('fasta_file',
                        help = 'File to look up peptide sequences.')

    parser.add_argument('input_file',
                        help = "File with peptide sequences.")

    parser.add_argument('-n',
                        help = 'Number of flanking residues in output.',
                        type = int,
                        default = 5)

    parser.add_argument('-p', '--pivot_residue',
                        help = 'Amino acid to put in center of sequence logos. \'{}\' is the default.'.format(DEFAULT_PIVOT),
                        type = str,
                        default = DEFAULT_PIVOT)

    parser.add_argument('-seqCol',
                        help = 'Sequence column name. \'{}\' is the default'.format(DEFAULT_SEQ_COL),
                        default = DEFAULT_SEQ_COL)

    parser.add_argument('-idCol',
                        help = 'ID column name. \'{}\' is the default.'.format(DEFAULT_ID_COL),
                        default= DEFAULT_ID_COL)

    parser.add_argument('-o', '--ofname',
                        help = 'Output file name.',
                        default = 'peptideSpans.tsv')

    args = parser.parse_args()

    #check args
    pivotResidue = args.pivot_residue
    if len(pivotResidue) != 1:
        sys.stderr.write('{} is not a valid pivot residue\n'.format(pivotResidue))
        exit()

    #read fasta file
    sys.stdout.write('Reading fasta file...')
    fastaFileFname = os.path.realpath(args.fasta_file)
    try:
        sequences = fastaFile.FastaFile(fastaFileFname)
    except Exception as e:
        sys.stderr.write('Error reading fasta file: {}\n'.format(e))
        exit()
    else: sys.stdout.write(' Done!\n')

    #read input table
    sys.stdout.write('Reading input file...')
    inputTableFname = os.path.realpath(args.input_file)
    try:
        inputTable = pd.read_csv(inputTableFname, sep = '\t')
        inputTable.dropna()
        inputTableColnames = inputTable.columns.values.tolist()
    except Exception as e:
        sys.stderr.write('Error reading input_file: {}\n'.format(e))
        exit()
    else: sys.stdout.write(' Done!\n')

    #check that required cols are in input table
    if not (args.idCol in inputTableColnames and args.seqCol in inputTableColnames):
        sys.stderr.write('{} or {} not found in {}.\n'.format(args.idCol, args.seqCol, args.input_file))
        exit()

    #set up lists to work with
    idList = inputTable[args.idCol].tolist()
    seqList = [re.sub('\*', '', x) for x in inputTable[args.seqCol].tolist()]

    #remove all * characters from input table sequence col and preserve original seq
    inputTable['original_sequence'] = inputTable[args.seqCol]
    inputTable[args.seqCol] = seqList

    #new lists to append data from each residue
    newIdList = list()
    newSeqList = list()
    newResidueList = list()
    newSpanList = list()

    sys.stdout.write('Parseing peptide list...')
    nl = True
    #itterate through each peptide in peptideList
    for i in range(0, len(idList)):
        #get list of pivot residue indecies in current sequence
        pivotList = [j for j, x in enumerate(seqList[j]) if x == pivotResidue]

        #continue if no pivotResude found
        if len(pivotList) == 0:
            if nl:
                sys.stdout.write('\n')
                nl = False
            sys.stdout.write("{} not found in sequence: {}. Skipping peptide...".format(pivotResidue, seqList[i]))
            continue
		
        #get protien sequence
        try:
            protSeq = sequences.getSequence(idList[i])
        except RuntimeError as e:
            sys.stderr.write('\n{}\nSkipping {}...\n'.format(e, idList[i]))
            continue

        begin = protSeq.find(seqList[i])
        end = begin + len(seqList[i])

        #itterate through each pivot residue in peptideList
        for residue in pivotList:
            residueNumber = begin + residue
            fragBegin = residueNumber - args.n
            if fragBegin < 0:
                fragBegin = 0
            span = protSeq[fragBegin:(residueNumber + args.n + 1)]

            #append row data to new lists
            newIdList.append(idList[i])
            newSeqList.append(seqList[i])
            newResidueList.append('{}{}'.format(pivotResidue, residueNumber + 1))
            newSpanList.append(span)

    #make new dataframe to join to input
    cysteines = pd.DataFrame({args.idCol : newIdList,
                              args.seqCol : newSeqList,
                              'residue' : newResidueList,
                              'span' : newSpanList})

    #prepare dataframe for export
    cysteines = cysteines.merge(inputTable, on = [args.idCol, args.seqCol], how = 'left')
    colOrder = inputTableColnames
    colOrder.append('residue')
    colOrder.append('span')
    cysteines = cysteines[colOrder]

    sys.stdout.write(' Done!\n')

    #export dataframe
    ofname = os.path.realpath(args.ofname)
    try:
        cysteines.to_csv(path_or_buf = ofname, sep = '\t', index = False)
    except Exception as e:
        sys.stderr.write('Error writing {}: {}\n'.format(ofname, e))
        exit()
    else:
        sys.stdout.write('Data written to {}\n'.format(ofname))

if __name__ == "__main__":
    main(sys.argv)

