// ScaleAdd.cc
// Scale the QCD hists appropriately for each pT and Add them together
// [] .L ScaleAdd.cc+
// [] run()

#include "TROOT.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TBranch.h"
#include "TLeaf.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1.h"
#include "THStack.h"
#include "TH2.h"
#include "TF1.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TMath.h"
#include <TStyle.h>

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <cstdlib>
#include <cmath>

using namespace std;

const int nPt = 10;
TString pT_range[nPt] = {"170to300", "300to470", "470to600", "600to800", "800to1000", 
                         "1000to1400", "1400to1800", "1800to2400", "2400to3200", "3200toInf"};

void run(){

    TString tagHistDist = "h_AntiTagMinMass30_ReqTopMassFat_TagMassFatMinMass_jetPt";
    TString probeHistDist = "h_AntiTagMinMass30_ReqTopMassFat_Probe_jetPt";

    TFile * OutFile = new TFile("probe_and_tag_hist_QCD_Pt_170toInf_091715.root" , "RECREATE");

    const double lumi = 40.03 ; // pb-1
    double mcscales[nPt] = {
        //xs / nevents * lumi
        117276. / 3468514. * lumi,
        7823 / 2936644. * lumi,
        648.2 / 1971800. * lumi,
        186.9 / 1981608. * lumi,
        32.293 / 1990208. * lumi,
        9.4183 / 1487712. * lumi,
        0.84265 / 197959. * lumi,
        0.114943 / 194924. * lumi,
        0.00682981 / 198383. * lumi,
        0.000165445 / 194528. * lumi
    };


    // Get the 10 QCD files
    TFile* fQCD[nPt];
    TH1F* Check;

    for (int iPt=0; iPt<nPt; iPt++) {
            fQCD[iPt]=new TFile("probe_and_tag_hist_QCD_Pt_"+pT_range[iPt]+"_091715.root","READ");
            cout<<"opened file probe_and_tag_hist_QCD_Pt_"+pT_range[iPt]+"_091715.root"<<endl;
            }
    Check = (TH1F*) fQCD[9]->Get(tagHistDist)->Clone();
    cout<<"DEBUG: after reading the file ="<< Check->GetSum()<<endl;

    // Get the tag histogram in them
    vector<TH1F*> tagHists;
    for (int iPt=0; iPt<nPt; iPt++) {
        tagHists.push_back( (TH1F*) fQCD[iPt]->Get(tagHistDist)->Clone() );
    }

    // Get the probe histogram in them
    vector<TH1F*> probeHists;
    for (int iPt=0; iPt<nPt; iPt++) {
        probeHists.push_back( (TH1F*) fQCD[iPt]->Get(probeHistDist)->Clone() );
    }

    // Scale the tag and probe hists
    for (int iPt=0; iPt<nPt; iPt++) {
        tagHists[iPt]->Scale(mcscales[iPt]);
        probeHists[iPt]->Scale(mcscales[iPt]);
    }
    // Add all tag hists and all probe hists
    TH1F* tagHist_allpT; TH1F* probeHist_allpT;
    tagHist_allpT   = (TH1F*)tagHists[0]->Clone();
    probeHist_allpT = (TH1F*)probeHists[0]->Clone();

    for (int iPt=1; iPt<nPt; iPt++) {
        tagHist_allpT  ->Add( (TH1F*)tagHists[iPt], 1);
        probeHist_allpT->Add( (TH1F*)probeHists[iPt], 1);
    }
    

    // Write the final tag and probe hists in a root file
    OutFile->cd();
    tagHist_allpT->SetName(tagHistDist);
    tagHist_allpT->Write();

    probeHist_allpT->SetName(probeHistDist);
    probeHist_allpT->Write();
    OutFile->Close();
}







