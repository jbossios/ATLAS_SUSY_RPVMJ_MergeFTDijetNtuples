
import array
from numpy import unique
import sys
import os
from ROOT import *
import logging

def merge_tchain_to_rdf(my_tchain, ttree_name, output_dir, dry_run, pmg_file_name, sum_of_weights, log, debug):
	""" Create a RDataFrame from a TChain, add a branch and save it to a ROOT file"""
	# Create RDataFrame
	my_df = RDataFrame(my_tchain)
	if not my_df:
		log.fatal('RDataFrame can not be created, exiting')
		sys.exit(1)
	n_events = my_df.Count().GetValue()
	log.info('Total number of entries = {}'.format(n_events))

	# Protection
	if not n_events:
		log.info('No events found, no output file will be produced')
		sys.exit(0)
	
	# Get DSIDs
	dsids_ = unique((my_df.AsNumpy(["mcChannelNumber"]))['mcChannelNumber']).tolist()
	dsids = [int(dsid) for dsid in dsids_]
	log.debug('dsids = {}'.format(dsids))

	# Create output directory
	if not dry_run and not os.path.exists(output_dir):
		os.makedirs(output_dir)

	# Separate dataframes by DSID
	for dsid in dsids:
		my_df_dsid = my_df.Filter("mcChannelNumber == {}".format(dsid))
	
		# Get PMG info (xs, eff, kfactor, etc) for this dsid
		pmg_dict = get_pmg_info(pmg_file_name, [dsid])
		log.debug('pmg_dict = {}'.format(pmg_dict))
	
		# Add normweight branch
		pmg_info = pmg_dict[dsid]
		log.debug('Adding "normweight" branch for dsid = {}'.format(dsid))
		my_df_dsid = my_df_dsid.Define("normweight", "mcEventWeight * {} * {} * {} / {}".format(pmg_info['xs'], pmg_info['eff'], pmg_info['kfactor'], sum_of_weights[dsid]))
		if debug:
			hist = my_df_dsid.Histo1D("normweight")
			output_file = TFile('normweight_histogram_dsid_{}.root'.format(dsid), 'RECREATE')
			hist.Write()
			output_file.Close()

		# Write new DFs as TTrees to ROOT files (unless requested not to)
		if not dry_run:
			log.debug('Taking a snapshot of the dataframe')
			my_df_dsid.Snapshot(ttree_name, '{}/{}.root'.format(output_dir, dsid));

def get_pmg_info(pmg_file, dsids):
	""" Get PMG cross-sections, efficiencies, kfactors, etc """
	pmg_dict = {}
	with open(pmg_file) as f:
		lines = f.read().splitlines()
	for dsid in dsids:
		selectedLines = [x for x in lines if str(dsid) in x]
		info = selectedLines[0].split()
		pmg_dict[dsid] = {
			"xs" : float(info[2]),
			"eff" : float(info[3]),
			"kfactor" : float(info[4]),
			"XSecUncUP" : float(info[5]),
			"XSecUncDOWN" : float(info[6]),
		}
	return pmg_dict

def merge_ttrees(args):
	""" Merge TTrees together and add normweight branch"""

	# Read arguments
	input_dir = args.input_dir
	output_dir = args.output_dir
	pmg_file_name = args.pmg_file_name
	debug = args.debug
	ttree_name = args.ttree_name
	dry_run = args.dry_run
	n_cpu = args.n_cpu

	# Create logger
	logging.basicConfig(level = 'INFO' if not debug else 'DEBUG', format = '%(levelname)s: %(message)s')
	log = logging.getLogger()

	log.info('Files in the following directory will be merged: {}'.format(input_dir))

	# Create a TChain of all TTrees
	ROOT.EnableImplicitMT(n_cpu)
	my_tchain = TChain(ttree_name)
	sum_of_weights = {} # sum of weights for each dsid
	for file_name in os.listdir(input_dir):
		# Make sure it's a ROOT file
		if not file_name.endswith('.root'): continue
		# Add only non-empty TTrees (but get metadata from all files, even those w/ empty TTrees)
		full_file_name = '{}/{}'.format(input_dir, file_name)
		try:
			tfile = TFile.Open(full_file_name)
		except OSError:
			raise OSError('{} can not be opened'.format(full_file_name))
		if tfile:
			# Identify DSID for this file
			dsid = int(input_dir.split('user.')[1].split('.')[2])
			log.debug('dsid: {} identified from input_dir: {}'.format(dsid, input_dir))
			# Get sum of weights from metadata
			metadata_hist = tfile.Get('MetaData_EventCount')
			if dsid not in sum_of_weights:
				sum_of_weights[dsid] = metadata_hist.GetBinContent(2) # initial sum of weights
			else:
				sum_of_weights[dsid] += metadata_hist.GetBinContent(2) # initial sum of weights
			# Get TTree and add it to the TChain
			ttree = tfile.Get('trees_SRRPV_')
			if ttree:
				if ttree.GetEntries() > 0:
					my_tchain.Add(full_file_name)
			tfile.Close()

	merge_tchain_to_rdf(my_tchain, ttree_name, output_dir, dry_run, pmg_file_name, sum_of_weights, log, debug)

	log.info('>>> All done <<<')

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--inDir', action='store', dest='input_dir', default='', help='Path to input files to be merged')
	parser.add_argument('--outDir', action='store', dest='output_dir', default='', help='Directory where output merged files will be located')
	parser.add_argument('--pmgFileName', action='store', dest='pmg_file_name', default='/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc16.txt', help='Full file name containing PMG cross sections, efficiencies, etc')
	parser.add_argument('--ttreeName', action='store', dest='ttree_name', default='trees_SRRPV_', help='Name of input TTrees')
	parser.add_argument("--nCPU",  action='store', dest='n_cpu', default=4, help = 'Number of CPUs to be used for multi-threading')
	parser.add_argument("--dryRun",  action='store_true', dest='dry_run', default=False, help = 'do a dry run, without actually merging anything')
	parser.add_argument('--debug', action='store_true', dest='debug', default=False, help='Debug flag')
	args = parser.parse_args()

	# Protections
	if not args.input_dir:
		log.fatal('{} is empty, please specify input directory, exiting'.format(input_dir))
		parser.print_help()
		sys.exit(1)
	if not args.output_dir:
		log.fatal('{} is empty, please specify input directory, exiting'.format(output_dir))
		parser.print_help()
		sys.exit(1)
	
	merge_ttrees(args)
