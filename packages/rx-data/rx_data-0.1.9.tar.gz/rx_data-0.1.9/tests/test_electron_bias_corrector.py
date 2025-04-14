'''
Module used to test bias corrections
'''

import os

import numpy
import pytest
import mplhep
import pandas            as pnd
import matplotlib.pyplot as plt

from pandarallel                     import pandarallel
from dmu.logging.log_store           import LogStore
from rx_data.rdf_getter              import RDFGetter
from rx_data.utilities               import df_from_rdf
from rx_data.electron_bias_corrector import ElectronBiasCorrector

log=LogStore.add_logger('rx_data:test_electron_bias_corrector')
#-----------------------------------------
class Data:
    '''
    Data class
    '''
    plt_dir = '/tmp/tests/rx_data/electron_bias_corrector'
#-----------------------------------------
@pytest.fixture(scope='session', autouse=True)
def _initialize():
    LogStore.set_level('rx_data:electron_bias_corrector', 10)
    plt.style.use(mplhep.style.LHCb2)

    os.makedirs(Data.plt_dir, exist_ok=True)
#-----------------------------------------
def _add_column(df : pnd.DataFrame, var : str):
    if var == 'max_PT':
        df[var] = numpy.maximum(df.L1_PT, df.L2_PT)

    if var == 'min_PT':
        df[var] = numpy.minimum(df.L1_PT, df.L2_PT)

    return df
#-----------------------------------------
def _get_range(var : str) -> tuple[float,float]:
    minx = None
    maxx = None

    if 'HASBREMADDED' in var:
        minx = 0
        maxx = 2

    if 'PX' in var or 'PY' in var or 'PT' in var:
        minx =    250
        maxx = 10_000

    if 'PZ' in var:
        minx =    250
        maxx = 100_000

    if 'ETA' in var:
        minx = 2
        maxx = 5

    if 'PHI' in var:
        minx = -3.14
        maxx =  3.14

    return minx, maxx
#-----------------------------------------
def _plot_brem_kinematics(df : pnd.DataFrame, var : str, label : str, ax=None):
    df         = _add_column(df, var)
    minx, maxx = _get_range(var)

    if label == 'Original':
        ax = df[var].hist(label=label, alpha=0.5, bins=40, range=[minx,maxx], ax=ax, color='gray')
    else:
        ax = df[var].hist(label=label, histtype='step', bins=40, range=[minx,maxx], ax=ax)

    return ax
#-----------------------------------------
def _plot_correction(org : pnd.DataFrame, cor : pnd.DataFrame, name : str) -> None:
    out_dir = f'{Data.plt_dir}/{name}'
    os.makedirs(out_dir, exist_ok=True)

    l1_var = ['L1_ETA', 'L1_PHI', 'L1_PT', 'L1_PX', 'L1_PY', 'L1_PZ', 'L1_HASBREMADDED']
    l2_var = ['L2_ETA', 'L2_PHI', 'L2_PT', 'L2_PX', 'L2_PY', 'L2_PZ', 'L2_HASBREMADDED']

    for var in l1_var + l2_var:
        ax=_plot_brem_kinematics(df=org, var=var, label='Original' )
        ax=_plot_brem_kinematics(df=cor, var=var, label='Corrected', ax=ax)
        if 'PT' in var:
            name= var.replace('PT', 'TRACK_PT')
            ax  = _plot_brem_kinematics(df=cor, var=name, label='Track', ax=ax)

        nentries = len(org)
        title = f'Entries={nentries}'
        plt.title(title)
        plt.legend()
        plt.xlabel(var)
        plt.savefig(f'{out_dir}/{var}.png')
        plt.close()
#-----------------------------------------
def _get_df(nentries : int = 10) -> pnd.DataFrame:
    RDFGetter.samples = {
        'main' : '/home/acampove/external_ssd/Data/samples/main.yaml',
        'mva'  : '/home/acampove/external_ssd/Data/samples/mva.yaml',
        }

    gtr = RDFGetter(sample='DATA_24_Mag*_24c4', trigger='Hlt2RD_BuToKpEE_MVA')
    rdf = gtr.get_rdf()
    rdf = rdf.Define('L1_TRACK_PT' , 'TMath::Sqrt(L1_TRACK_PX * L1_TRACK_PX + L1_TRACK_PY * L1_TRACK_PY)')
    rdf = rdf.Define('L2_TRACK_PT' , 'TMath::Sqrt(L2_TRACK_PX * L2_TRACK_PX + L2_TRACK_PY * L2_TRACK_PY)')

    rdf = rdf.Filter('mva_cmb > 0.8 && mva_prc > 0.5')
    rdf = rdf.Filter('Jpsi_M > 2800 && Jpsi_M < 3200')
    rdf = rdf.Filter('B_const_mass_M > 5200')

    rdf = rdf.Redefine('L1_HASBREMADDED', 'int(L1_HASBREMADDED)')
    rdf = rdf.Redefine('L1_BREMHYPOCOL' , 'int(L1_BREMHYPOCOL)' )
    rdf = rdf.Redefine('L1_BREMHYPOROW' , 'int(L1_BREMHYPOROW)' )
    rdf = rdf.Redefine('L1_BREMHYPOAREA', 'int(L1_BREMHYPOAREA)')
    rdf = rdf.Range(nentries)

    return df_from_rdf(rdf)
#-----------------------------------------
def _filter_kinematics(df : pnd.DataFrame, lepton : str = None):
    l_to_keep = [
                 f'{lepton}_PX',
                 f'{lepton}_PY',
                 f'{lepton}_PZ',
                 f'{lepton}_PT',
                 f'{lepton}_TRACK_PT',
                 f'{lepton}_ETA',
                 f'{lepton}_HASBREMADDED',
                 f'{lepton}_PHI']

    if lepton is None:
        l_to_keep_l1 = [ name.replace('None', 'L1') for name in l_to_keep ]
        l_to_keep_l2 = [ name.replace('None', 'L2') for name in l_to_keep ]
        l_to_keep    = l_to_keep_l1 + l_to_keep_l2

    df = df[l_to_keep]

    return df
#-----------------------------------------
def _check_equal(df_org : pnd.DataFrame, df_cor : pnd.DataFrame, must_differ : bool) -> None:
    equal_cols = numpy.isclose(df_org, df_cor, rtol=0.001)

    if must_differ:
        assert not numpy.all(equal_cols)
    else:
        assert numpy.all(equal_cols)
#-----------------------------------------
def test_skip_correction():
    '''
    Tests without actually doing the correction
    '''
    df_org = _get_df()
    df_org = df_org.fillna(-1)
    cor    = ElectronBiasCorrector(skip_correction=True)
    df_cor = df_org.apply(lambda row : cor.correct(row, 'L1'), axis=1)

    df_org = _filter_kinematics(df_org, lepton='L1')
    df_cor = _filter_kinematics(df_cor, lepton='L1')

    _check_equal(df_org, df_cor, must_differ = False)
#-----------------------------------------
def test_correction_brem_track():
    '''
    Use brem_track methods
    '''
    LogStore.set_level('rx_data:electron_bias_corrector', 40)
    pandarallel.initialize(nb_workers=1, progress_bar=True)

    df_org = _get_df(nentries = 10_000)
    df_org = df_org.fillna(-1)

    cor    = ElectronBiasCorrector(skip_correction=False)
    df_cor = df_org.apply(lambda row : cor.correct(row, 'L1', kind='brem_track_2'), axis=1)
    df_cor = df_cor.apply(lambda row : cor.correct(row, 'L2', kind='brem_track_2'), axis=1)

    df_org = _filter_kinematics(df_org)
    df_cor = _filter_kinematics(df_cor)

    _plot_correction(org=df_org, cor=df_cor, name='brem_track_2')
    _check_equal(df_org, df_cor, must_differ = True)
    LogStore.set_level('rx_data:electron_bias_corrector', 10)
#-----------------------------------------
