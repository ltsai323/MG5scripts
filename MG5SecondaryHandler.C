#define MG5SecondaryHandler_cxx
#include "MG5SecondaryHandler.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

void MG5SecondaryHandler::Loop(
        float ptMIN, float ptMAX,
        const char* iFILE, const char* oFILE
        )
{
    IOMgr io_mgr(ptMIN,ptMAX,iFILE,oFILE);
    Init(io_mgr.iTree);
    RegNewTree(io_mgr.oTree);

    // additional branch
    Double_t mc_weight = 1.; io_mgr.oTree->Branch("mcweight" , &mc_weight , "mcweight/D");
    Int_t    phoIdx    = 1.; io_mgr.oTree->Branch("phoIdx"   , &phoIdx    , "phoIdx/I");
    Int_t    jetIdx    = 1.; io_mgr.oTree->Branch("jetIdx"   , &jetIdx    , "jetIdx/I");
    Int_t    secJetIdx = 1.; io_mgr.oTree->Branch("secJetIdx", &secJetIdx , "secJetIdx/I");

   Long64_t nentries = io_mgr.iTree->GetEntries();
   //Long64_t nentries = 100;

   // Get entries with negtive weight
   Double_t sumEntries = 0.;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
       io_mgr.iTree->GetEntry(jentry);
       if ( Event_size == 0 ) continue;
       if ( Event_Weight[0] > 0 ) sumEntries++;
       if ( Event_Weight[0] < 0 ) sumEntries--;
   }


   for (Long64_t jentry=0; jentry<nentries;jentry++) {
       io_mgr.iTree->GetEntry(jentry);
       if ( Event_size == 0 ) continue;
       mc_weight = Event_Weight[0] / sumEntries;

       int pIdx = -1;
       // forbid first 2 incoming particles
       for ( int pidx = 2; pidx < Particle_size; ++pidx )
           if ( Particle_PID[pidx] == 22 ) pIdx = pidx;
       if ( pIdx == -1 ) continue;

       if ( Particle_PT[pIdx]<io_mgr.ptmin ) continue;
       if ( Particle_PT[pIdx]>io_mgr.ptmax ) continue;
       //io_mgr.oTree->Fill();
       //printf("filling evt %d\n", jentry);
       
       int tmp_idx = -1;
       float tmp_pt = -1;
       for ( int jidx = 2; jidx < Particle_size; ++jidx )
       {
           if ( Particle_PID[jidx] == 22 ) continue;
           // find maximum pt
           if ( Particle_PT[jidx] > tmp_pt )
           { tmp_pt = Particle_PT[jidx]; tmp_idx = jidx; }
       }

       phoIdx = pIdx;
       jetIdx = tmp_idx;
       if ( tmp_idx == -1 ) secJetIdx = -1;
       else if ( Particle_size <= 4 ) secJetIdx = -1;
       else if ( phoIdx + jetIdx == 5 ) secJetIdx = 4; // 2+3
       else if ( phoIdx + jetIdx == 6 ) secJetIdx = 3; // 2+4
       else if ( phoIdx + jetIdx == 7 ) secJetIdx = 2; // 3+4

       io_mgr.oTree->Fill();
   }

   io_mgr.oTree->Write();
   io_mgr.oFile->Close();
   io_mgr.iFile->Close();
}
