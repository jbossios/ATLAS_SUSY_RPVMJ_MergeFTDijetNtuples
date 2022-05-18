from multiprocessing import Pool
from functools import partial
import array
from numpy import unique
import sys
import os
from ROOT import *
import logging

# create log
logging.basicConfig(level = 'INFO', format = '%(levelname)s: %(message)s')
log = logging.getLogger()

def add_normweight(conf):
  """ Create a RDataFrame from a TChain, add a branch and save it to a ROOT file"""
  # unpack
  file_name = conf["file_name"]
  input_dir = conf["input_dir"]
  ttree_name = conf["ttree_name"]
  output_dir = conf["output_dir"]
  dry_run = conf["dry_run"]
  pmg_file_name = conf["pmg_file_name"]
  sum_of_weights = conf["sum_of_weights"]
  debug = conf["debug"]

  # check if should infer output directory
  if not output_dir:
    output_dir = os.path.dirname(file_name)

  log.info('Processing {}'.format(file_name))

  # Make sure input file is a ROOT file
  if not file_name.endswith('.root'):
    pass
  
  # Open ROOT file and get TTree
  tfile = TFile.Open(file_name)
  # Identify DSID for this file
  dsid = int(file_name.split('user.')[1].split('.')[2])
  log.debug('dsid: {} identified from {}'.format(dsid, file_name))
  # Get TTree and add it to the TChain
  ttree = tfile.Get(ttree_name)
  if not ttree:
    tfile.Close()
    pass
  if ttree.GetEntries() == 0:
    tfile.Close()
    pass

  # Create RDataFrame
  my_df = RDataFrame(ttree)
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
    log.info('Adding "normweight" branch for file with dsid = {}'.format(dsid))
    my_df_dsid = my_df_dsid.Define("normweight", "mcEventWeight * {} * {} * {} / {}".format(pmg_info['xs'], pmg_info['eff'], pmg_info['kfactor'], sum_of_weights[dsid]))
    if debug:
      hist = my_df_dsid.Histo1D("normweight")
      output_file = TFile('normweight_histogram_dsid_{}.root'.format(dsid), 'RECREATE')
      hist.Write()
      output_file.Close()

    # Write new DFs as TTrees to ROOT files (unless requested not to)
    if not dry_run:
      out_full_file_name = '{}/{}'.format(output_dir, os.path.basename(file_name).replace(".root", "_expanded.root"))
      log.info('Taking a snapshot of the dataframe as a ROOT file: {}'.format(out_full_file_name))
      my_df_dsid.Snapshot(ttree_name, out_full_file_name);

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

def expand_ttrees(args):
  """ Expand TTrees by adding normweight branch"""

  # Read arguments
  input_dir = args.input_dir
  output_dir = args.output_dir
  pmg_file_name = args.pmg_file_name
  debug = args.debug
  ttree_name = args.ttree_name
  dry_run = args.dry_run
  ncpu = args.ncpu

  # get list of files
  file_list = handleInput(input_dir)
  # remove already expanded files
  file_list = [i for i in file_list if '_expanded.root' not in i]

  # Create logger
  logging.basicConfig(level = 'INFO' if not debug else 'DEBUG', format = '%(levelname)s: %(message)s')
  log = logging.getLogger()
  
  log.info('Files in the following directory will be merged: {}'.format(input_dir))

  # Get sum of weights from all input files (by DSID)
  sum_of_weights = {} # sum of weights for each dsid
  for file_name in file_list:
    # Make sure it's a ROOT file
    if not file_name.endswith('.root'): continue
    # Get metadata from all files, even those w/ empty TTrees
    # full_file_name = '{}/{}'.format(input_dir, file_name)
    try:
      tfile = TFile.Open(file_name)
    except OSError:
      raise OSError('{} can not be opened'.format(file_name))
    # Identify DSID for this file
    dsid = int(file_name.split('user.')[1].split('.')[2])
    log.debug('dsid: {} identified from input_dir: {}'.format(dsid, file_name))
    # Get sum of weights from metadata
    metadata_hist = tfile.Get('MetaData_EventCount')
    if dsid not in sum_of_weights:
      sum_of_weights[dsid] = metadata_hist.GetBinContent(3) # initial sum of weights
    else:
      sum_of_weights[dsid] += metadata_hist.GetBinContent(3) # initial sum of weights
  
  print(sum_of_weights)

  # create job configurations
  config = []
  for file_name in file_list:
    config.append({
      "file_name" : file_name, 
      "input_dir" : input_dir,
      "ttree_name" : ttree_name,
      "output_dir" : output_dir,
      "dry_run" : dry_run,
      "pmg_file_name" : pmg_file_name,
      "sum_of_weights" : sum_of_weights,
      #"log" : log, 
      "debug" : debug
    })

  # Add normweight and write a new ROOT file
  if not dry_run:
    if ncpu > 1:
      # launch pool
      results = Pool(ncpu).map(add_normweight, config)
    else:
      for conf in config:
        add_normweight(conf)
  
  log.info('>>> All done <<<')

def handleInput(data):
    # otherwise return 
    if os.path.isfile(data) and ".root" in os.path.basename(data):
        return [data]
    elif os.path.isfile(data) and ".txt" in os.path.basename(data):
        return sorted([line.strip() for line in open(data,"r")])
    elif os.path.isdir(data):
        return sorted(os.listdir(data))
    elif "*" in data:
        from glob import glob
        return sorted(glob(data))
    return []

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--inDir', action='store', dest='input_dir', default='', help='Path to input files')
  parser.add_argument('--outDir', action='store', dest='output_dir', default='', help='Directory where output/updated files will be located')
  parser.add_argument('--pmgFileName', action='store', dest='pmg_file_name', default='/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc16.txt', help='Full file name containing PMG cross sections, efficiencies, etc')
  parser.add_argument('--ttreeName', action='store', dest='ttree_name', default='trees_SRRPV_', help='Name of input TTrees')
  parser.add_argument("--dryRun",  action='store_true', dest='dry_run', default=False, help = 'do a dry run, without actually doing anything')
  parser.add_argument('--debug', action='store_true', dest='debug', default=False, help='Debug flag')
  parser.add_argument("--ncpu", help="Number of cores to use for multiprocessing. If not provided multiprocessing not done.", default=1, type=int)
  args = parser.parse_args()
  print(args.output_dir)
  # Protections
  if not args.input_dir:
    print('ERROR: please specify input directory, exiting')
    parser.print_help()
    sys.exit(1)
  if not args.output_dir:
    #print('ERROR: please specify output directory, exiting')
    log.info("No output directory provided so inferring from filenames")
    #parser.print_help()
    #sys.exit(1)
  
  expand_ttrees(args)
