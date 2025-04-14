def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score

relevant_documents = {1, 2, 3, 4, 5}
retrieved_documents = {1, 2, 3, 6, 7}

true_positives = len(relevant_documents.intersection(retrieved_documents))
precision = true_positives / len(retrieved_documents)
recall = true_positives / len(relevant_documents)
f_measure = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print("Manual Calculation:")
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))
print("F-measure:", round(f_measure, 2))

y_true = [1 if doc in relevant_documents else 0 for doc in retrieved_documents]

y_scores = [1] * len(retrieved_documents)

avg_precision = average_precision_score(y_true, y_scores)

print("\nEvaluation Toolkit:")
print("Average Precision:", round(avg_precision, 2))

    '''
    print(code)