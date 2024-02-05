# pip install serpapi FÖRST
# pip install google-search-results
from serpapi import GoogleSearch

def getSeach(swag, num):
    params = {
        "q": swag,
        #"location": loc,  # OPTIONAL
        "hl": "sv",  # OPTIONAL
        "gl": "se",  # OPTIONAL
        "google_domain": "google.se",
        "api_key": "5f4693b65a0e9d1a165d3581f1f4ab4dd2dab0a7a77248a0d09da6fa33d01821"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = results.get('organic_results', [])

    urls = [result.get('link') for result in organic_results[:num]] # NUMBER OF RESULTS

    return urls


#getSeach(["Umida Brands AB", "Urban Market Stockholm AB", "FRKY Foods AB"], "Stockholm County, Sweden", 4)
