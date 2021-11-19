from multiprocessing import Pool
import nltk
import pandas as pd
import fitz

from ..NLP_tools.nlp import NLP

def process_opinion(index_path):
    """Processes an e-print.

    :param index_path: contain the :class:`pandas.DataFrame` index and the path to this e-print."""
    index = index_path[0]
    path = str(index_path[1])
    print('Start : ' + path)
    try:
        # Open file
        try:
            pdf_file = fitz.open(path)
        except:
            pdf_file = fitz.open(path[:-5] + '1.pdf')

        text = ''.join([page.getText() for page in pdf_file])
        pdf_file.close()

        nlp = NLP()
        return {'index': index,
                'opinion': nlp.opinion(nlp.cleaning(text))}
    except Exception as e:
        # On error occured
        print('error file : ' + str(e))
        return {'index': index,
                'opinion': -5.}

class OpinionProcessing:
    """This class spawns process. Each of them computes the opinion of
    e-prints.

    :param e_prints_path: :class:`pandas.Series` of path to e-prints, indexed by their dates.
    :type e_prints_path: :class:`pandas.Series`

    :param output_path: Path to save the calculated opinion.
    :type output_path: str

    :param crtc_name: name of the current CRTC, used to name the result folder.
    :type crtc_name: str"""
    def __init__(self,
                 serie_path,
                 output_path,
                 crtc_name):
        # nltk initialisation

        # Importing the dictionary (lexicon) of opinion words
        # (from Bing Liu and collaborators
        # (https://www.cs.uic.edu/~liub/FBS/opinion-analysis.html))
        nltk.download('opinion_lexicon')
        # Cleaning the dataset from common english words
        nltk.download('stopwords')
        # Wordnet is a lexical database for the English language that helps
        # the script determine the base word
        nltk.download('wordnet')

        #: :class:`pandas.Series` of all articles path
        self.serie_path = serie_path
        #: Size of the :attr:`self.serie_path`
        self.nb_paths = len(list(serie_path))

        # For save results
        #: Destination folder for computed articles
        self.output_path = output_path
        #: Used for the construction the final .csv
        self.opinion_list = {'index': [], 'opinion': []}
        #: Name of the CRTC
        self.crtc_name = crtc_name
        #: Detected errors
        self.errors = 0


    def process_result_pool(self, result) -> None:
        """Stocks the result into a .csv file.

        :param result: opinion and index of the e-print to be saved.
        :type result: dict"""
        # Save into a file if no errors occured
        opinion_list = self.opinion_list
        if result['opinion'] > -4. :
            opinion_list['index'].append(result['index'])
            opinion_list['opinion'].append(result['opinion'])
            # Use panda to stock data into csv
            df = pd.DataFrame(data={'opinion': opinion_list['opinion']},
                              index=opinion_list['index'])

            df.to_csv(self.output_path.joinpath(self.crtc_name + '.csv'),
                      mode='w')
        else :
            self.errors += 1

    def processing(self, process_number: int):
        """Creates all process and wait to their returns.

        :param process_number: number max of ongoing processes.
        :type process_number: int"""
        i = 0
        with Pool(process_number) as pool:
            for res in pool.imap_unordered(process_opinion,
                                           zip(self.serie_path.index,
                                               self.serie_path.values)):
                self.process_result_pool(res)
                print('Get ' + str(i))
                i += 1
        print(self.errors)
