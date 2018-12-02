from core.analysis.methods import *


def process(request, models):
    func = analysis_methods[request['method']]
    return func(request, models)
