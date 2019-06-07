# getResidueNumbers

## Usage
```
usage: getResidueNumbers [-h] [-v] [-n N] [-p PIVOT_RESIDUE] [-s SEQCOL]
                         [-i IDCOL] [-o OFNAME]
                         fasta_file input_file

positional arguments:
  fasta_file            File to look up peptide sequences.
  input_file            File with peptide sequences.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -n N                  Number of flanking residues in output.
  -p PIVOT_RESIDUE, --pivot_residue PIVOT_RESIDUE
                        Amino acid to put in center of sequence logos. 'C' is
                        the default.
  -s SEQCOL, --seqCol SEQCOL
                        Sequence column name. 'sequence' is the default
  -i IDCOL, --idCol IDCOL
                        ID column name. 'ipi' is the default.
  -o OFNAME, --ofname OFNAME
                        Output file name.
```
