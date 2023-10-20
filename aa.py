#!/usr/bin/env python3
import ROOT

if __name__ =="__main__":
    ifile = ROOT.TFile.Open('../old/gjet_NLO_loop_sm_no_b_mass_CT14nnlo/Events/lowPT.root')
    itree = ifile.Get('LHEF')

    ofile = ROOT.TFile('new.root','recreate')
    otree = itree.CloneTree(0)

    ientry = 10

    for idx in range(ientry):
        itree.GetEntry(idx)
        print(itree.Particle_size, itree.__dict__)
        otree.Fill()
    ofile.cd()
    otree.Write()
    ofile.Close()
