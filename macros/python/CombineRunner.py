import os
import sys
import subprocess
from multiprocessing import Process

from functions import *



class CombineRunner:

    def __init__(self, path_datacards, year):
        self.path_datacards = path_datacards
        self.year = year
        print 'created an instance of "CombineRunner". Let\'s go!'



    def CreateDatacards(self, masspoints, categories, channels, backgrounds, systematics, rootfilename, signaltag):
        for mass in masspoints:
            for cat in categories:
                for chan in channels:
                    if not cat in categories_per_channel[chan]: continue
                    create_datacard(self.year, mass, cat, chan, backgrounds, systematics, self.path_datacards, 'input/' + rootfilename, signaltag)

    def CombineChannels(self, masspoints, categories, channels):
        combine_dir = os.getenv('CMSSW_BASE') + '/src/HiggsAnalysis/CombinedLimit'
        if not os.path.exists(combine_dir):
            raise RuntimeError('Combine not set-up where expected: %s.' % (combine_dir))
        processes = []
        for mass in masspoints:
            datacards = []
            finalname = self.path_datacards + '/COMB'
            for chan in channels:
                finalname += '_' + chan + '_cat'
                for cat in categories:
                    if not cat in categories_per_channel[chan]: continue
                    datacards.append(self.path_datacards + '/' + variables_per_category[cat] + '_' + chan + '_cat' + cat + '_M' + str(mass) + '.txt')
                    finalname += cat
            finalname += '_M' + str(mass) + '.txt'
            command = [combine_dir + '/scripts/combineCards.py']
            command += datacards
            f = open(finalname, 'w')
            processes.append(subprocess.Popen(command, stdout=f))

        for p in processes:
            p.wait()

    def ExecuteCombineCombination(self, masspoints, categories, channels, signaltag, BR):
        cwd = os.getcwd()
        if not os.path.exists(self.path_datacards + '/output'):
            raise RuntimeError('Combine output directory not where expected: %s.' % (self.path_datacards + '/output'))
        os.chdir(self.path_datacards + '/output');
        combine_dir = os.getenv('CMSSW_BASE') + '/src/HiggsAnalysis/CombinedLimit'
        processes = []
        for mass in masspoints:
            combcard = self.path_datacards + '/COMB'
            for chan in channels:
                combcard += '_' + chan + '_cat'
                for cat in categories:
                    if not cat in categories_per_channel[chan]: continue
                    combcard += cat
            combcard += '_M' + str(mass) + '.txt'
            #command = ['combine', '-n', signal_per_channel[channels[0]], '-m', str(mass), combcard] # make names distinguishable
            command = ['combine', '-n', signaltag + '_BR' + BR, '-m', str(mass), combcard]
            #if 'srele' in channels and 'srmu' in channels:
            #    command = ['combine', '-n', 'LQ_comb', '-m', str(mass), combcard]
            #elif 'srele' in channels:
            #    command = ['combine', '-n', 'LQtoTE', '-m', str(mass), combcard]
            #elif 'srmu' in channels:
            #    command = ['combine', '-n', 'LQtoTMu', '-m', str(mass), combcard]
            #else:
            #    raise RuntimeError('no valid signal region given')

            processes.append(subprocess.Popen(command))

        #f = open('masspoints_%s.txt' % (signal_per_channel[channels[0]]), 'w')
            f = open('masspoints_%s.txt' % signaltag, 'w')
        line = ''
        for m in masspoints:
            line += str(m) + ' '
        line = line[:-1]
        f.write('%i\n%s' % (len(masspoints), line))
        f.close()


        for p in processes:
            p.wait()

        os.chdir(cwd)
