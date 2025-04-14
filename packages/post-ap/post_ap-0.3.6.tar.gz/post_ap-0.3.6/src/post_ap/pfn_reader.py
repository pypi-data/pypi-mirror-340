'''
Module storing PFNReader class
'''

import apd

from apd import SampleCollection

from dmu.logging.log_store import LogStore

log = LogStore.add_logger('post_ap:pfn_reader')
# ---------------------------------------
class PFNReader:
    '''
    Thin wrapper around apd used to get list of PFNs
    '''
    #------------------------------------
    def __init__(self, cfg : dict):
        '''
        cfg: Dictionary with configuration needed to read PFNs
        '''
        self._cfg = cfg
    #------------------------------------
    def _paths_from_collection(self, collection : SampleCollection, l_sample : list[str], version : str) -> dict[str,list[str]]:
        d_pfn = {}
        npfn  = 0
        for d_info in collection:
            sample_name = d_info['name']
            sample_vers = d_info['version']

            if sample_vers != version:
                continue

            if sample_name not in l_sample:
                continue

            sam                = collection.filter(name=sample_name)
            l_pfn              = sam.PFNs()
            npfn              += len(l_pfn)
            d_pfn[sample_name] = l_pfn

        log.info(f'Found {npfn} PFNs')

        return d_pfn
    # ---------------------------------------
    def get_pfns(self, production : str, nickname : str) -> dict[str,list[str]]:
        '''
        Parameters:

        production : Name of AP production, e.g. rd_ap_2024
        nickname   : Used to denote list of samples in config, e.g. data

        Returns:

        Dictionary matching sample name and list of ROOT files
        '''
        wg         = self._cfg['working_group']
        apo        = apd.get_analysis_data(analysis=production, working_group=wg)
        collection = apo.all_samples()
        if not isinstance(collection, SampleCollection):
            raise ValueError('Cannot retrieve a collection of samples for {production}:{nickname}')

        l_sample   = self._cfg['productions'][production]['samples' ][nickname]
        version    = self._cfg['productions'][production]['versions'][nickname]

        d_path     = self._paths_from_collection(collection, l_sample, version)

        nsamp = len(d_path)
        log.info(f'Found {nsamp} samples')

        return d_path
# ---------------------------------------
