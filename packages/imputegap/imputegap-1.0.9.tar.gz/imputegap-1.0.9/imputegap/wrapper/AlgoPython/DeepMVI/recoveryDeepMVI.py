#!/usr/bin/python
import numpy as np

from imputegap.wrapper.AlgoPython.DeepMVI.transformer import transformer_recovery

def recover_matrix(matrix, max_epoch=1000, patience=2, lr=1e-3, verbose=True):
    temp = transformer_recovery(matrix, max_epoch, patience, lr, verbose)
    return temp

# end function


def deep_mvi_recovery(input, max_epoch=1000, patience=2, lr=1e-3, verbose=True):

    if verbose:
        print("(IMPUTATION) DEEP MVI: Matrix Shape: (", input.shape[0], ", ", input.shape[1], ") "
                "for max_epoch ", max_epoch, ", patience ", patience, ", lr ", lr, "...")

    # read input matrix
    matrix = input
    
    matrix_imputed = recover_matrix(matrix, max_epoch, patience, lr, verbose)

    if matrix_imputed is None:
        print("\n(ERR) DeepMVI has failed with the current configuration, please update the missing data rate or the missingness pattern.\n")
        return input
    
    # verification
    nan_mask = np.isnan(matrix_imputed)
    matrix_imputed[nan_mask] = np.sqrt(np.finfo('d').max / 100000.0)

    return matrix_imputed
    # end if

# end function