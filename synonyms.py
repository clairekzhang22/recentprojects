'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    vec1words = list(vec1.keys())
    vec2words = list(vec2.keys())
    vec1num = list(vec1.values())
    vec2num = list(vec2.values())

    vec1mag = 0
    for i in range(len(vec1num)):
        vec1mag += (vec1num[i] ** 2)
    vec2mag = 0
    for i in range(len(vec2num)):
        vec2mag += (vec2num[i] ** 2)

    bottom_magnitude = (vec1mag * vec2mag) ** 0.5

    similar_word_index_vec1 = []
    similar_word_index_vec2 = []
    top_sum = 0

    if len(vec1words) >= len(vec2words):
        for i in range(len(vec2words)):
            for j in range(len(vec1words)):
                if vec2words[i] == vec1words[j]:
                    similar_word_index_vec1.append(j)
                    similar_word_index_vec2.append(i)

        for k in range(len(similar_word_index_vec1)):
            vec1val = vec1num[similar_word_index_vec1[k]]
            vec2val = vec2num[similar_word_index_vec2[k]]
            top_sum += vec1val * vec2val

    if len(vec1words) < len(vec2words):
        for i in range(len(vec1words)):
            for j in range(len(vec2words)):
                if vec1words[i] == vec2words[j]:
                    similar_word_index_vec2.append(j)
                    similar_word_index_vec1.append(i)

        for k in range(len(similar_word_index_vec2)):
            vec1val = vec1num[similar_word_index_vec1[k]]
            vec2val = vec2num[similar_word_index_vec2[k]]
            top_sum += vec1val * vec2val

    cos_sim = top_sum / bottom_magnitude
    return (cos_sim)

def build_semantic_descriptors(sentences):
    fulldict = {}

    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            associated_dict = {}
            associated_words = []


            if sentences[i][j] in fulldict:
                associated_dict = fulldict.get(sentences[i][j])
                for l in range(len(sentences[i])):
                    associated_words.append(sentences[i][l])
                associated_words.remove(sentences[i][j])
                for k in range(len(associated_words)):
                    if associated_words[k] in associated_dict:
                        associated_dict[associated_words[k]] += 1
                    else:
                        associated_dict[associated_words[k]] = 1

            else:
                for l in range(len(sentences[i])):
                    associated_words.append(sentences[i][l])
                associated_words.remove(sentences[i][j])
                for k in range(len(associated_words)):
                    if associated_words[k] in associated_dict:
                        associated_dict[associated_words[k]] += 1
                    else:
                        associated_dict[associated_words[k]] = 1

            fulldict[sentences[i][j]] = associated_dict

    return fulldict

def build_semantic_descriptors_from_files(filenames):
    text = []
    list = []

    for i in range(len(filenames)):
        txtlist = open(filenames[i], encoding="latin1").read().lower()
        txtlist = txtlist.replace(",","")
        txtlist = txtlist.replace("--","")
        txtlist = txtlist.replace("-","")
        txtlist = txtlist.replace(";","")
        txtlist = txtlist.replace(":","")

        txtlist = txtlist.replace("\n"," ")
        txtlist = txtlist.replace("'"," ")

        txtlist = txtlist.replace("!",".")
        txtlist = txtlist.replace("?",".")
        txtlist = txtlist.split(".")
        text = text + txtlist


    for i in range(len(text)):
        val = [text[i].split()]
        list = list + val

    list[:] = (item for item in list if item != [])

    return build_semantic_descriptors(list)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    sim_compare = []
    for i in range(len(choices)):
        if word in semantic_descriptors and choices[i] in semantic_descriptors:
            vector_word = semantic_descriptors[word]
            vector_choice = semantic_descriptors[choices[i]]
            sim_value = similarity_fn(vector_word,vector_choice)
        else:
            sim_value = -1

        sim_compare.append(sim_value)

    most_sim_index = sim_compare.index(max(sim_compare))
    return choices[most_sim_index]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    test_count = 0
    correct_count = 0
    list = []

    txtlist = open(filename, encoding="latin1").read()
    txtlist = txtlist.split("\n")
    for i in range(len(txtlist)):
        val = [txtlist[i].split()]
        list = list + val
    list[:] = (item for item in list if item != [])


    for i in range(len(list)):
        ans = list[i][1]
        match_ans = most_similar_word(list[i][0],list[i][2::],semantic_descriptors, similarity_fn)
        test_count += 1

        if ans == match_ans:
            correct_count += 1

    return (correct_count / test_count) * 100


if __name__ == "__main__":
    # print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

#     sentences = [["i", "am", "a", "sick", "man"],
# ["i", "am", "a", "spiteful", "man"],
# ["i", "am", "an", "unattractive", "man"],
# ["i", "believe", "my", "liver", "is", "diseased"],
# ["however", "i", "know", "nothing", "at", "all", "about", "my",
# "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
#     print(build_semantic_descriptors(sentences))

    #filenames = ["message (1).txt"]
    # filenames = ["test1.txt"]
    # print(build_semantic_descriptors_from_files(filenames))


    # word = "draw"
    # choices = ["paint","walk"]
    # semantic_descriptors = build_semantic_descriptors_from_files(["syntest1.txt","syntest.txt"])
    # similarity_fn = cosine_similarity
    #
    #     # if cannot be computed = -1 (what scenario would it not be computed?) --> not in semantic des, or no similar words
    # print(most_similar_word(word, choices, semantic_descriptors, similarity_fn))


    sem_descriptors = build_semantic_descriptors_from_files(["syntest.txt", "syntest1.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")
