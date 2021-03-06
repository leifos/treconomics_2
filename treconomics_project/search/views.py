from __future__ import absolute_import
import re
import os
import sys
import datetime
import logging
# Django
import math
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from urllib.parse import urlencode
# Whoosh
from whoosh.index import open_dir
# Cache for autocomplete trie
from django.core.cache import caches
# Timing Query
import timeit
# Experiments
from ifind.search import Query
from treconomics.models import DocumentsExamined
from treconomics.models import TaskDescription, TopicAds
from treconomics.experiment_functions import get_topic_relevant_count
from treconomics.experiment_functions import get_experiment_context
from treconomics.experiment_functions import mark_document, log_event
from treconomics.experiment_functions import time_search_experiment_out
from treconomics.experiment_functions import get_performance, populate_context_dict
from treconomics.experiment_functions import log_query_performance, log_performance, query_result_performance
from treconomics.experiment_configuration import my_whoosh_doc_index_dir, data_dir
from treconomics.experiment_configuration import experiment_setups
import json


from .snippets import entity_snippet

ix = open_dir(my_whoosh_doc_index_dir)
ixr = ix.reader()

# logging.basicConfig(level=logging.DEBUG)

@login_required
def show_document(request, whoosh_docid):
    # check for timeout
    """
    Displays the document selected by the user
    :param request:
    :param whoosh_docid: the way of identifying the selected document
    :return:
    """
    if time_search_experiment_out(request):
        return redirect('treconomics:timeout')

    ec = get_experiment_context(request)
    uname = ec["username"]
    taskid = ec["taskid"]
    interface = ec["interface"]
    topic_num = ec["topicnum"]

    condition = ec["condition"]
    current_search = request.session['queryurl']

    # get document from index
    fields = ixr.stored_fields(int(whoosh_docid))
    title = fields["title"]
    content = fields["content"]
    doc_num = fields["docid"]
    doc_date = fields["timedate"]
    doc_source = fields["source"]
    doc_id = whoosh_docid
    # topic_num = ec["topicnum"]

    def get_document_rank():
        """
        Returns the rank (integer) for the given document ID.
        -1 is returned if the document is not found in the session ranked list.
        """
        the_docid = int(whoosh_docid)
        ranked_results = request.session.get('results_ranked', [])

        # Some list comprehension - returns a list of one integer with the rank of a given document
        # if it exists in ranked_results; returns a blank list if the document is not present.
        at_rank = [item[1] for item in ranked_results if item[0] == the_docid]

        if len(at_rank) > 0:
            return at_rank[0]
        else:
            return -1

    # check if there are any get parameters.
    user_judgement = -2
    # rank = 0
    if request.is_ajax():
        getdict = request.GET

        if 'judge' in getdict:
            user_judgement = int(getdict['judge'])
            rank = get_document_rank()

            # marks that the document has been marked rel or nonrel
            doc_length = ixr.doc_field_length(int(request.GET.get('docid', 0)), 'content')
            user_judgement = mark_document(request, doc_id, user_judgement, title, doc_num, rank, doc_length)
            # mark_document handles logging of this event
        return JsonResponse(user_judgement, safe=False)
    else:
        log_event(event="DOC_CLICKED",
                  request=request,
                  whooshid=whoosh_docid)
        
        # marks that the document has been viewed
        rank = get_document_rank()

        doc_length = ixr.doc_field_length(int(doc_id), 'content')
        user_judgement = mark_document(request, doc_id, user_judgement, title, doc_num, rank, doc_length)

        context_dict = {'participant': uname,
                        'task': taskid,
                        'condition': condition,
                        'interface' : interface,
                        'current_search': current_search,
                        'docid': doc_id,
                        'docnum': doc_num,
                        'title': title,
                        'doc_date': doc_date,
                        'doc_source': doc_source,
                        'content': content,
                        'user_judgement': user_judgement,
                        'rank': rank}
        
        if 'task' in request.session:
            context_dict['task'] = int(request.session['task'])
    
        if 'diversity' in request.session:
            context_dict['diversity'] = int(request.session['diversity'])

        if request.GET.get('backtoassessment', False):
            context_dict['backtoassessment'] = True

        ##############
        ##  GET ADS  #
        ##############

        get_ads_for_page(interface, topic_num, context_dict)


        return render(request, 'trecdo/document.html', context_dict)


@login_required
def show_saved_documents(request):
    """
    Displays a list of all the documents that were marked as relevant
    by the user.
    """
    # Timed out?
    if time_search_experiment_out(request):
        return redirect('treconomics:timeout')

    ec = get_experiment_context(request)
    taskid = ec['taskid']
    condition = ec['condition']
    uname = ec['username']
    current_search = request.session['queryurl']
    
    # Following block added by David on 2018-01-04 to ensure the header bar scheme is correct.
    if 'taskid' in request.GET:
        taskid = int(request.GET.get('taskid'))
    elif 'taskid' in request.session:
        taskid = int(request.session['taskid'])
    
    user_judgement = -2
    if request.method == 'GET':
        getdict = request.GET

        if 'judge' not in getdict and 'docid' not in getdict:
            # Log only if user is entering the page, not after clicking a relevant button
            logging.debug('LOG_VIEW_SAVED_DOCS')
            log_event(event="VIEW_SAVED_DOCS", request=request)

        if 'judge' in getdict:
            user_judgement = int(getdict['judge'])
        if 'docid' in getdict:
            docid = int(getdict['docid'])
        if (user_judgement > -2) and (docid > -1):
            # updates the judgement for this document
            doc_length = ixr.doc_field_length(docid, 'content')
            trecid = ixr.stored_fields(docid)['docid']

            user_judgement = mark_document(request=request,
                                           whooshid=docid,
                                           trecid=trecid,
                                           judgement=user_judgement,
                                           doc_length=doc_length)

    # Get documents that are for this task, and for this user
    u = User.objects.get(username=uname)
    docs = DocumentsExamined.objects.filter(user=u).filter(task=taskid)
    
    for doc in docs:
        if doc.title:
            doc.title = doc.title.strip()
        else:
            doc.title = 'Untitled'
        
        if doc.title == '':
            doc.title = 'Untitled'

    context_dict = {'participant': uname,
                    'task': taskid,
                    'condition': condition,
                    'current_search': current_search,
                    'docs': docs}

    return render(request, 'trecdo/saved_documents.html', context_dict)


@login_required
def task(request, taskid):
    logging.debug('TASK_SET_TO %d', taskid)
    request.session['taskid'] = taskid
    pid = request.user.username
    link = "<a href='/treconomics/saved/'>click here</a>"
    msg = '{0} your task is set to: {1}. {2}'.format(pid, taskid, link)
    return HttpResponse(msg)




def run_query(request, result_dict, query_terms='', page=1, page_len=10, condition=0, interface=1, diversity=0, topic_num=None):
    """
    Helper method which populates the results dictionary, and send the user to the right interface.
    :param result_dict: dictionary with query terms
    :param query_terms:
    :param page:
    :param page_len:
    :param condition:
    :param interface:
    :return:
    """

    log_event(event="QUERY_START", request=request, query=query_terms)
    if page < 1:
        page = 1

    query = Query(query_terms)
    query.skip = page
    query.top = page_len
    result_dict['query'] = query_terms

    print(query)
    search_engine = experiment_setups[condition].get_engine()

    ###################################
    # CONTROL THE SNIPPET LENGTH HERE #
    ###################################
    #snippet_sizes = [2, 2, 2, 2]
    #snippet_surround = [40, 40, 40, 40]

    #pos = interface - 1
    #search_engine.snippet_size = snippet_sizes[pos]
    #search_engine.set_fragmenter(frag_type=2, surround=snippet_surround[pos])
    search_engine.snippet_size = 2
    search_engine.set_fragmenter(frag_type=2, surround=40)

    response = search_engine.search(query)

    log_event(event="QUERY_END", request=request, query=query_terms)
    num_pages = response.total_pages

    result_dict['trec_results'] = None
    result_dict['trec_no_results_found'] = True
    result_dict['trec_search'] = False
    result_dict['num_pages'] = num_pages

    logging.debug('PAGE %d', num_pages)

    if num_pages > 0:
        result_dict['trec_search'] = True
        result_dict['trec_results'] = response.results[len(response.results)-page_len:len(response.results)]
        result_dict['curr_page'] = response.actual_page
        print(response.actual_page)

        for res in result_dict['trec_results']:
            res.title = str(res.title, 'utf-8')
            res.source = str(res.source, 'utf-8')
            res.docid = str(res.docid, 'utf-8')
            res.url = str(res.url, 'utf-8')


        if page > 1:
            result_dict['prev_page'] = page - 1
            result_dict['prev_page_show'] = True

            if (page - 1) == 1:
                result_dict['prev_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=1&noperf=true'
            else:
                result_dict['prev_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=' + str(page - 1)
        if page < num_pages:
            result_dict['next_page'] = page + 1
            result_dict['next_page_show'] = True
            result_dict['next_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=' + str(page + 1)


def get_results(request, result_dict, page, page_len, condition, user_query, interface, diversity=0, topic_num=None):
    """
    Returns a results dictionary object for the given parameters above.
    If the combinations have been previously used, we return a cached version (if it still exists).
    If a cached version does not exist, we query Whoosh and return the results.
    """

    start_time = timeit.default_timer()
    # prevent_performance_logging can be passed to override logging.
    # If a user is on page 2 then goes back to page 1, we don't want to get the performance again.
    # if not prevent_performance_logging and page == 1:
    # print "Performance should be measured - but it's disabled as it's too costly!"

    run_query(request, result_dict, user_query, page, page_len, condition, interface, diversity, topic_num)
    result_dict['query_time'] = timeit.default_timer() - start_time


def set_task(request, taskid=-1):
    taskid = int(taskid)

    # If taskid is set, then it marks the start of a new search task
    # Update the session variable to reflect this
    if taskid >= 0:
        request.session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['taskid'] = taskid

        if taskid == 0:
            log_event(event="PRACTICE_SEARCH_TASK_COMMENCED", request=request)
        else:
            log_event(event="SEARCH_TASK_COMMENCED", request=request)


def is_from_search_request(request, new_page_no):
    """
    Returns True if the URL of the referrer is a standard search request.
    This is used to determine if we should delay results appearing.

    The new page number of required to check against the page number from the referer.
    If they match, we don't delay - if they don't, we do.
    """
    http_referer = request.META['HTTP_REFERER']
    http_referer = http_referer.strip().split('&')
    page = 1

    for item in http_referer:
        if 'page=' in item:
            item = item.split('=')
            page = int(item[1])

    if request.POST.get('newquery') == 'true':
        return reverse('search') in request.META['HTTP_REFERER']

    return reverse('search') in request.META['HTTP_REFERER'] and new_page_no == page


@login_required
def search(request, taskid=-1):
    sys.stdout.flush()
    taskid = int(taskid)

    # If taskid is set, then it marks the start of a new search task
    # Update the session variable to reflect this
    if taskid >= 0:
        request.session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['taskid'] = taskid

        if taskid == 0:
            log_event(event="PRACTICE_SEARCH_TASK_COMMENCED", request=request)
        else:
            log_event(event="SEARCH_TASK_COMMENCED", request=request)

    #FIXME this might cause issues check for timeout
    if time_search_experiment_out(request):
        return redirect('treconomics:timeout')
    else:
        """show base index view"""

        ec = get_experiment_context(request)
        condition = ec["condition"]
        rotation = ec["rotation"]
        interface = ec["interface"]
        topic_num = ec["topicnum"]

        print(taskid, rotation, interface, topic_num)
        print('--------')

        page_len = ec["rpp"]
        page = 1

        result_dict = {'participant': ec["username"],
                       'task': ec["taskid"],
                       'topicno': ec["topicnum"],
                       'condition': condition,
                       'interface': interface,
                       'application_root': '/treconomics/',
                       'ajax_search_url': 'searcha/',
                       'autocomplete': ec['autocomplete'],
                       'is_fast': 'true'
                       }

        populate_context_dict(ec, result_dict)


        # Ensure that we set a queryurl.
        # This means that if a user clicks "View Saved" before posing a query, there will be something
        # to go back to!
        if not request.session.get('queryurl'):
            query_url = result_dict['application_root'] + 'search/'
            # TODO revise
            logging.debug('Set queryurl to : %s', query_url)
            request.session['queryurl'] = query_url

        suggestions = False
        query_flag = False
        if request.method == 'POST':
            # handle the searches from the different interfaces
            user_query = request.POST['query'].strip()
            log_event(event="QUERY_ISSUED", request=request, query=user_query)
            query_flag = True
            result_dict['page'] = page
        elif request.method == 'GET':
            getdict = request.GET
            if 'query' in getdict:
                user_query = getdict['query']
                query_flag = True
            if 'suggestion' in getdict:
                suggestions = True
            if suggestions:
                log_event(event="QUERY_SUGGESTION_ISSUED", request=request, query=user_query)

            if 'page' in getdict:
                page = int(getdict['page'])
            else:
                page = 1

        if query_flag:
            # If the user poses a blank query, we just send back a results page saying so.
            if user_query == '':
                result_dict['blank_query'] = True
                return render(request, 'trecdo/results.html', result_dict)
            else:
                # Get some results! Call this wrapper function which uses the Django cache backend.

                print("INTERFACE IS {0}".format(interface))

                print("page: {0} pagelen: {1}".format(page,page_len))
                get_results(request, result_dict,
                            page,
                            page_len,
                            condition,
                            user_query,
                            interface, 0, topic_num)
                log_event(event="QUERY_COMPLETE", request=request, query=user_query)

                result_dict['page'] = page
                result_dict['focus_querybox'] = 'false'

                if result_dict['trec_results'] is None:
                    result_dict['focus_querybox'] = 'true'

                if result_dict['trec_results']:
                    qrp = query_result_performance(result_dict['trec_results'], ec["topicnum"])
                    log_event(event='SEARCH_RESULTS_PAGE_QUALITY',
                              request=request,
                              whooshid=page,
                              rank=qrp[0],
                              judgement=qrp[1])

                    log_query_performance(request, ec["topicnum"], user_query, result_dict['trec_results'])

                #########################
                ##  Get Ads from TopicAds
                ##########################
                print("Serving SERP Ads for Interface:", interface)
                get_ads_for_page(interface, topic_num, result_dict)



                #TODO fix this using url-resolvers (reverse())
                query_params = urlencode({'query': user_query, 'page': page, 'noperf': 'true'})
                query_url = '/treconomics/search/?' + query_params

                logging.debug('Set queryurl to : %s', query_url)
                request.session['queryurl'] = query_url

                result_dict['display_query'] = result_dict['query']
                if len(result_dict['query']) > 50:
                    result_dict['display_query'] = result_dict['query'][0:50] + '...'

                set_results_session_var(request, result_dict)

                log_event(event='VIEW_SEARCH_RESULTS_PAGE', request=request, page=page)
                request.session['last_request_time'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                return render(request, 'trecdo/results.html', result_dict)
        else:
            log_event(event='VIEW_SEARCH_BOX', request=request, page=page)
            return render(request, 'trecdo/search.html', result_dict)


def set_results_session_var(request, result_dict):
    """
    A helper function which sets a session variable containing the Whoosh document IDs for a given
    response.
    """
    results_ranked = []

    if not result_dict['trec_results'] is None:
        for result in result_dict['trec_results']:
            results_ranked.append((result.whooshid, result.rank))

    request.session['results_ranked'] = results_ranked


@login_required
def view_log_query_focus(request):
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    log_event(event='QUERY_FOCUS', request=request)
    return HttpResponse(1)


def view_performance(request):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    def ratio(rels, nonrels):
        """ expect two floats
        """
        dem = rels + nonrels
        if dem > 0.0:
            return round((rels * rels) / dem, 2)
        else:
            return 0.0

    topics = experiment_setups[condition].topics

    avg_acc = 0.0
    performances = []
    for t in topics:
        perf = get_performance(uname, t)
        topic_desc = TaskDescription.objects.get(topic_num=t).title
        perf["num"] = t
        perf["title"] = topic_desc
        perf["score"] = ratio(float(perf["rels"]), float(perf["nons"]))
        perf["total"] = get_topic_relevant_count(t)

        # Should log the performance of each topic here.
        log_performance(request, perf)
        performances.append(perf)
        avg_acc += perf["accuracy"]

    avg_acc = avg_acc / float(len(topics))

    for p in performances:
        logging.debug(p)

    context_dict = {'participant': uname,
                    'condition': condition,
                    'performances': performances, 'avg_acc': avg_acc}
    return render(request, 'base/performance_experiment.html', context_dict)



@login_required
def view_log_hover(request):
    """
    View which logs a user hovering over a search result.
    """
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    ec = get_experiment_context(request)

    uname = ec['username']
    taskid = ec['taskid']
    u = User.objects.get(username=uname)

    status = request.GET.get('status')
    rank = request.GET.get('rank')
    page = request.GET.get('page')
    trec_id = request.GET.get('trecID')
    whoosh_id = request.GET.get('whooshID')
    doc_length = ixr.doc_field_length(int(whoosh_id), 'content')

    try:
        examined = DocumentsExamined.objects.get(user=u, task=taskid, doc_num=trec_id)
        judgement = examined.judgement
    except ObjectDoesNotExist:
        judgement = -2

    msg = ''
    if status == 'in':
        msg = "DOCUMENT_HOVER_IN"

    elif status == 'out':
        msg = "DOCUMENT_HOVER_OUT"

    log_event(event=msg,
              request=request,
              whooshid=whoosh_id,
              trecid=trec_id,
              rank=rank,
              page=page,
              judgement=judgement,
              doc_length=doc_length)

    return JsonResponse({'logged': True})


@login_required
def suggestion_selected(request):
    """
    Called when a suggestion is selected from the suggestion interface.
    Logs the suggestion being selected.
    """
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    new_query = request.GET.get('new_query')
    log_event(event='AUTOCOMPLETE_QUERY_SELECTED', query=new_query, request=request)

    return JsonResponse({'logged': True})


@login_required
def suggestion_hover(request):
    """
    Called when a user hovers over a query suggestion.
    """
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    suggestion = request.GET.get('suggestion')
    rank = int(request.GET.get('rank'))

    log_event(event='AUTOCOMPLETE_QUERY_HOVER', query=suggestion, rank=rank, request=request)

    return JsonResponse({'logged': True})


@login_required
def autocomplete_suggestion(request):
    """
    Handles the autocomplete suggestion service.
    """
    # Get the condition from the user's experiment context.
    # This will yield us access to the autocomplete trie!
    ec = get_experiment_context(request)
    condition = ec['condition']
    rotation = ec['rotation']
    taskid = ec['taskid']
    es = experiment_setups[condition]
    exp = es.get_exp_dict(taskid, rotation)

    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    if request.GET.get('suggest'):
        results = []

        if exp['autocomplete']:
            chars = str(request.GET.get('suggest'))

            # See if the cache has what we are looking for.
            # If it does, pull it out and use that.
            # If it doesn't, query the trie and store the results in the cache before returning.

            autocomplete_cache = caches['autocomplete']
            results = autocomplete_cache.get(chars)

            if not results:
                suggestion_trie = exp['trie']
                results = suggestion_trie.suggest(chars)
                cache_time = 300

                autocomplete_cache.set(chars, results, cache_time)

        response_data = {
            'count': len(results),
            'results': results,
        }

        return JsonResponse(response_data)

    return JsonResponse({'error': True})


def view_run_queries(request, topic_num):
    # from experiment_configuration import bm25

    num = 0
    query_file_name = os.path.join(data_dir, topic_num + '.queries')
    logging.debug(query_file_name)

    start_time = timeit.default_timer()
    query_list = []

    with open(query_file_name, "r") as query_file:
        while query_file and num < 200:
            num += 1
            line = query_file.readline()
            # print line
            parts = line.partition(' ')
            # print parts
            # TODO query_num = parts[0]
            query_str = str(parts[2])
            if query_str:
                logging.debug(query_str)
                q = Query(query_str)
                q.skip = 1
                # TODO response = bm25.search(q)
                query_list.append(query_str)
            else:
                break

    seconds = timeit.default_timer() - start_time

    context_dict = {'topic_num': topic_num, 'seconds': seconds, 'num': num}
    return render(request, 'base/query_test.html', context_dict)



def get_ads_for_page( interface, topic_num, context_dict):
    """
    Puts ads into the context dictionary to be rendered on SERP and Landing Pages.
    :param condition: 1 - No Ads, 2 - On Topic Ads, 3 - Off Topic Ads, 4 - Off and On Topic Ads
    :param topic_num: for on topic ads.
    :param context_dict: context dictionary
    :return: None - updates the context dictionary by adding in the ads for keys: top_ad, bot_ad, side_ads
    """
    top_ad = None
    bot_ad = None
    side_ads = []
    bQ = None

    banner_list = []
    ad_list = []
    #Q(shape__contains='Portrait') | Q(shape_contains='Horizontal')
    # ON TOPIC ADS
    if interface==2:
        bQ = Q(topic_num__contains=topic_num)
        banner_list = TopicAds.objects.filter(Q(shape__contains='Banner'), bQ)
        ad_list = TopicAds.objects.filter(
            Q(shape__contains='Portrait') | Q(shape__contains='Horizontal'),
            bQ
        )

    # OFF TOPIC ADS
    if interface==3:
        bQ = Q(topic_num__contains="0")
        banner_list = TopicAds.objects.filter(Q(shape__contains='Banner'), bQ)
        ad_list = TopicAds.objects.filter(
            Q(shape__contains='Portrait') | Q(shape__contains='Horizontal'),
            bQ
        )


    # OFF and ON TOPIC ADS
    if interface==4:
        bQ = Q(topic_num__contains="0")

        off_banner_list = TopicAds.objects.filter(Q(shape__contains='Banner'), bQ)

        off_ad_list = TopicAds.objects.filter(
            Q(shape__contains='Portrait') | Q(shape__contains='Horizontal'),
            bQ
        )

        bQ = Q(topic_num__contains=topic_num)
        on_banner_list = TopicAds.objects.filter(Q(shape__contains='Banner'), bQ)

        on_ad_list = TopicAds.objects.filter(
            Q(shape__contains='Portrait') | Q(shape__contains='Horizontal'),
            bQ
        )
        banner_list = random.choices(off_banner_list,k=2)+ random.choices(on_banner_list,k=2)
        ad_list = random.choices(off_ad_list, k=4) + random.choices(on_ad_list, k=4)



    if interface > 1:
        side_ads = random.choices(ad_list, k=6)
        top_ad = random.choice(banner_list)
        bot_ad = random.choice(banner_list)

    context_dict['top_ad'] = top_ad
    context_dict['bot_ad'] = bot_ad
    context_dict['side_ads'] = side_ads



def goto_ad(request, adid, pos):
    log_event(event="AD_CLICKED",request=request, whooshid=adid, trecid=pos)
    ad = TopicAds.objects.get(id=adid)
    return redirect(ad.adimage.url)



def check_document(request, whoosh_docid):
    """
    Displays the document
    :param request:
    :param whoosh_docid: the way of identifying the selected document
    :return:
    """
    # get document from index
    fields = ixr.stored_fields(int(whoosh_docid))
    title = fields["title"]
    content = fields["content"]
    doc_num = fields["docid"]
    doc_date = fields["timedate"]
    doc_source = fields["source"]
    doc_id = whoosh_docid



    context_dict = {'docid': doc_id,
                        'docnum': doc_num,
                        'title': title,
                        'doc_date': doc_date,
                        'doc_source': doc_source,
                        'content': content}

    return render(request, 'trecdo/check_document.html', context_dict)

