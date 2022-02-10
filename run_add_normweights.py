import os

sample = 'Signal' # options: Signal, Dijets

signal_path = '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/signal/'

paths = {
  'Dijets' : [
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.abadea.mc16_13TeV.364705.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5WithSW.r10724_p4355.21.2.173-0_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364702.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2WithSW.r10724_p4355.21.2.173-0-v2_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364703.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3WithSW.r10724_p4355.21.2.173-0_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.r10724_p4355.21.2.173-0-v2_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364706.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ6WithSW.r10724_p4355.21.2.173-0_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364707.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ7WithSW.r10724_p4355.21.2.173-0_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364708.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ8WithSW.r10724_p4355.21.2.173-0_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364709.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ9WithSW.r10724_p4355.21.2.173-0-v2_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364710.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ10WithSW.r10724_p4355.21.2.173-0-v2_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364711.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ11WithSW.r10724_p4355.21.2.173-0_trees.root',
    '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets/user.jbossios.mc16_13TeV.364712.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ12WithSW.r10724_p4355.21.2.173-0_trees.root',
  ],
  'Signal' : [
    signal_path+'user.sfranche.mc16_13TeV.504509.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_100_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504510.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_200_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504511.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_300_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504512.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_400_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504513.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_900_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504514.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1000_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504515.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1100_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504516.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1200_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504517.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1300_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504518.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1400_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504519.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1500_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504520.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1600_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504521.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1700_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504522.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1800_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504523.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_1900_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504524.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_2000_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504525.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_2100_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504526.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_2200_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504527.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_2300_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504528.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_2400_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504529.MGPy8EG_A14NNPDF23LO_GG_rpv_UDB_2500_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504530.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_100_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504531.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_200_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504532.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_300_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504533.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_400_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504534.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_900_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504535.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1000_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504536.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1100_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504537.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1200_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504538.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1300_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504539.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1400_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504540.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1500_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504541.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1600_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504542.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1700_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504543.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1800_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504544.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_1900_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504545.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_2000_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504546.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_2100_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504547.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_2200_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504548.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_2300_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504549.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_2400_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504550.MGPy8EG_A14NNPDF23LO_GG_rpv_UDS_2500_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504551.MGPy8EG_A14NNPDF23LO_GG_rpv_ALL_1800_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
    signal_path+'user.sfranche.mc16_13TeV.504552.MGPy8EG_A14NNPDF23LO_GG_rpv_ALL_2200_squarks.r10724_p4355.21.2.173-0-v2_trees.root',
  ],
}

base_out_dir = {
  'Dijets' : '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/dijets_expanded',
  'Signal' : '/eos/atlas/atlascerngroupdisk/phys-susy/RPV_mutlijets_ANA-SUSY-2019-24/ntuples/tag/input/mc16e/signal_expanded',
}

commands = []
for path in paths[sample]:
  # Identify type of sample
  sample = 'dijets' if '3647' in path else 'signal'
  if sample == 'dijets':
    jz_slice = int(path.split('3647')[1][0:2])
    out_dir = '{}/JZ{}'.format(base_out_dir[sample], jz_slice)
  else: # signal
    dsid = path.split('5045')[1][0:2]
    out_dir = '{}/5045{}'.format(base_out_dir[sample], dsid)
  commands.append('python add_normweights.py --inDir {} --outDir {}'.format(path, out_dir))

command = ' && '.join(commands) + ' &'
os.system(command)
