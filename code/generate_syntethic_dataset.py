import random
import pandas as pd

# Sinónimos y frases base
synonyms_good = [
    ["loved", "really liked", "was fascinated by", "was delighted with", "enjoyed", "was pleased with"],
    ["resistant", "durable", "solid", "firm", "robust", "strong"],
    ["practical", "useful", "functional", "convenient", "manageable", "versatile"],
    ["best purchase", "great acquisition", "excellent choice", "fantastic buy", "incredible acquisition", "perfect choice"]
]

synonyms_bad = [
    ["bad", "terrible", "horrible", "disastrous", "awful", "deficient"],
    ["quality", "finish", "material", "fabrication", "construction", "design"],
    ["broke", "destroyed", "disassembled", "spoiled", "failed", "ruined"],
    ["recommend", "suggest", "advise", "propose", "discourage", "not recommend"]
]

phrases_good = [
    "It is very {0} and {1} for traveling. Without a doubt the {2} I have made.",
    "The suitcase is very {1}, although a bit small. The wheels work perfectly and it is very {2}.",
    "I am very satisfied with this suitcase. It is {1}, {2} and meets all my expectations.",
    "I bought it for my son and he {0}. It is really {2} and {1}.",
    "Although I don't like the color, it is very {2} and I am happy with the {2}.",
    "The suitcase is {1} and very {2}. I would buy it again without hesitation."
]

phrases_bad = [
    "The suitcase {2} on the first use. The {1} is very {0} and I do not {3} it at all.",
    "I am not very satisfied with the suitcase. It is {1} but does not meet the cabin size requirements I need.",
    "The {1} of the product is {0}. I do not {3} it at all.",
    "I bought this suitcase and it {2} quickly. The {1} is really {0}.",
    "The design is {0} and it {2} after a single use. Definitely do not {3} it.",
    "I thought it was good, but the {1} is {0}. Do not {3} it at all."
]

phrases_neutral = [
    "The suitcase is average in terms of {1}. It works as expected.",
    "It is a standard suitcase with {1}. Nothing exceptional, but it gets the job done.",
    "The {1} of this suitcase is acceptable. Not great, but not bad either.",
    "It is neither {0} nor {1}, just an average suitcase.",
    "I have no strong feelings about this suitcase. It is just {0}."
]

countries = ["USA", "UK", "Spain", "Germany", "France", "Italy"]

def generate_comment():
    sentiment = random.choice(["good", "bad", "neutral"])
    
    if sentiment == "good":
        phrase = random.choice(phrases_good)
        comment = phrase.format(
            random.choice(synonyms_good[0]),
            random.choice(synonyms_good[1]),
            random.choice(synonyms_good[2])
        )
    elif sentiment == "bad":
        phrase = random.choice(phrases_bad)
        comment = phrase.format(
            random.choice(synonyms_bad[0]),
            random.choice(synonyms_bad[1]),
            random.choice(synonyms_bad[2]),
            random.choice(synonyms_bad[3])
        )
    else:
        phrase = random.choice(phrases_neutral)
        comment = phrase.format(
            random.choice(synonyms_bad[0]),
            random.choice(synonyms_good[1])
        )
    
    return comment

def generate_dataset(num_comments):
    data = []
    for i in range(1, num_comments + 1):
        comment = generate_comment()
        country = random.choice(countries)
        data.append([i, comment, country])
    
    df = pd.DataFrame(data, columns=["id", "text", "country"])
    return df

# Generar un dataset de 100 comentarios
df = generate_dataset(500)
#print(df.head())

# Guardar el dataset en un archivo CSV
df.to_csv('input_csv_v2.csv', index=False)

