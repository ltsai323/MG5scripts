#!/usr/bin/env python3

def PrintHelp():
    print('''

            Requirement : Current directory should be MG5 respository. Such that the executable should be found in ./bin/generate_events
            Usage :
              1. Creation mode : Create a run_card_blahblah.dat. Fully controlled by command.
                 - args: 1. pd label, 2. lha id 3. out label, 4. min pt cut on photon

              2. Default mode : Create a list of run_card_blahblah.dat for basic use.
                                  ('bin01', 30  ),
                                  ('bin02', 55  ),
                                  ('bin03', 100 ),
                                  ('bin04', 135 ),
                                  ('bin05', 175 ),
                                  ('bin06', 200 ),
                                  ('bin07', 220 ),
                                  ('bin08', 300 ),
                                  ('bin09', 400 ),
                                  ('bin10', 500 ),
                                  ('bin11', 700 ),
                  - args: 1. pd label.  2. lha id
              3. Test mode : Run default mode with default PDlabel 'NNPDF31_nlo_as_0118' and id '303400'
                  - args: NONE
                  ''')
    raise IOError('Invalid input argument')
run_card_template='''
#***********************************************************************
#                        MadGraph5_aMC@NLO                             *
#                                                                      *
#                      run_card.dat aMC@NLO                            *
#                                                                      *
#  This file is used to set the parameters of the run.                 *
#                                                                      *
#  Some notation/conventions:                                          *
#                                                                      *
#   Lines starting with a hash (#) are info or comments                *
#                                                                      *
#   mind the format:   value    = variable     ! comment               *
#                                                                      *
#   Some of the values of variables can be list. These can either be   *
#   comma or space separated.                                          *
#                                                                      *
#   To display additional parameter, you can use the command:          *
#      update to_full                                                  *
#***********************************************************************
#
#*******************                                                 
# Running parameters
#*******************                                                 
#
#***********************************************************************
# Tag name for the run (one word)                                      *
#***********************************************************************
  tag_1	= run_tag ! name of the run 
#***********************************************************************
# Number of LHE events (and their normalization) and the required      *
# (relative) accuracy on the Xsec.                                     *
# These values are ignored for fixed order runs                        *
#***********************************************************************
  {nEVENTs:d}	= nevents ! Number of unweighted events requested 
  -1.0	= req_acc ! Required accuracy (-1=auto determined from nevents)
  -1	= nevt_job ! Max number of events per job in event generation. 
                 !  (-1= no split).
#***********************************************************************
# Output format
#***********************************************************************
  -1.0	= time_of_flight ! threshold (in mm) below which the invariant livetime is not written (-1 means not written)
  average	= event_norm ! average/sum/bias. Normalization of the weight in the LHEF
#***********************************************************************
# Number of points per itegration channel (ignored for aMC@NLO runs)   *
#***********************************************************************
  0.01	= req_acc_fo ! Required accuracy (-1=ignored, and use the 
 	                   ! number of points and iter. below)
# These numbers are ignored except if req_acc_FO is equal to -1
  5000	= npoints_fo_grid ! number of points to setup grids
  4	= niters_fo_grid ! number of iter. to setup grids
  10000	= npoints_fo ! number of points to compute Xsec
  6	= niters_fo ! number of iter. to compute Xsec
#***********************************************************************
# Random number seed                                                   *
#***********************************************************************
  {iSEED:d}	= iseed ! rnd seed (0=assigned automatically=default))
#***********************************************************************
# Collider type and energy                                             *
#    0 = no PDF                                                        *
#    1/-1 = proton/antiproton                                          *
#    3/-3 = electron/positron with ISR/Beamstrahlung;                  * 
#    4/-4 = muon/antimuon with ISR/Beamstrahlung;                      * 
#***********************************************************************
  1	= lpp1 ! beam 1 type (0 = no PDF)
  1	= lpp2 ! beam 2 type (0 = no PDF)
  6500.0	= ebeam1 ! beam 1 energy in GeV
  6500.0	= ebeam2 ! beam 2 energy in GeV
#***********************************************************************
# PDF choice: this automatically fixes also alpha_s(MZ) and its evol.  *
#***********************************************************************
  lhapdf	= pdlabel ! PDF set
  {lhaID:d}     = lhaid ! If pdlabel=lhapdf, this is the lhapdf number. Only 
              ! numbers for central PDF sets are allowed. Can be a list; 
              ! PDF sets beyond the first are included via reweighting.
  0	= pdfscheme ! the scheme of the input PDFs. 0->MSbar; 1->DIS
	            ! 2->eta (leptonic); 3->beta (leptonic) 
		    ! 4->mixed (leptonic); 6->delta (leptonic)
                    ! if pdlabel==emela, this is set automatically
#***********************************************************************
# The following block is specific to lepton collisions (lpp=+-3)       *
#***********************************************************************
  True	= photons_from_lepton ! whether to include or not photons from 
                              ! lepton ISR
#***********************************************************************
# Include the NLO Monte Carlo subtr. terms for the following parton    *
# shower (HERWIG6 | HERWIGPP | PYTHIA6Q | PYTHIA6PT | PYTHIA8)         *
# WARNING: PYTHIA6PT works only for processes without FSR!!!!          *
#***********************************************************************
  HERWIG6	= parton_shower 
  1.0	= shower_scale_factor ! multiply default shower starting
                            ! scale by this factor
  False	= mcatnlo_delta ! use MC@NLO-Delta matching, arXiv:2002.12716
                        ! (only with Pythia8309 or later)
#***********************************************************************
# Renormalization and factorization scales                             *
# (Default functional form for the non-fixed scales is the sum of      *
# the transverse masses divided by two of all final state particles    * 
# and partons. This can be changed in SubProcesses/set_scales.f or via *
# dynamical_scale_choice option)                                       *
#***********************************************************************
  False	= fixed_ren_scale ! if .true. use fixed ren scale
  False	= fixed_fac_scale ! if .true. use fixed fac scale
  91.118	= mur_ref_fixed ! fixed ren reference scale 
  91.118	= muf_ref_fixed ! fixed fact reference scale
  -1	= dynamical_scale_choice ! Choose one (or more) of the predefined
           ! dynamical choices. Can be a list; scale choices beyond the
           ! first are included via reweighting
  1.0	= mur_over_ref ! ratio of current muR over reference muR
  1.0	= muf_over_ref ! ratio of current muF over reference muF
 
#*********************************************************************** 
# Reweight variables for scale dependence and PDF uncertainty          *
#***********************************************************************
  1.0, 2.0, 0.5	= rw_rscale ! muR factors to be included by reweighting
  1.0, 2.0, 0.5	= rw_fscale ! muF factors to be included by reweighting
  True	= reweight_scale ! Reweight to get scale variation using the 
            ! rw_rscale and rw_fscale factors. Should be a list of 
            ! booleans of equal length to dynamical_scale_choice to
            ! specify for which choice to include scale dependence.
  False	= reweight_pdf ! Reweight to get PDF uncertainty. Should be a
            ! list booleans of equal length to lhaid to specify for
            !  which PDF set to include the uncertainties.
#***********************************************************************
# Store reweight information in the LHE file for off-line model-       *
# parameter reweighting at NLO+PS accuracy                             *
#***********************************************************************
  False	= store_rwgt_info ! Store info for reweighting in LHE file
#***********************************************************************
#  Customization of the code. List of files containing user hook function 
#***********************************************************************
  	= custom_fcts ! List of files containing user hook function
#***********************************************************************
# ickkw parameter:                                                     *
#   0: No merging                                                      *
#   3: FxFx Merging - WARNING! Applies merging only at the hard-event  *
#      level. After showering an MLM-type merging should be applied as *
#      well. See http://amcatnlo.cern.ch/FxFx_merging.htm for details. *
#   4: UNLOPS merging (with pythia8 only). No interface from within    *
#      MG5_aMC available, but available in Pythia8.                    *
#  -1: NNLL+NLO jet-veto computation. See arxiv:1412.8408 [hep-ph].    *
#***********************************************************************
  0	= ickkw 
#***********************************************************************
#
#***********************************************************************
# BW cutoff (M+/-bwcutoff*Gamma). Determines which resonances are      *
# written in the LHE event file                                        *
#***********************************************************************
  15.0	= bwcutoff 
#***********************************************************************
# Cuts on the jets. Jet clustering is performed by FastJet.            *
#  - If gamma_is_j, photons are also clustered with jets.              *
#    Otherwise, they will be treated as tagged particles and photon    * 
#    isolation will be applied. Note that photons in the real emission *
#    will always be clustered with QCD partons.                        *
#  - When matching to a parton shower, these generation cuts should be *
#    considerably softer than the analysis cuts.                       *
#  - More specific cuts can be specified in SubProcesses/cuts.f        *
#***********************************************************************
  1.0	= jetalgo ! FastJet jet algorithm (1=kT, 0=C/A, -1=anti-kT)
  0.7	= jetradius ! The radius parameter for the jet algorithm
  {ptJ:.1f}	= ptj ! Min jet transverse momentum
  {etaJ:.1f} = etaj ! Max jet abs(pseudo-rap) (a value .lt.0 means no cut)
  False	= gamma_is_j ! Wether to cluster photons as jets or not
#***********************************************************************
# Cuts on the charged leptons (e+, e-, mu+, mu-, tau+ and tau-)        *
# More specific cuts can be specified in SubProcesses/cuts.f           *
#***********************************************************************
  0.0	= ptl ! Min lepton transverse momentum
  -1.0	= etal ! Max lepton abs(pseudo-rap) (a value .lt.0 means no cut)
  0.0	= drll ! Min distance between opposite sign lepton pairs
  0.0	= drll_sf ! Min distance between opp. sign same-flavor lepton pairs
  0.0	= mll ! Min inv. mass of all opposite sign lepton pairs
  30.0	= mll_sf ! Min inv. mass of all opp. sign same-flavor lepton pairs
#***********************************************************************
# Fermion-photon recombination parameters                              *
# If Rphreco=0, no recombination is performed                          *
#***********************************************************************
  0.1	= rphreco ! Minimum fermion-photon distance for recombination
  -1.0	= etaphreco ! Maximum abs(pseudo-rap) for photons to be recombined (a value .lt.0 means no cut)
  False	= lepphreco ! Recombine photons and leptons together
  False	= quarkphreco ! Recombine photons and quarks together
#***********************************************************************
# Photon-isolation cuts, according to hep-ph/9801442                   *
# Not applied if gamma_is_j                                            *
# When ptgmin=0, all the other parameters are ignored                  *
# More specific cuts can be specified in SubProcesses/cuts.f           *
#***********************************************************************
  {ptGmin:.1f}	= ptgmin ! Min photon transverse momentum
  {etaGAMMA:.1f}	= etagamma ! Max photon abs(pseudo-rap)
  0.4	= r0gamma ! Radius of isolation code
  1.0	= xn ! n parameter of eq.(3.4) in hep-ph/9801442
  1.0	= epsgamma ! epsilon_gamma parameter of eq.(3.4) in hep-ph/9801442
  True	= isoem ! isolate photons from EM energy (photons and leptons)
#***********************************************************************
# Cuts associated to MASSIVE particles identified by their PDG codes.  *
# All cuts are applied to both particles and anti-particles, so use    *
# POSITIVE PDG CODES only. Example of the syntax is {{6 : 100}} or       *
# {{6:100, 25:200}} for multiple particles                               *
#***********************************************************************
  {{}}	= pt_min_pdg ! Min pT for a massive particle
  {{}}	= pt_max_pdg ! Max pT for a massive particle
  {{}}	= mxx_min_pdg ! inv. mass for any pair of (anti)particles
#***********************************************************************
# Use PineAPPL to generate PDF-independent fast-interpolation grid     *
# (https://zenodo.org/record/3992765#.X2EWy5MzbVo)                     *
#***********************************************************************
  False	= pineappl ! PineAPPL switch 
#***********************************************************************
# Folding parameters for S-events to reduce the number of negatively   *
# weighted events. Allowed values are 1, 2, 4 or 8 for each of the     *
# three variables. Typically, folding in xi_i or y_ij results in the   *
# largest reduction of negatively weighted events. (arXiv:2002.12716)  *
#***********************************************************************
  1, 1, 1	= folding ! correspond to folding in xi_i, y_ij, and phi_i
#***********************************************************************
'''
def LOG(*args): print('[run_card_generator_single LOG] ',*args)

class run_card_writer:
    pdlabel = ''
    lhaid   = -1

    nevents = 10000
    ptgmin  = 10.
    ptj     = 10.
    etaj    = -1
    etagamma= -1
    iseed   =  0

    def Write(self,outFOLDER:str, ptGmin:int):
        self.ptgmin = ptGmin
        ofilename=f'run_card_{outFOLDER}@{ptGmin}.dat'
        with open(ofilename,'w') as ofile:
            ofile.write(
                run_card_template.format(
                    #pdLABEL = self.pdlabel,
                    lhaID   = self.lhaid,
                    nEVENTs = self.nevents,
                    ptGmin  = self.ptgmin,
                    ptJ     = self.ptj,
                    etaJ    = self.etaj,
                    etaGAMMA= self.etagamma,
                    iSEED   = self.iseed,
                    ) )
            LOG(f'{ofilename} generated')

def initRunSummary(pdLABEL:str, lhaID:int):
    with open('run_summary.txt', 'w') as ofile:
        ofile.write(f'pdlabel: {pdLABEL}\n')
        ofile.write(f'lhaid  : {lhaID}\n')
def addRunSummary(binNAME:str, ptGmin:int):
    with open('run_summary.txt', 'a') as ofile:
        ofile.write(str( (binNAME,ptGmin) ) + '\n')

def mainfunc(
        outLABEL:str,
        ptMIN:int,
        pdLABEL:str,
        lhaID:int ):
    writer = run_card_writer()
    writer.pdlabel  = pdLABEL
    writer.lhaid    = lhaID
    writer.nevents  = 100000
    writer.iseed    = 0

    writer.ptj      = 30.
    writer.etaj     = 2.4
    writer.etagamma = 2.5

    writer.Write(outLABEL,ptMIN)

    addRunSummary(outLABEL,ptMIN)


if __name__ == "__main__":
    import sys
    argnum = len(sys.argv)
    if argnum != 5 and argnum != 3 and argnum != 1: PrintHelp()

    if argnum == 5:
        # creation usage
        # args: 1. pd label, 2. lha id 3. out label, 4. min pt cut on photon 
        #  append mode
        pdLABEL, lhaID, outLABEL, ptMIN = sys.argv[1:]
        #outLABEL, ptMIN, pdLABEL, lhaID = sys.argv[1:]
        LOG('----- Creation mode -----')

        #initRunSummary(pdLABEL, int(lhaID))
        mainfunc(outLABEL, int(ptMIN), pdLABEL, int(lhaID))
    else:
        # default values
        # args: 1.pd label. 2. lha id
        isDefaultMode = True if argnum == 3 else False
        if isDefaultMode: LOG('----- Default mode -----')
        else:             LOG('-----   Test  mode -----')

        pdLABEL = sys.argv[1] if isDefaultMode else 'NNPDF31_nlo_as_0118'
        lhaID   = sys.argv[2] if isDefaultMode else '303400'

        bin_separations = [
                ('bin01', 30  ),
                ('bin02', 55  ),
                ('bin03', 100 ),
                ('bin04', 135 ),
                ('bin05', 175 ),
                ('bin06', 200 ),
                ('bin07', 220 ),
                ('bin08', 300 ),
                ('bin09', 400 ),
                ('bin10', 500 ),
                ('bin11', 700 ),
                ]

        initRunSummary(pdLABEL, int(lhaID))
        for outLABEL, ptMIN in bin_separations:
            mainfunc(outLABEL, int(ptMIN), pdLABEL, int(lhaID))

    put_to_Events=True
    if put_to_Events:
        import shutil
        import glob
        files_to_move = glob.glob('./' + "run_card_*.dat")

        dest_dir = 'Events/'
        for file in files_to_move:
            LOG(f'moving {file} to {dest_dir}')
            shutil.move(file, dest_dir)

        with open('Events/run_summary.txt', 'a') as orig_file, open('run_summary.txt', 'r') as new_file:
            new_content = new_file.read()
            orig_file.write(new_content)

        import os
        os.remove('run_summary.txt')
        print(f'output files are stored at {os.getcwd()}/Events/')

