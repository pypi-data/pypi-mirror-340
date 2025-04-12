__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2025"
__license__ = "MIT"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import numpy as np
import pandas as pd
from rdkit import Chem
from Bio import SeqIO
from drutai.util import Biochar
from drutai.util.Console import Console


def fasta(fasta_fpn):
    sequence = []
    for seq in SeqIO.parse(fasta_fpn, "fasta"):
        # print(seq.seq)
        sequence.append(str(seq.seq))
    sequence = ''.join(sequence)
    if sequence == '':
        print('The sequence is empty.')
    return sequence


def fetch(
        br_fpn,
        smile_fpn,
        fasta_fp,
        verbose=True,
):
    console = Console()
    console.verbose = verbose

    df_br = pd.read_csv(
        br_fpn,
        sep='\t',
        header=0,
    )
    console.print("small-molecule and target relations:\n{}".format(df_br))
    num_samples = df_br.shape[0]
    df_smile = pd.read_csv(
        smile_fpn,
        sep='\t',
        header=0,
    )
    console.print("small-molecule smile map:\n{}".format(df_smile))
    dict_smile = pd.Series(df_smile['smile'].values, index=df_smile['sm'].values).to_dict()
    # console.print(dict_smile)

    v = [[] for _ in range(num_samples)]
    for i in range(num_samples):
        aseq = fasta(fasta_fpn=fasta_fp + df_br.loc[i, 'target'] + '.fasta')

        cprot_ = Biochar.cprot(aseq)
        v[i] += list(cprot_.values())

        dprot_ = Biochar.dprot(aseq)
        for j in range(400):
            v[i].append(np.float32(dprot_[j][1]))

        tprot_ = Biochar.tprot(aseq)
        for j in range(8000):
            v[i].append(np.float32(tprot_[j][1]))

        ctd_ = Biochar.pyp(aseq)
        ctd_values = ctd_.values()
        for val in ctd_values:
            v[i].append(np.float32(val))


        mol = Chem.MolFromSmiles(dict_smile[df_br.loc[i, 'sm']])
        # print(mol)

        pc195 = Biochar.dsi(mol)
        for _, e in enumerate(pc195):
            v[i].append(np.float32(e))

        pc2 = Biochar.crippen(mol)
        for _, e in enumerate(pc2):
            v[i].append(np.float32(e))

        fp_morgan = Biochar.fp1(mol)
        for _, e in enumerate(fp_morgan):
            v[i].append(int(e))

        fp_torsion = Biochar.fp2(mol)
        for _, e in enumerate(fp_torsion):
            v[i].append(int(e))
    v = np.array(v)
    return v[:, 0: 11664].astype(np.float32)