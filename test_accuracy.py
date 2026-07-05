import csv
from rag_pipeline import ask

input_file = "reports/accuracy/test_questions.csv"
output_file = "reports/accuracy/accuracy_results.csv"

results = []
correct = 0
total = 0

with open(input_file, newline="", encoding="utf-8-sig") as file:

    reader = csv.DictReader(file)

    print("Columns:", reader.fieldnames)

    for row in reader:

        question = row["Question"].strip()
        expected = row["Expected Answer"].strip()

        print("=" * 60)
        print("Question:", question)

        answer = ask(question)

        print("Answer:", answer)

        if expected.lower() in answer.lower():
            status = "Pass"
            correct += 1
        else:
            status = "Review"

        total += 1

        results.append([
            question,
            expected,
            answer,
            status
        ])

with open(output_file, "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Question",
        "Expected Answer",
        "Actual Answer",
        "Status"
    ])

    writer.writerows(results)

accuracy = (correct / total) * 100 if total else 0

print("=" * 60)
print(f"Correct Answers : {correct}")
print(f"Total Questions : {total}")
print(f"Accuracy        : {accuracy:.2f}%")
print("=" * 60)