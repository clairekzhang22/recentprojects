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
            current_compared_word = vec2words[i]
            for j in range(len(vec1words)):
                if current_compared_word == vec1words[j]:
                    similar_word_index_vec1.append(j)
                    similar_word_index_vec2.append(i)


        for k in range(len(similar_word_index_vec1)):
            vec1val = vec1num[similar_word_index_vec1[k]]
            vec2val = vec2num[similar_word_index_vec2[k]]
            top_sum += vec1val * vec2val

    if len(vec1words) < len(vec2words):
        for i in range(len(vec1words)):
            current_compared_word = vec1words[i]
            for j in range(len(vec1words)):
                if current_compared_word == vec2words[j]:
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

    #go sentance by sentance
    #check if the word alr exists in


    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            fulldict[sentences[i][j]] = 0
            #associated_dict[sentences[i][j]] = associated_dict[sentences[i][j]] + 1

    print(fulldict)

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

        txtlist = txtlist.replace("!",".")
        txtlist = txtlist.replace("?",".")
        txtlist = txtlist.split(".")
        text = text + txtlist


    for i in range(len(text)):
        val = [text[i].split()]
        list = list + val

    return build_semantic_descriptors(list)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    pass

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    pass
if __name__ == "__main__":
    #print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))


    filenames = ["message (1).txt"]
    print(build_semantic_descriptors_from_files(filenames))