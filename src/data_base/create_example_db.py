from os import curdir
import sqlite3 as sq
from datetime import datetime, timedelta

# Надо понять, а как это нормально делают, с учетом того,
# что вводимые данные = структуры из Python
# https://youtu.be/pd-0G0MigUA?t=1078
# надо переписать с использованием sqlalchemy
# https://docs.sqlalchemy.org/en/14/dialects/sqlite.html

base = None
cur = None

def connect_to_db():
    global base, cur
    # base = sq.connect(':memory:')
    base = sq.connect('example.db')
    base.row_factory = sq.Row    
    cur = base.cursor()
    if base:
        print('Connection was successful')
        

def create_table(name, types,values):
    # types = ['date TEXT', 'title TEXT PRIMARY KEY', 'start DATE']
    
    # create_table = 'CREATE TABLE IF NOT EXISTS ' + name + \
    create_table = 'CREATE TABLE ' + name + \
        '(' + ', '.join(types) + ')'
    print(create_table)
    base.execute(create_table)    
    short_types  = [ item.split(' ')[0] for item in types if 'KEY' not in item ]
    insert_name = 'INSERT INTO ' + name + \
        '(' + ', '.join(short_types) + ')'
    for item in values:
        insert = insert_name+  ' VALUES ('+ ('?, '*(len(types)-1))[:-2]+');'
        print(f"insert = {insert}")
        cur.execute(insert, tuple(item))
    base.commit()


def sql_search_by_author(author_name: tuple):
    print(f"author_name = {author_name}")
    print(f"len(author_name) = {len(author_name)}")
    request =  """        
        SELECT report_id as 'Индекс',
            group_concat(name_author) as 'Авторы',
            title as 'Название',
            link as 'Сслыка на статью'
        FROM author
            INNER JOIN report_author USING(author_id)
            INNER JOIN report USING(report_id)
        GROUP BY report_id
        HAVING group_concat(name_author) LIKE ?
        ORDER BY report_id       
        """
    print(f'request = {request}')
    cur.execute(request,author_name)
    
    output = cur.fetchall()
    return output

def sql_timetable_select(t1vote:tuple):
    request = """
                SELECT timetable_description,
                        event_beg,
                        event_end,
                        name_location,
                        name_author,
                        title,
                        link
                FROM timetable
                    INNER JOIN location USING(location_id)
                    INNER JOIN report USING(report_id)
                    INNER JOIN report_author USING(report_id)
                    INNER JOIN author USING(author_id)
                WHERE event_beg > ?
                    AND event_beg < ?
                GROUP BY timetable_description;
              """
    print(f"request = {request}, t1vote = {t1vote}")   
    return cur.execute(request, t1vote).fetchall()
    # return cur.execute(request).fetchall()


connect_to_db()


report_name = 'report'
report_types = ['report_id INTEGER PRIMARY KEY', 'title TEXT NOT NULL', 'link TEXT' ]
report_values = [[' A Trade-off between ML and DL Techniques in Natural Language Processing', 'https://iopscience.iop.org/article/10.1088/1742-6596/1831/1/012025/meta'],
                 [' Understanding COVID-19 news coverage using medical NLP', 'https://arxiv.org/abs/2203.10338'],
                 [' Fake News Classification Based on Content Level Features', 'https://www.mdpi.com/1460538'],
                 [' Selecting NLP Classification Techniques to Better Understand Causes of Mass Killings','https://link.springer.com/chapter/10.1007/978-3-031-10464-0_46']]
create_table(report_name, report_types, report_values)


# https://www.sqlite.org/foreignkeys.html
abstract_name = 'abstract'
abstract_types = ['abstract_id INTEGER PRIMARY KEY', 'report_id INTEGER NOT NULL', 'text_abstract TEXT NOT NULL']
abstract_values = [['1', ''' The domain of Natural Language Processing covers various tasks, such as classification, text generation, and language model. The data processed using word embeddings, or vectorizers, is then trained using Machine Learning and Deep Learning algorithms. In order to observe the tradeoff between both these types of algorithms, with respect to data available, accuracy obtained and other factors, a binary classification is undertaken to distinguish between insincere and regular questions on Quora. A dataset called Quora Insincere Questions Classification was used to train various machine learning and deep learning models. A Bidirectional-Long Short Term Network (LSTM) was trained, with the text processed using Global Vectors for Word Representation (GloVe). Machine Learning algorithms such as Extreme Gradient Boosting classifier, Gaussian Naive Bayes, and Support Vector Classifier (SVC), by using the TF-IDF vectorizer to process the text. This paper also presents an evaluation of the above algorithms on the basis of precision, recall, f1 score metrics.'''],
                 ['2', ''' Being a global pandemic, the COVID-19 outbreak received global media attention. In this study, we analyze news publications from CNN and The Guardian - two of the world’s most influential media organizations. The dataset includes more than 36,000 articles, analyzed using the clinical and biomedical Natural Language Processing (NLP) models from the Spark NLP for Healthcare library, which enables a deeper analysis of medical concepts than previously achieved. The analysis covers key entities and phrases, observed biases, and change over time in news coverage by correlating mined medical symptoms, procedures, drugs, and guidance with commonly mentioned demographic and occupational groups. Another analysis is of extracted Adverse Drug Events about drug and vaccine manufacturers, which when reported by major news outlets has an impact on vaccine hesitancy'''],
                 ['3', ''' Due to the openness and easy accessibility of online social media (OSM), anyone can easily contribute a simple paragraph of text to express their opinion on an article that they have seen. Without access control mechanisms, it has been reported that there are many suspicious messages and accounts spreading across multiple platforms. Accordingly, identifying and labeling fake news is a demanding problem due to the massive amount of heterogeneous content. In essence, the functions of machine learning (ML) and natural language processing (NLP) are to enhance, speed up, and automate the analytical process. Therefore, this unstructured text can be transformed into meaningful data and insights. In this paper, the combination of ML and NLP are implemented to classify fake news based on an open, large and labeled corpus on Twitter. In this case, we compare several state-of-the-art ML and neural network models based on content-only features. To enhance classification performance, before the training process, the term frequency-inverse document frequency (TF-IDF) features were applied in ML training, while word embedding was utilized in neural network training. By implementing ML and NLP methods, all the traditional models have greater than 85% accuracy. All the neural network models have greater than 90% accuracy. From the experiments, we found that the neural network models outperform the traditional ML models by, on average, approximately 6% precision, with all neural network models reaching up to 90% accuracy. '''],
                 ['4', ''' We perform an analysis of SVM, BERT, and Longformer NLP tools as applied to large volumes of unclassified news articles given small volumes of labeled news articles for training. Analysis of the target machine learning tools is performed through a case study of global trigger events; specifically triggers of state-led mass killings. The goal of the case study is to draw relationships from the millions of machine classified articles to identify trends for the prediction and prevention of future mass killing events. In this paper we focus on the classification one specific trigger, coups, in order to glean insight into the accuracy and complexity of our SVM, BERT, and Longformer models. This study centers on classifying which news articles contain uniquely defined coup events and the temporal placement of those articles. Our performance analysis centers on the comparison of multiple accuracy metrics as applied to specific subsets of the corpus. We also demonstrate that raw accuracy scores are insufficient to fully understand the quality of classification required for specific target use cases.''']]
create_table(abstract_name, abstract_types, abstract_values)


author_name = 'author'
author_types = ['author_id INTEGER PRIMARY KEY', 'name_author TEXT NOT NULL', 'contact_info TEXT NOT NULL']
author_values = [[' Bhavesh Singh', ' bhavesh.singh@djsce.edu.in Dwarkadas J. Sanghvi College of Engineering, Mumbai - 400056, India'],
                 [' Rahil Desai', ' rahil.desai@djsce.edu.in Dwarkadas J. Sanghvi College of Engineering, Mumbai - 400056, India '],
                 [' Himanshu Ashar', ' himanshu.ashar@djsce.edu.in Dwarkadas J. Sanghvi College of Engineering, Mumbai - 400056, India'],
                 [' Ali Emre Varol', ' emre@johnsnowlabs.com John Snow Labs inc. 16192 Coastal Highway, Lewes, DE 19958, USA'],
                 [' Veysel Kocaman', ' veysel@johnsnowlabs.com John Snow Labs inc. 16192 Coastal Highway, Lewes, DE 19958, USA'],
                 [' Hasham Ul Haq', ' hasham@johnsnowlabs.com John Snow Labs inc. 16192 Coastal Highway, Lewes, DE 19958, USA'],
                 [' David Talby', ' david@johnsnowlabs.com John Snow Labs inc. 16192 Coastal Highway, Lewes, DE 19958, USA'],
                 [' Chun-Ming Lai', ' cmlai@thu.edu.tw Department of Computer Science, Tunghai University, Taichung City 407224, Taiwan'],
                 [' Mei-Hua Chen', ' mhchen@thu.edu.tw Department of Foreign Languages and Literature, Tunghai University, Taichung City 407224, Taiwan'],
                 [' Vinod Kumar Verma', ' vinod5881@gmail.com Department of Computer Science & Engineering, Sant Longowal Institute of Engineering & Technology, (SLIET), Longowal 148106, India'],
                 [' Abigail Sticha', ' asticha@nd.edu University of Notre Dame, Notre Dame, IN, 46556, USA'],
                 [' Paul Brenner', ' asticha@nd.edu University of Notre Dame, Notre Dame, IN, 46556, USA']]
create_table(author_name, author_types, author_values)

report_author_name = 'report_author'
report_author_types = ['report_author_id INTEGER PRIMARY KEY', 'report_id INTEGER NOT NULL', 'author_id INTEGER NOT NULL']
report_author_values = [['1', '1'],
                 ['1', '2'],
                 ['1', '3'],
                 ['2', '4'],
                 ['2', '5'],
                 ['2', '6'],
                 ['2', '7'],
                 ['3', '8'],
                 ['3', '9'],
                 ['3', '10'],
                 ['4', '11'],
                 ['4', '12']]
create_table(report_author_name, report_author_types, report_author_values)


voting_name = 'voting'
voting_types = ['vote_id INTEGER PRIMARY KEY', 'report_id INTEGER NOT NULL', 'telegram_id INTEGER NOT NULL', 'vote INTEGER']
voting_values = [['1', ' 1015489742158', '1'],
                 ['1', ' 2342342523523', '1'],
                 ['1', ' 5345345123678', '1'],
                 ['2', ' 1015489742158', '1'],
                 ['2', ' 2342342523523', '0'],
                 ['2', ' 5345345123678', '1'],
                 ['3', ' 1015489742158', '0'],
                 ['4', ' 2342342523523', '1'],
                 ['4', ' 5345345123678', '1'],
                 ['4', ' 9081209321342', '1'],
                 ['4', ' 7623786420234', '1']]
                 
                 
create_table(voting_name, voting_types, voting_values)


location_name = 'location'
location_types = ['location_id INTEGER PRIMARY KEY',
                  'name_location TEXT',
                   'location_description TEXT']
location_values = [['Hall 1', '321 Shoreline Lake, Sun Frutto, ML 194216'],
                   ['Hall 2', '323 Shoreline Park, Sun Frutto, DL 194216']]
create_table(location_name,location_types,location_values)

# reqname = ("%Голов%",)
# print(reqname)
# print(type(reqname))
# output = sql_search_by_author(reqname)
# print(output)


# UTC, Временные зоны нужны, когда я могу получить зону от пользователя.
# Но если все пользователи точно будут в одной временной зоне, то ... 
# Не надо применять временные зоны ...

beg_time = datetime(2022, 8, 25, 8)
# print('dt.isoformat(): ',beg_time.isoformat())
dt_m=timedelta(minutes = 15)
dt_d=timedelta(days = 1)
# print('dt_m: ', dt_m, type(dt_m))
# print('dt_d: ', dt_d, type(dt_d))
kvals = list(range(1,3))
timetable_values = [((beg_time + (i)*dt_m + j*dt_d).isoformat(),
              (beg_time + (i+1)*dt_m + j*dt_d).isoformat(),
              f'speech {i*len(kvals)+k} in hall {k} of day = {j+1} ',
              k,
              (i*len(kvals)+k-1)%4+1, )
              for j in range(5) for i in range(12*4) for k in kvals]

timetable_name = 'timetable'
timetable_types = ['timetable_id INTEGER PRIMARY KEY',
                   'event_beg TEXT', 'event_end TEXT',
                   'timetable_description TEXT',
                   'location_id INTEGER NOT NULL',
                   'report_id INTEGER NOT NULL']
create_table(timetable_name, timetable_types, timetable_values)

answ = sql_timetable_select(('2022-08-18T10:10:00','2022-08-18T10:50:00',)) 
for item in answ:    
    print(item.keys())
    print(len(item))
    print([item[ikeys] for ikeys in item.keys()])
    for vals in item:
        print(vals)
    # print(item.values())
# print(answ.keys())

base.close()

# """SELECT report_id as "Номер доклада", SUM(vote) as "Количество голосов"
# FROM voting
# GROUP BY report_id
# ORDER BY "Количество голосов" DESC
# LIMIT 3;
# """

# SELECT report_id as "ID доклада",
# 	   title as "Название доклада",
# 	   SUM(vote) as "Количество голосов"
# FROM voting 
# 	INNER JOIN report USING(report_id)
# GROUP BY report_id
# ORDER BY "Количество голосов" DESC