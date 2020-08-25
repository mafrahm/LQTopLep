
from python.CombineRunner import *


path_datacards = '/nfs/dust/cms/user/frahmmat/CMSSW_10_2_X_v2/CMSSW_10_2_16/src/UHH2/LQTopLep/data/datacards'
CombineRunner = CombineRunner(path_datacards, 2016)

systematics = ['lumi', 'rate_ttbar', 'rate_dy', 'rate_ttv', 'rate_diboson', 'rate_singletop', 'rate_wjets', 'rate_qcdele', 'pu', 'pdf', 'muid', 'muiso', 'mutrigger', 'eleid', 'elereco', 'eletrigger', 'btag_bc', 'btag_udsg', 'scale_TTbar', 'scale_DYJets', 'scale_TTV', 'scale_Diboson', 'scale_SingleTop']

backgrounds = ['TTbar', 'DYJets', 'SingleTop', 'TTV', 'Diboson', 'WJets', 'QCDEle'] #QCDMu needed for ttbar


categories = ['A', 'B']
channels = ['srele'] #srele, dycrele, ttbar


masspoints = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1700, 2000]


CombineRunner.CreateDatacards(masspoints, categories, channels, backgrounds, systematics, 'combine_histograms_mc_fullsyst_ech.root')
CombineRunner.CombineChannels(masspoints, categories, channels)
CombineRunner.ExecuteCombineCombination(masspoints, categories, channels)


# srele alone works perfectly
# limits with CRs look weird
# how to add ttbar region? using QCDMu and LQtoTMu?
