import json
import os
import random

import inflect
import nltk
from flair.data import Sentence
from flair.models import SequenceTagger
from nltk import pos_tag, word_tokenize

# Download necessary data
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
from glob import glob

import numpy as np
import spacy

# Path to the file containing all descriptions
DESCRIPTIONS_FILE = "/media/SSD6/cigonzalez/data/caption-matching/ids.json"
# Directory where individual annotation files will be saved
ANNOTATIONS_DIR = "./interface_outputs_new_mapping"
SEMANTIC_LEVELS = [
    "exact",
    "synonyms",
    "hyponyms",
    "meronyms",
    "semantically_related",
]  # "synonyms",
METHODS = ["osprey", "ours"]
CATEGORIES = [
    "road",
    "sidewalk",
    "building",
    "wall",
    "fence",
    "pole",
    "traffic light",
    "traffic sign",
    "vegetation",
    "terrain",
    "sky",
    "person",
    "rider",
    "car",
    "truck",
    "bus",
    "train",
    "motorcycle",
    "bicycle",
    "None of the above",
]

tagger = SequenceTagger.load("pos")


def singularize(noun):
    p = inflect.engine()
    is_plural = pos_tag(word_tokenize(noun))[0][1] in ["NNS", "NNPS"]
    singular = p.singular_noun(noun) if is_plural else noun
    # Check if the singular form is a string
    if not isinstance(singular, str):
        singular = noun
    return singular


def map_to_dataset_categories(output, targets, sentences=True):
    def _match_category(c, semantic_relationships):
        if c in semantic_relationships:
            return (semantic_relationships[c]["id"], "exact")
        else:
            for r in SEMANTIC_LEVELS[1:]:
                for d in semantic_relationships.keys():
                    if c in semantic_relationships[d][r]:
                        return (semantic_relationships[d]["id"], r)
        return (-1, "NIV")

    def _get_match(noun, category, semantic_relationships):
        for r in SEMANTIC_LEVELS:
            if noun.lower().strip() in semantic_relationships[category][r]:
                return r
        return "NIV"

    nlp = spacy.load("en_core_web_sm")
    nouns = [] if sentences else output
    hyponyms, meronyms = [], []
    if sentences:
        for o in output:
            tags = Sentence(o)
            self.tagger.predict(tags)
            # tags = pos_tag(word_tokenize(o))
            o = nlp(o)

            hyponym, meronym = "", ""
            tokens = [t for t in o]
            text_tokens = [t.text for t in tokens]
            if "of" in text_tokens:
                idx = text_tokens.index("of")
                # find pattern a <word> of <word> or <word> of <word>
                if (
                    tokens[idx - 1].dep_ != "pobj"
                    and tokens[idx - 1].text != "full"
                    and (
                        idx - 1 >= 0
                        and tokens[0].dep_ == "det"
                        and tokens[0].text == "a"
                    )
                ):
                    hyponym = tokens[idx + 1 :]
                    hyponym = [
                        t for t in hyponym if t.dep_ == "pobj" or t.dep_ == "compound"
                    ]
                    # remove non-consecutive tokens
                    for i, t in enumerate(hyponym):
                        if i > 0:
                            if t.i != hyponym[i - 1].i + 1:
                                hyponym = hyponym[:i]
                                break
                    hyponym = " ".join([t.text for t in hyponym])
                    hyponym = singularize(hyponym)
                # find pattern the <word> of a <word>
                elif (
                    tokens[idx - 1].dep_ != "pobj"
                    and tokens[idx - 1].text != "made"
                    and tokens[idx - 1].text != "full"
                    and tokens[0].dep_ == "det"
                ):
                    meronym = tokens[idx + 1 :]
                    meronym = [t for t in meronym if t.dep_ != "det"]
                    meronym = " ".join([t.text for t in meronym])
                    meronym = singularize(meronym)
            if "on" in text_tokens:
                idx = text_tokens.index("on")
                # find pattern <word> on the <word>
                if (
                    tokens[idx - 1].dep_ != "pobj"
                    and tokens[idx - 1].text != "full"
                    and len(tokens) > idx + 2
                    and tokens[idx + 1].dep_ == "det"
                ):
                    meronym = tokens[idx + 2 :]
                    meronym = [
                        t for t in meronym if t.dep_ == "pobj" or t.dep_ == "compound"
                    ]
                    # remove non-consecutive tokens
                    for i, t in enumerate(meronym):
                        if i > 0:
                            if t.i != meronym[i - 1].i + 1:
                                meronym = meronym[:i]
                                break
                    meronym = " ".join([t.text for t in meronym])
                    meronym = singularize(meronym)
            noun = [
                t
                for i, t in enumerate(o)
                if (t.dep_ == "nsubj" or t.dep_ == "nsubjpass" or t.dep_ == "compound")
                # and tags[i].tag in ["NN", "NNS", "NNP", "NNPS"]
            ]
            if len(noun) == 0 or len([t for t in noun if t.dep_ != "compound"]) == 0:
                noun = [
                    t
                    for i, t in enumerate(o)
                    if (t.dep_ == "ROOT" or t.dep_ == "compound")
                    # and tags[i].tag in ["NN", "NNS", "NNP", "NNPS"]
                ]

            root = [
                t
                for t in noun
                if t.dep_ == "ROOT" or t.dep_ == "nsubj" or t.dep_ == "nsubjpass"
            ]
            # filter compound nouns that are not part of the root
            noun = [t for t in noun if t.i <= root[0].i]

            # remove adjectives
            if len(noun) > 1:
                noun = [t for t in noun if tags[t.i].tag not in ["JJ", "JJR", "JJS"]]

            noun = " ".join([t.text for t in noun])
            noun = singularize(noun)
            # print(
            #     f"sentence: {o}, noun: {noun}, hyponym: {hyponym}, meronym: {meronym}"
            # )

            nouns.append(noun)
            hyponyms.append(hyponym)
            meronyms.append(meronym)

    tmp = {
        r: torch.zeros([len(output), len(SEMANTIC_LEVELS) + 1]) for r in SEMANTIC_LEVELS
    }
    gt_relationships = [
        _get_match(
            self,
            n.lower().strip(),
            self.dataset_categories[targets[j]].lower().strip(),
            SEMANTIC_LEVELS,
        )
        for j, n in enumerate(nouns)
    ]
    gt_relationships = [
        SEMANTIC_LEVELS.index(r) if r != "NIV" else -1 for r in gt_relationships
    ]

    h_gt_relationships = [
        _get_match(
            self,
            h.lower().strip(),
            self.dataset_categories[targets[j]].lower().strip(),
            SEMANTIC_LEVELS,
        )
        for j, h in enumerate(hyponyms)
    ]
    h_gt_relationships = [
        SEMANTIC_LEVELS.index(r) if r != "NIV" else -1 for r in h_gt_relationships
    ]

    m_gt_relationships = [
        _get_match(
            self,
            m.lower().strip(),
            self.dataset_categories[targets[j]].lower().strip(),
            SEMANTIC_LEVELS,
        )
        for j, m in enumerate(meronyms)
    ]
    m_gt_relationships = [
        SEMANTIC_LEVELS.index(r) if r != "NIV" else -1 for r in m_gt_relationships
    ]
    for i, (n, h, m, gt_r, h_gt_r, m_gt_r) in enumerate(
        zip(
            nouns,
            hyponyms,
            meronyms,
            gt_relationships,
            h_gt_relationships,
            m_gt_relationships,
        )
    ):
        # consider compund nouns a single noun or multiple nouns
        match, r = _match_category(self, n, SEMANTIC_LEVELS)
        # if noun.split(" ") != 1:
        #     for j, n_ in enumerate(noun.split(" ")):
        #         match_, r_ = _match_category(self, n_, SEMANTIC_LEVELS)
        #         if SEMANTIC_LEVELS.index(r_) < r:
        #             match = match_
        #             r = r_
        h_match, h_r = _match_category(self, h, SEMANTIC_LEVELS)
        m_match, m_r = _match_category(self, m, SEMANTIC_LEVELS)
        h_r = SEMANTIC_LEVELS.index(h_r) if h_r != "NIV" else 0
        m_r = SEMANTIC_LEVELS.index(m_r) if m_r != "NIV" else 0
        r = SEMANTIC_LEVELS.index(r) if r != "NIV" else 0
        for j in range(len(SEMANTIC_LEVELS)):
            if SEMANTIC_LEVELS[j] in SEMANTIC_LEVELS:
                if j >= 2 and h != "":

                    gt_r = h_gt_r if h_gt_r < gt_r and h_gt_r >= 0 else gt_r
                    if h_r < r and h_r >= 0:
                        r = h_r
                        match = h_match
                if j >= 3 and m != "":

                    gt_r = m_gt_r if m_gt_r < gt_r and m_gt_r >= 0 else gt_r
                    if m_r < r and m_r >= 0:
                        r = m_r
                        match = m_match
                if j >= gt_r and gt_r >= 0:

                    tmp[SEMANTIC_LEVELS[j]][i, targets[i]] = 1
                else:

                    if j >= r:
                        tmp[SEMANTIC_LEVELS[j]][i, match] = 1
                    else:
                        tmp[SEMANTIC_LEVELS[j]][i, -1] = 1
    tmp = {k: torch.log(v + 1e-8) for k, v in tmp.items()}
    tmp.pop("sentence_bert")
    return tmp, nouns


# Load descriptions
with open(DESCRIPTIONS_FILE, "r", encoding="utf-8") as f:
    ids = json.load(f)

# Make a set of all descriptions
descriptions = {}
for method in METHODS:
    completly_different = 0
    hl_bert = 0
    hl_ours = {l: 0 for l in SEMANTIC_LEVELS}
    hl_differs = {l: 0 for l in SEMANTIC_LEVELS}
    hl_ours_any = 0
    hl_differs_all = 0
    # # Get all annotation files
    # files = glob(os.path.join(ANNOTATIONS_DIR, method, "*.json"))
    # ids = [os.path.basename(f).split(".")[0] for f in files]
    for id in ids[method]:
        with open(
            os.path.join(ANNOTATIONS_DIR, method, "{:}.json".format(id["id"])),
            "r",
            encoding="utf-8",
        ) as f:
            d = json.load(f)
        mapping, nouns = map_to_dataset_categories(
            [d["descrioption"]], [d["label"]], sentences=True
        )
        breakpoint()
        if [d[l] == d["bert"] for l in SEMANTIC_LEVELS].count(True) == 0:
            completly_different += 1
            if d["category"] == d["bert"]:
                print("Description: ", d["description"])
                print("Category: ", CATEGORIES[d["category"]])
                hl_bert += 1
            elif [d[l] == d["category"] for l in SEMANTIC_LEVELS].count(True) > 0:
                hl_ours_any += 1
            else:
                hl_differs_all += 1
            for l in SEMANTIC_LEVELS:
                if d["category"] == d[l]:
                    hl_ours[l] += 1
                    # if l == "semantically_related" and d["category"] != d["meronyms"]:
                    #     print(d["description"])
                    #     breakpoint()
                elif d["category"] != d[l] and d["category"] != d["bert"]:
                    hl_differs[l] += 1

    print("Method: ", method)
    print("Number of completly different descriptions: ", completly_different)
    # Prints statistics
    # Number of descriptions with the same category as the sentence_bert
    print(
        "Number of descriptions with the same category as the sentence_bert: ",
        hl_bert / completly_different,
    )
    print("Equal to ours at any semantic level: ", hl_ours_any / completly_different)
    print(
        "Different from both ours and sentence_bert at any semantic level: ",
        hl_differs_all / completly_different,
    )
    # Number of descriptions with the same category as ours per semantic level
    for l in SEMANTIC_LEVELS:
        print(
            "Number of descriptions with the same category as ours per semantic level: ",
            hl_ours[l] / completly_different,
        )
    # Number of descriptions differrent from both ours and sentence_bert per semantic level
    for l in SEMANTIC_LEVELS:
        print(
            "Number of descriptions differrent from both ours and sentence_bert per semantic level: ",
            hl_differs[l] / completly_different,
        )

        # if d["description"] not in descriptions:
        #     descriptions[d["description"]] = [
        #         "{:}_{:}_{:}".format(method, d["image_id"], d["segment_id"])
        #     ]
        # else:
        #     descriptions[d["description"]].append(
        #         "{:}_{:}_{:}".format(method, d["image_id"], d["segment_id"])
        #     )

# Keep descriptions only once
# new_ids = {method: [] for method in METHODS}
# for key in descriptions:
#     if len(descriptions[key]) > 1:
#         random.shuffle(descriptions[key])
#     method = descriptions[key][0].split("_")[0]
#     id = "_".join(descriptions[key][0].split("_")[1:])
#     new_ids[method].append({"id": id, "annotated": False})

# # Save the new ids
# with open(DESCRIPTIONS_FILE, "w", encoding="utf-8") as f:
#     json.dump(new_ids, f)
