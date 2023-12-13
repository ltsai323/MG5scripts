#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class FileWithDesc:
    file:str
    desc:str
def Get(the_input:FileWithDesc): return (the_input.file,the_input.desc)

## generatedsample_bcOnly
# mcPredictedC_intrinsicC_0118_nf5        = FileWithDesc( desc='5NFS intrinsic charm',
#         file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv')
# mcPredictedC_intrinsicC_0118_nf4        = FileWithDesc( desc='4NFS intrinsic charm',
#         file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_c.csv')
# mcPredictedC_perturbativeC_0118_nf5     = FileWithDesc( desc='5NFS perturbative charm',
#         file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_c.csv')
# mcPredictedC_perturbativeC_0118_nf4     = FileWithDesc( desc='4NFS perturbative charm',
#         file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_c.csv')
# mcPredictedB_intrinsicC_0118_nf5        = FileWithDesc( desc='5NFS intrinsic charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_b.csv')
# mcPredictedB_intrinsicC_0118_nf4        = FileWithDesc( desc='4NFS intrinsic charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_b.csv')
# mcPredictedB_perturbativeC_0118_nf5        = FileWithDesc( desc='5NFS perturbative charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_b.csv')
# mcPredictedB_perturbativeC_0118_nf4        = FileWithDesc( desc='4NFS perturbative charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_b.csv')
# 
# mcLeadingC_intrinsicC_0118_nf5        = FileWithDesc( desc='5NFS intrinsic charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_c.csv')
# mcLeadingC_intrinsicC_0118_nf4        = FileWithDesc( desc='4NFS intrinsic charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv')
# mcLeadingC_perturbativeC_0118_nf5     = FileWithDesc( desc='5NFS perturbative charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_c.csv')
# mcLeadingC_perturbativeC_0118_nf4     = FileWithDesc( desc='4NFS perturbative charm',
#             file='generatedsample_bcOnly/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv')
# 
# mcLeadingB_intrinsicC_0118_nf5        = FileWithDesc( desc='5NFS intrinsic charm',
#             file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_b.csv',
# mcLeadingB_intrinsicC_0118_nf4        = FileWithDesc( desc='4NFS intrinsic charm',
#             file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_leading_b.csv',
# mcLeadingB_perturbativeC_0118_nf5     = FileWithDesc( desc='5NFS perturbative charm',
#             file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_b.csv',
# mcLeadingB_perturbativeC_0118_nf4     = FileWithDesc( desc='4NFS perturbative charm',
#             file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_leading_b.csv',


mcPredictedC_intrinsicC_0118_nf5        = FileWithDesc( desc='5NFS intrinsic charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv')
mcPredictedC_perturbativeC_0118_nf5     = FileWithDesc( desc='5NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_c.csv')
mcPredictedC_perturbativeC_0118_nf3     = FileWithDesc( desc='3NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_3/MG5result_mcPredicted_c.csv')

mcPredictedB_intrinsicC_0118_nf5        = FileWithDesc( desc='5NFS intrinsic charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_b.csv')
mcPredictedB_perturbativeC_0118_nf5     = FileWithDesc( desc='5NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_b.csv')
mcPredictedB_perturbativeC_0118_nf3     = FileWithDesc( desc='3NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_3/MG5result_mcPredicted_b.csv')


mcLeadingC_intrinsicC_0118_nf5        = FileWithDesc( desc='5NFS intrinsic charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_c.csv')
mcLeadingC_perturbativeC_0118_nf5     = FileWithDesc( desc='5NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_c.csv')
mcLeadingC_perturbativeC_0118_nf3     = FileWithDesc( desc='3NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_3/MG5result_mcPredicted_leading_c.csv')

mcLeadingB_intrinsicC_0118_nf5          = FileWithDesc( desc='5NFS intrinsic charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_b.csv')
mcLeadingB_perturbativeC_0118_nf5       = FileWithDesc( desc='5NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_b.csv')
mcLeadingB_perturbativeC_0118_nf3       = FileWithDesc( desc='3NFS perturbative charm',
        file='gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_3/MG5result_mcPredicted_leading_b.csv')
