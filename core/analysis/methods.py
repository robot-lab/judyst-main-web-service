from core.utils.exceptions import *
import core.analysis.consts 


def get_common_statistic(request, models):
    if 'search_request' in request['parameters']:
        ret = {}
        doc_from = request['parameters']['search_request']['doc_id_from']
        doc_to = request['parameters']['search_request']['doc_id_to']
        # need Leva. Need sql....        
        # supertypes_from = []
        # supertypes_to = []
        # for supertype in consts.supertypes:
        #     count = models.Documents.objects.filter(supertype=supertype).
        #     supertypes_from.append({supertype: count})
        #     count = models.Documents.objects.filter(supertype=supertype)
        #     supertypes_from.append({supertype: count})

    raise CommonAnalysisException('Not supported')


analysis_methods = {
    'common_statistic': get_common_statistic,

}
