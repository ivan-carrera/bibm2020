from Bio import Entrez
import time
import os
import json


# replace special chars
def replace_spchars(original_string):
    new_string = original_string  # .encode('ascii', errors='ignore')
    for c in ['\n', '>', '<', '&', '(', ')', '[', ']', '%', '=', ',', '.', '+', '\\', '/', '#', '-']:
        new_string = new_string.replace(c, ' ')
    return new_string.strip()


# transform an abstract from text to a dictionary
def to_dict(abstract_string, cell_name):
    abstract_ = dict()
    doc_list = abstract_string.split('\n\n')
    title = doc_list[1]
    try:
        title = title.replace('\n', ' ')
    except:
        pass
    title = replace_spchars(title)
    len_list = []
    for item in doc_list:
        len_list.append(len(item))
        if 'PMID:' in item:
            item = item.split('PMID:')[1]
            try:
                item = item.replace(' [Indexed for MEDLINE]', '')
            except:
                pass
            item = item.replace(' ', '')
            index_ = 'PMID:' + item
    # abstract should be the biggest item of doc_list
    abstract = doc_list[len_list.index(max(len_list))]
    abstract = replace_spchars(abstract).replace('\n', ' ')
    if abstract.startswith('Author information:'):
        abstract = ''
    abstract = (title + ' ' + abstract)
    abstract_['title'] = title
    abstract_['index'] = index_
    abstract_['document'] = abstract
    abstract_['cell_id'] = cell_name
    return abstract_


# list_toquery transforms the list of synonyms into a query
def list_toquery(list_):
    string = ''
    if list_ is None:
        print('List is NONE')
    if type(list_) is str:
        list_ = [list_]
    for element in list_:
        if element is None:
            x = ''
        else:
            x = str(element)
        if x != '':
            string = string + '("' + x + '"[Title/Abstract]) OR '
    return string[:-4] + ' AND ((cell line[Title/Abstract]) OR (cellular line[Title/Abstract]) OR ' \
                         '(cell-line[Title/Abstract]))'


# query returns a list of PubMed IDs
def search_idlist(query):
	# This information should be updated with your Entrez credentials
    # Please refer to [https://www.ncbi.nlm.nih.gov/books/NBK25497/#_chapter2_Usage_Guidelines_and_Requiremen_]
    # You can create an account in [https://www.ncbi.nlm.nih.gov/account/]
    Entrez.email = ''
    Entrez.api_key = ''
    try:
        handle = Entrez.esearch(db='pubmed', sort='relevance', retmax='500', retmode='xml', term=query)
        results = Entrez.read(handle)
    except Exception as e:
        print('Something is happening with queries about: ', query, e)
        time.sleep(2)  # this sleep is performed when PubMed servers reject queries
        return search_idlist(query)
    return results['IdList']


# once you have a PubMed ID, you can retrieve the abstract
def get_abstract(pmid):
    # This information should be updated with your Entrez credentials
    # Please refer to [https://www.ncbi.nlm.nih.gov/books/NBK25497/#_chapter2_Usage_Guidelines_and_Requiremen_]
    # You can create an account in [https://www.ncbi.nlm.nih.gov/account/]
    Entrez.email = ''
    Entrez.api_key = ''
    try:
        handle = Entrez.efetch(db='pubmed', id=pmid, retmode='text', rettype='abstract')
    except Exception as e:
        print('Error with PMID:', pmid, e)
        time.sleep(2)
        return get_abstract(pmid)
    return handle.read()


def process_gt(cell_):
    gt_path = 'data/cell_json_gt/'
    cell_id = cell_['accession']
    if os.path.exists(gt_path + cell_id + '.json'):
        print(cell_id, 'gt file already exists')
        pass
    else:
        cell_abstracts = dict()
        cell_abstracts['cell_id'] = cell_id
        cell_abstracts['documents'] = list()

        gt_list = cell_['reference']
        print(cell_id, 'fetching', len(gt_list), 'abstracts from ground truth')
        try:
            for id_item in gt_list:
                abstract_text = get_abstract(id_item)
                try:
                    abstract_dict = to_dict(abstract_text, cell_name=cell_id)
                    cell_abstracts['documents'].append(abstract_dict)
                except Exception as e:
                    print('Exception with pmid:', id_item, e)
                    pass
        except Exception as e:
            print('Parsing error', e)
            pass
        if len(cell_abstracts['documents']) > 0:
            json.dump(cell_abstracts, fp=open(gt_path + cell_id + '.json', 'w'))


def process_pm(cell_):
    pm_path = 'data/cell_json_pm/'
    cell_id = cell_['accession']

    if os.path.exists(pm_path + cell_id + '.json'):
        print(cell_id, 'pubmed file already exists')
        pass
    else:
        cell_abstracts = dict()
        keyword_list = cell_['cell_name']
        query = list_toquery(keyword_list)
        idlist = search_idlist(query)

        # newref is the list of references that are not in idlist from search
        newref = list(set(idlist) - set(cell_['reference']))

        print(cell_id, len(idlist), 'abstracts from search', len(newref), 'abstracts to fetch')
        cell_abstracts['cell_id'] = cell_id
        cell_abstracts['documents'] = list()
        try:
            for id_item in newref:
                abstract_text = get_abstract(id_item)
                try:
                    abstract_dict = to_dict(abstract_text, cell_name=cell_id)
                    cell_abstracts['documents'].append(abstract_dict)
                except Exception as e:
                    print('Exception with pmid:', id_item, e)
                    pass
        except Exception as e:
            print('Parsing error', e)
            pass
        if len(cell_abstracts['documents']) > 0:
            json.dump(cell_abstracts, fp=open(pm_path + cell_id + '.json', 'w'))


def process_gt_pm(cell_):
    try:
        process_gt(cell_)
    except Exception as e:
        print('Exception when process_gt(', cell_,')\n', e)
        pass
    try:
        process_pm(cell_)
    except Exception as e:
        print('Exception when process_pm(', cell_, ')\n', e)
        pass
