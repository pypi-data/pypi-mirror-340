#Implement the Boolean retrieval model and process queries.


documents = {
    1: "apple banana orange",
    2: "apple banana",
    3: "banana orange",
    4: "apple"
}

def build_index(docs):
    index = {}
    for doc_id, text in docs.items():
        terms = set(text.split())
        for term in terms:
            if term not in index:
                index[term] = {doc_id}
            else:
                index[term].add(doc_id)
    return index

inverted_index = build_index(documents)

def boolean_and(operands, index):
    if not operands:
        return list(range(1, len(documents) + 1))
    
    result = index.get(operands[0], set())
    for term in operands[1:]:
        result = result.intersection(index.get(term, set()))
    
    return list(result)

def boolean_or(operands, index):
    result = set()
    for term in operands:
        result = result.union(index.get(term, set()))
    
    return list(result)

def boolean_not(operand, index, total_docs):
    operand_set = set(index.get(operand, set()))
    all_docs_set = set(range(1, total_docs + 1))
    return list(all_docs_set.difference(operand_set))

query1 = ["apple", "banana"]
query2 = ["apple", "orange"]

result1 = boolean_and(query1, inverted_index)
result2 = boolean_or(query2, inverted_index)
result3 = boolean_not("orange", inverted_index, len(documents))

print("Documents containing 'apple' and 'banana':", result1)
print("Documents containing 'apple' and 'orange':", result2)
print("Documents not containing 'orange':", result3)
