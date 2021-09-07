import json
import operator
import string
import sys
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np



# for saving the stats
stats = {}
stats_filtered_stopwords = {}
stats_filtered_punctuations = {}
email_frequencies = {}
websites_Email_Counter = 0
website_doc_length = 0


def statistic(filename='res/loremipsum.txt'):
    with open(filename) as f:
        data = json.load(f)
        global websites_Email_Counter
        global website_doc_length
        stop_words = stopwords.words('english')

        for index in range(len(data)):  # this iterates through the range of list
            # for key in data[index]:  # this goes through each key value for each of the lists dicts
            #     print(data[index][key])
            emailDict = data[index]['emails']
            if emailDict:
                websites_Email_Counter += 1
                if emailDict is not None:
                    for item in emailDict :

                        if item in email_frequencies:
                            email_frequencies[item] += 1
                        else:
                            email_frequencies[item] = 1
            # print(websites_Email_Counter)
            body = data[index]['body']
            body = body.replace("\n", "").replace("\t", "")
            body = body.split(' ')
            #print(body)
            for word in body:
                if word != "":
                    website_doc_length += 1
                    if word in stats:
                        stats[word] += 1
                    else:
                        stats[word] = 1
            # tokenized stop words
            for word in body:
                if word != "" and word not in stop_words:
                    website_doc_length += 1
                    if word in stats_filtered_stopwords:
                        stats_filtered_stopwords[word] += 1
                    else:
                        stats_filtered_stopwords[word] = 1

            for word in body:
                if word != "" and word not in string.punctuation:
                    website_doc_length += 1
                    if word in stats_filtered_punctuations:
                        stats_filtered_punctuations[word] += 1
                    else:
                        stats_filtered_punctuations[word] = 1
        websites_Email_Counter = websites_Email_Counter / 1000
        website_doc_length = website_doc_length / 1000


def print_stats():
    '''
    Prints the gathered text statistics to the console by iterating over
    the `stats` dict.
    '''
    # for key in stats:
    #     print('The word "{word}" is {num} times in the text.'.format(word=key, num=stats[key]))
    print("doc_len: ", website_doc_length)
    print('Emails:')

    for key in dict(sorted(email_frequencies.items(), key=operator.itemgetter(1), reverse=True)[:10]):
        print('\t("{word}", {num})'.format(word=key, num=email_frequencies[key]))

    print('perc: {webperc}'.format(webperc=websites_Email_Counter))

    print('\n\n')
    print_format('stats',stats)
    print('\n\n')
    print_format('stats_filtered_stopwords',stats_filtered_stopwords)
    print('\n\n')
    print_format('stats_filtered_punctuations',stats_filtered_punctuations)
    # global stats
    # global stats_filtered_stopwords

    # stats = dict(sorted(stats.items(), key=operator.itemgetter(1), reverse=True)[:30])
    # stats_filtered_stopwords = dict(sorted(stats_filtered_stopwords.items(), key=operator.itemgetter(1), reverse=True)[:30])

    # print('''
    #       rank  term        freq.    perc.    rank  term           freq.    perc.
    #     ------  --------  -------  -------  ------  -----------  -------  -------
    #     ''')




def print_format(log_name, word_dict):

    rank = [i for i in range(1,31)]
    stats = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:30])
    key_list = list(stats.keys())
    value_list = list(stats.values())
    #print(key_list,value_list)

    print("{:<10s} {:<10s} {:<10s} {:<10s} {:<10s} {:<10s} {:<10s} {:<10s}".format("rank", "term", "freq", "perc", "rank","term", "freq", "perc"))
    print("{:10} {:10} {:10} {:10} {:10} {:10} {:10} {:10}".format("--------", "--------", "--------", "--------", "--------", "--------", "--------", "--------"))
    second_column_rank = 16
    for i in range(1, 16):
        perc1 = float("{0:.2f}".format(value_list[i - 1] / website_doc_length))
        perc2 = float("{0:.2f}".format(value_list[i + 14] / website_doc_length))
        print('{rank:<10} {term:<10} {freq:^12} {perc:<10} {rank2:<10} {term2:<10} {freq2:^10} {perc2:<10}'.format(rank=i,term=key_list[i - 1],freq=value_list[i - 1],perc=perc1,rank2=second_column_rank,term2=key_list[i + 14],freq2=value_list[i + 14],perc2=perc2))
        second_column_rank += 1

    log_print(log_name,np.array(rank),np.array(value_list))

def log_print(log_name,x ,y): #x is rank y is freq
    plt.figure(figsize=(4,3), dpi=70)
    plt.loglog(x,y)
    plt.savefig("{name}.png".format(name = log_name))


def main():
    # check if there are filenames specified during script call
    if len(sys.argv) > 1:
        # if so, the script iterates over the indices of the arguments
        for i in range(len(sys.argv)):  # ==> take every indice from [0, 1]
            # ignore the scriptname as input
            if i != 0:
                statistic(sys.argv[i])
    else:
        # standard case if no filename is given as argument
        statistic()
    print_stats()


if __name__ == '__main__':
    main()
