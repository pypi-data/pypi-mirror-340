


"""
Shows the violint plots, disentanglment across a range of different count values.
"""

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tqdm.autonotebook import tqdm


def func_eqeq(a, b):
    return a==b

def func_biggerthaneq(a, b):
    return a >= b

def vis(
    adata_unnorm,
    pred_Xspl_rownormcorrected,
    min_cnt_vertical_slice,
    max_cnt_vertical_slice,
    list_LR,
    path_dump,
    str_sampleID,
    str_batchID,
    idx_slplus1
):
    """
    :param adata_unnorm:
    :param pred_Xspl_rownormcorrected:
    :param list_LR: the list of genes found both in the LR databse and the gene pannel.
    :param fname_dump_red:
    :param fname_dump_blue
    :return:
    """

    assert adata_unnorm.shape[0] == pred_Xspl_rownormcorrected.shape[0]
    assert adata_unnorm.shape[1] == pred_Xspl_rownormcorrected.shape[1]

    for g in list_LR:
        assert g in adata_unnorm.var.index.tolist()

    list_geneindex_inLR = [
        adata_unnorm.var.index.tolist().index(g) for g in list_LR
    ]
    list_geneindex_inLR.sort()

    for cnt_vertical_slice in tqdm(range(min_cnt_vertical_slice, max_cnt_vertical_slice), desc="Creating violin plots for tissue {}".format(idx_slplus1)):

        for nameop, op_eqorbiggerthaneq, func_operator in zip(['eq', 'biggerthaneq'], ['==', '>='], [func_eqeq, func_biggerthaneq]):

            mask_inLR = func_operator(adata_unnorm.X.toarray()[:, list_geneindex_inLR], cnt_vertical_slice)

            mask_notinLR = func_operator(adata_unnorm.X.toarray()[:, list(set(range(adata_unnorm.shape[1])) - set(list_geneindex_inLR))], cnt_vertical_slice)

            mask_all = func_operator(adata_unnorm.X.toarray(), cnt_vertical_slice)


            slice_pred_inLR = pred_Xspl_rownormcorrected[:, list_geneindex_inLR][mask_inLR].flatten()
            slice_pred_notinLR = pred_Xspl_rownormcorrected[:, list(set(range(adata_unnorm.shape[1])) - set(list_geneindex_inLR))][mask_notinLR].flatten()

            plt.figure()
            sns.violinplot(
                data={
                    'not in LR-DB': slice_pred_notinLR / ((cnt_vertical_slice + 0.0) if(op_eqorbiggerthaneq == '==') else adata_unnorm.X.toarray()[:, list(set(range(adata_unnorm.shape[1])) - set(list_geneindex_inLR))][mask_notinLR].flatten()),
                    'in LR-DB': slice_pred_inLR / ((cnt_vertical_slice + 0.0) if(op_eqorbiggerthaneq == '==') else adata_unnorm.X.toarray()[:, list_geneindex_inLR][mask_inLR].flatten()),
                },
                cut=0
            )
            plt.title(
                "sample: {} \n in biological batch {} \n among readout counts{}{} \n {}".format(
                    str_sampleID,
                    str_batchID,
                    op_eqorbiggerthaneq,
                    cnt_vertical_slice,
                    "read counts not in & in LR-DB are {} and {} respectively".format(
                        slice_pred_notinLR.shape[0],
                        slice_pred_inLR.shape[0]
                    )
                )
            )
            plt.savefig(
                os.path.join(
                    path_dump,
                    'readcount_{}_{}.png'.format(nameop, cnt_vertical_slice)
                ),
                bbox_inches='tight',
                pad_inches=0
            )
            plt.close()

        # plt.show()



