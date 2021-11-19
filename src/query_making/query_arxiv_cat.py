"""QueryArXivCat class definition, used to retrieve arXiv following the arXiv
API : https://arxiv.org/help/api/user-manual"""

import time
import re
import traceback
import logging
import requests
import feedparser
import pandas as pd

class QueryArXivCat:
    """This class retrieve all URLs of e-prints of categories contained in
    `categories`.

    :param result_folder: Path to the result folder where .csv data will be
        stored.
    :type result_folder: :class: `pathlib.PurePath`

    :param category: arXiv category.
    :type category: str

    :param cyber_keywords: Pre-formated queries of security considerations keywords.
    :type cyber_keywords: str"""

    __URL = 'http://export.arxiv.org/api/query'
    __PARAMS = {
        'search_query': '',
        'start': 1,
        'max_results': 1,
        'sortBy': 'submittedDate',
        'sortOrder': 'ascending'
    }
    def __init__(self, result_folder, category, cyber_keywords=None) :
        #: `pandas.Series` which contain categories
        self.category = category
        #: Path to the result folder
        self.result_folder = result_folder
        #: Formated query of security considerations keywords
        self.cyber_keywords = cyber_keywords

        #: Number max of loop, if a query doesn't work
        self.MAX_LOOP = 20
        #: Number of wanted result per query
        self.MAX_QUERY_RESULT = 1000
        #: arXiv API doesn't allow to retrieve more than 50 000 e-prints
        self.ARXIV_LIMIT = 50000

    @staticmethod
    def get_arxiv_path(paper_id, category, version):
        """Create the arXiv path.

        :param paper_id: id of the e-print.
        :type paper_id: str

        :param category: category of the paper (if category == 'abs' then it uses only the `paper_id`).
        :type category: str

        :param version: version of the e-print.
        :type version: str"""
        # e-print newer than 2007
        if category == 'abs':
            return ''.join(['arxiv/pdf/', paper_id[:4], '/', paper_id, 'v', version, '.pdf'])
        return ''.join([category, '/pdf/', paper_id[:4], '/', paper_id, 'v', version, '.pdf'])

    def processing(self):
        """Execute queries on arXiv"""
        # Number max of result for this category
        category = self.category
        if self.cyber_keywords is None:
            max_results = self.__get_max_results('cat:{}'.format(category))
        else:
            print('cyber')
            max_results = self.__get_max_results('cat:{}'.format(category)
                                                 + ' AND '
                                                 + self.cyber_keywords)

        print('Max articles : ' + str(max_results))

        # Init parameters
        parameters = dict(self.__PARAMS)
        parameters['max_results'] = self.MAX_QUERY_RESULT

        # Total dataframes
        total_data = []

        # Little trick to pass throught the arxiv limit
        if max_results <= self.ARXIV_LIMIT:
            self.get_eprints(parameters,
                              max_results,
                              category,
                              total_data)
        elif max_results <= 2 * self.ARXIV_LIMIT:
            total_data = self.get_eprints(parameters,
                                           self.ARXIV_LIMIT,
                                           category,
                                           total_data)
            # Re ordering
            parameters['sortOrder'] = 'descending'
            self.get_eprints(parameters,
                              max_results - self.ARXIV_LIMIT,
                              category,
                              total_data)
        else:
            raise RuntimeError('Error, too much e-prints')

    def get_eprints(self, parameters, max_results, category, total_data):
        """Get all eprints of a category

        :param parameters: restAPI parameters.
        :type parameters: dict

        :param max_results: number of eprints to retrieve.
        :type max_results: int

        :param category: name of the desired category to retrieve.
        :type category: str

        :param total_data: list of eprints already retrieved.
        :type total_data: [:class:`pandas.DataFrame`]"""
        # Offset of the query
        offset = 0
        # Number of articles retrieved
        nb_articles = 0
        # Number max of unsuccessful queries
        max_loop = self.MAX_LOOP
        while max_loop != 0 and nb_articles < max_results:
            # Query with MAX_QUERY_RESULT results
            parameters['start'] = offset
            if self.cyber_keywords is None:
                parameters['search_query'] = 'cat:{}'.format(category)
            else:
                parameters['search_query'] = ('cat:{}'.format(category)
                                              + ' AND '
                                              + self.cyber_keywords)
            # Do the request
            req = self.__do_request_req(parameters)
            # Get data of the retrieve page
            query_data = {'id': [],
                          'published': [],
                          'updated': [],
                          'version': [],
                          'primary_category': [],
                          'all_categories': [],
                          'arxiv_path': [],
                          'http_link': []}

            for entry in feedparser.parse(req.text).entries:
                # Get information from the link
                match = re.match('http.*/(.*)/(.*)v(.*)', entry.id)

                query_data['id'].append(match.group(2))
                query_data['published'].append(entry.published)
                query_data['updated'].append(entry.updated)
                query_data['version'].append(match.group(3))
                query_data['primary_category'].append(entry.arxiv_primary_category['term'])
                query_data['all_categories'].append([tag['term'] for tag in entry.tags])
                query_data['arxiv_path'].append(self.get_arxiv_path(
                    match.group(2),
                    match.group(1),
                    match.group(3)))
                query_data['http_link'].append(entry.link \
                                          .replace('http://', 'http://export.') \
                                          .replace('abs', 'pdf') \
                                          + '.pdf')
            nb_data = len(query_data['id'])
            # Avoid infinite looping
            if nb_data == 0 :
                max_loop -= 1
            else :
                max_loop = 20

            # Shifting
            nb_articles += nb_data
            offset = nb_articles

            # Append actual data to get the total
            total_data.append(pd.DataFrame(query_data))
            # Write into csv
            if self.cyber_keywords is None:
                pd.concat(total_data, ignore_index=True).to_csv(
                    self.result_folder.joinpath(category + '.csv'),
                    mode='w')
            else:
                pd.concat(total_data, ignore_index=True).to_csv(
                    self.result_folder.joinpath(category + '_cyber.csv'),
                    mode='w')

            # Debug
            print('Category : {}; Article retrieved {}' \
                  .format(category, nb_articles))

            # Requested by arXiv API
            time.sleep(3)
        return total_data

    def __do_request_req(self, parameters, i=0):
        """Recursive function for retry request if a bug occur.

        :param parameters: restAPI parameters.
        :type parameters: dict

        :param i: recursive counter.
        :type i: int"""
        try:
            print(str(i) + ' attempt')
            return requests.get(self.__URL, params=parameters)
        except KeyboardInterrupt:
            # If ^C stop the infinite loop
            logging.error(traceback.format_exc())
            return None
        except Exception as e:
            # Retry if another error occur
            logging.error(traceback.format_exc())
            return self.__do_request_req(parameters, i + 1)


    def __get_max_results(self, search_query):
        """Do a request to obtain the size of a category.

        :param search_query: formated query.
        :type search_query: str"""

        parameters = dict(self.__PARAMS)
        parameters['search_query'] = search_query
        parameters['start'] = 1
        parameters['max_results'] = 0

        req = self.__do_request_req(parameters)
        return int(feedparser.parse(req.text)['feed']['opensearch_totalresults'])
