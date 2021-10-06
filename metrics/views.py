from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from model import mongo_services
from tools import jsons

def index(request):
    template = loader.get_template('index.html')
    context = {
        'links': ( {"name":"home", "target":"/"},
                   {"name":"parcourir", "target":"/metrics/dictionnary"},
                   {"name":"Contact", "target":"mailto:contact@kommets.com"}
                   )
    }
    return HttpResponse(template.render(context, request))
    
def dictionnary(request):
    template = loader.get_template('dico.html')
    context = {
        'links': ( {"name":"home", "target":"/"},
                   )
    }    
    return HttpResponse(template.render(context, request))
    
def browse(request):
    letter = request.GET.get('l')
    #sys.path.insert(0,"../model")
    enterprises = mongo_services.get_enterprises_starting_with(letter)
    template = loader.get_template('browse.html')
    context = {
        'links': ( {"name":"home", "target":"/"},
                   {"name":"parcourir", "target":"/metrics/dictionnary"},
                  ),
        'enterprises': enterprises
    }    
    return HttpResponse(template.render(context, request))
    
def outline(request):
    id = int(request.GET.get('id'))
    enterprise_data = mongo_services.get_enterprise_document(id)
    context = { "links":({"name":"home", "target":"/"}, {"name":"parcourir", "target":"/metrics/dictionnary"}),
                "name": enterprise_data["elem"]["name"],
                "sector": enterprise_data["sector"],
                "assets_data": jsons.get_assets(enterprise_data["elem"]),
                "liabilities_data": jsons.get_liabilities(enterprise_data["elem"]),
                "results_data": jsons.get_results_data(enterprise_data["elem"]),
                "quantile_data":jsons.get_quantiles(enterprise_data["elem"]),
                "qvalues":jsons.get_qvalues(enterprise_data["elem"]),
                "score":enterprise_data["elem"]["sc"],
                "qscore":enterprise_data["elem"]["qs"]
                }
                                        #
                                        #
                                        #"quantile_data"=>$this->get('app.jsons')->get_quantiles($enterprise_data["elem"]),
                                        #"qvalues"=>$this->get('app.jsons')->get_qvalues($enterprise_data["elem"]),
                                        #"score"=>$enterprise_data["elem"]["sc"],
                                        #"qscore"=>$enterprise_data["elem"]["qs"]
                                        #));
    template = loader.get_template('outline.html')
    return HttpResponse(template.render(context, request))