import pickle
import os
from base import get_total_rmid_list
from position import Location
from psrm.base.target_fibermap import rd2sid, parseVar_sid
from psrm.analSpec.ob2rf import ob2rf
from psrm.analSpec.deredden import SF_deredden


def rmid2sid(rmid):
    '''Look up sid with specific rmid'''
    # This function uses ra & dec for the exchange and serves as an interface
    # between this project with psrm as it does not use rmid
    ra_file = Location.project_loca + "info_database/ra.pkl"
    ra_dict = pickle.load(open(ra_file))
    ra = ra_dict[int(rmid)]
    dec_file = Location.project_loca + "info_database/dec.pkl"
    dec_dict = pickle.load(open(dec_file))
    dec = dec_dict[int(rmid)]
    sid = rd2sid(ra, dec)
    return sid


def sid2pmf(sid):
    '''Look up plate No., mjd and fiber id with specific sid'''
    # This function serves as an interface between this project with psrm
    pmf = parseVar_sid(sid, 'plate', 'mjd', 'fiberid')
    pmflist = [pmf[sid]['plate'], pmf[sid]['mjd'], pmf[sid]['fiberid']]
    return pmflist


def rmid2zfinal(rmid):
    '''Look up the zfinal for specific rmid'''
    zfinal_file = Location.project_loca + "info_database/zfinal.pkl"
    zfinal_dict = pickle.load(open(zfinal_file))
    zfinal = zfinal_dict[rmid]
    return zfinal


def output_raw(rmid, mjd, data, note):
    os.chdir(Location.project_loca + "data/raw")
    try:
        os.mkdir(str(rmid))
    except OSError:
        pass
    os.chdir(str(rmid))
    try:
        os.mkdir(str(mjd))
    except OSError:
        pass
    os.chdir(str(mjd))
    out_file = open(note + ".pkl", "wb")
    pickle.dump(data, out_file)
    out_file.close()


def raw_reader(rmid):
    '''Read in raw data, deredden and transform back to restframe with specific rmid and output to data/raw/specific_rmid'''
    pmflist = sid2pmf(rmid2sid(rmid))
    no_of_obs = len(pmflist[1])
    for i in range(no_of_obs):
        raw = SF_deredden(
            pmflist[0][i],
            pmflist[2][i],
            'fluxerr',
            mjd=pmflist[1][i])
        rf = ob2rf(
            raw['wave'],
            raw['flux'],
            rmid2zfinal(rmid),
            fluxerr=raw['fluxerr'])
        output_raw(rmid, pmflist[1][i], rf['wave'], "wave")
        output_raw(rmid, pmflist[1][i], rf['flux'], "flux")
        output_raw(rmid, pmflist[1][i], rf['fluxerr'], 'error')
