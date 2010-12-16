import re

def slugify_search_query(text):
    from content.utils import normalize_query
    import re

    norm_query = normalize_query(text)
    pattern = re.compile('[^a-zA-Z0-9+]')
    alph_norm_query = [re.sub(pattern,'',t.replace(' ','+')) for t in norm_query]
    return "_".join(alph_norm_query)

def unslugify(text):
    return [t.replace('+',' ') for t in text.split('_')]

def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    """
    Splits the query string in invidual keywords, getting rid of unecessary spaces
    and grouping quoted words together.
    Example:
    >>> normalize_query('  some+random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 
    
def get_search_query(query_string, search_fields):
    """
    Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.
    """
    from django.db.models import Q
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query
