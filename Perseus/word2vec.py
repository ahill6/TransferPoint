# imports needed and logging
import gzip
import gensim 
import logging
logging.basicConfig(format=’%(asctime)s : %(levelname)s : %(message)s’, level=logging.INFO)

-- pass in paragraphs (word2vec wants sentences, but passing in full paragraphs as sentences works)
    -- and is easier than trying to guess/infer sentences (is there punctuation?)
        -- consistently I mean
# TODO - <p> will generally work, but some files are broken out purely by lines.  
#   however, those usually have <divX> for some number X (find biggest number?)
# RUN EXPERIMENT TO SEE HOW MANY OF THE FILES HAVE PARAGRAPHS, WHICH DO NOT

-- transform them into dictionary forms first (do something about the unsure attributions)
    ** especially what do you do about the ones that are attributed to 25 different ea% things??


def read_input(input_file):
    """This method reads the input file which is in gzip format"""

    logging.info("reading file {0}...this may take a while".format(input_file))
    with gzip.open(input_file, 'rb') as f:
        for i, line in enumerate(f):

            if (i % 10000 == 0):
                logging.info("read {0} reviews".format(i))
            # do some pre-processing and return list of words for each review
            # text
            yield gensim.utils.simple_preprocess(line)

            # TODO - need to change preprocessing (likely do my own) so that to_lower, etc. works
            # for GKC


    # build vocabulary and train model
    model = gensim.models.Word2Vec(
        documents,
        size=150,
        window=10,
        min_count=2,
        workers=10)
    ''' parameters in model training:
        size        size of the dense vector used to represent each word.
                        little available data = should be smaller.
                        Engineering decision.  100-150 works well for demo-writer in English
        window      max distance bteweeen target word and neighboring word (exactly same as my window var)
                        if enough data, shouldn't matter (within reason).  suggests use default
        min_count   model ignores words that do not satisfy min_count
                        if enough data, shouldn't matter
        


    model.train(documents, total_examples=len(documents), epochs=10)

    # demo from example, not purely analogous here
    w1 = 'dirty'
    model.wv.most_similar(positive=w1)

    # look up 6 words similar to 'polite'
    w1 = ['polite']
    model.wv.most_similar(positive=w1, topn=6)

    # copute (cosine) similarity for two different words
    model.wv.similarity(w1='france', w2='dirty')

