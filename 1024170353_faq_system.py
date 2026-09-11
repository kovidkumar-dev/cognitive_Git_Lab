"""
UCS420: Cognitive Computing - Assignment 4
A Cognitive FAQ System Using Pandas
Name: Kovid Kumar
Roll Number: 1024170353
"""

import pandas as pd

# Q1: Build Personalized Knowledge Base
roll_number = "1024170353"

# Last two digits of roll number -> 5, 3
last_two_digits = [int(d) for d in roll_number[-2:]]

categories_list = ["billing", "account", "general"]

# digit 5 -> categories_list[5 % 3] = categories_list[2] = "general"
# digit 3 -> categories_list[3 % 3] = categories_list[0] = "billing"

fixed_entries = [
    {"question": "what is the annual fee", "answer": "The annual fee is Rs 500.",
     "keywords": "fee cost price charge", "category": "billing"},
    {"question": "how to reset password", "answer": "Go to Settings > Reset Password.",
     "keywords": "password reset login", "category": "account"},
    {"question": "what are your working hours", "answer": "We are open 9 AM to 5 PM.",
     "keywords": "hours timing open time", "category": "general"},
    {"question": "how can i pay the fee", "answer": "You can pay via UPI, card, or net banking.",
     "keywords": "pay payment upi fee", "category": "billing"},
]

# Personalized entry from digit 5 -> category "general"
personalized_entry_1 = {
    "question": "what is the last date to submit assignments",
    "answer": "Assignments must be submitted by the last date announced on the student portal.",
    "keywords": "deadline last date submission",
    "category": "general",
}

# Personalized entry from digit 3 -> category "billing"
personalized_entry_2 = {
    "question": "how do i get a refund for the annual fee",
    "answer": "Refund requests can be raised through the accounts portal within 15 days of payment.",
    "keywords": "refund fee cancellation",
    "category": "billing",
}

all_entries = fixed_entries + [personalized_entry_1, personalized_entry_2]

df = pd.DataFrame(all_entries)

print("=" * 70)
print("Q1: Final 6-row Knowledge Base DataFrame")
print("=" * 70)
print(f"Roll Number: {roll_number} | Last two digits: {last_two_digits}")
print(f"digit {last_two_digits[0]} -> category = "
      f"{categories_list[last_two_digits[0] % 3]}")
print(f"digit {last_two_digits[1]} -> category = "
      f"{categories_list[last_two_digits[1] % 3]}")
print(df)
print()



# Q2: Generate and Score a Hypothesis - scoring function

def score_query(query, dataframe):
    """
    Takes a query string and returns all matching entries ranked by
    confidence (number of overlapping keywords between the query and
    each entry's keyword list).
    """
    query_words = set(query.lower().split())
    results = []

    for _, row in dataframe.iterrows():
        keyword_set = set(row["keywords"].lower().split())
        score = len(query_words & keyword_set)
        if score > 0:
            results.append({
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "score": score,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


print("=" * 70)
print("Q2: Scoring Function Demo")
print("=" * 70)
demo_query = "how to reset password"
demo_results = score_query(demo_query, df)
print(f"Query: '{demo_query}'")
for r in demo_results:
    print(f"  Score {r['score']} -> {r['question']} | {r['answer']}")
print()


# Q3: same_category function

def same_category(category_name, dataframe):
    """Returns all questions belonging to a given category."""
    return dataframe[dataframe["category"] == category_name]


print("=" * 70)
print("Q3: same_category() Demo")
print("=" * 70)
# Using the category of a personalized entry from Q1 ("general")
chosen_category = personalized_entry_1["category"]
print(f"Questions in category '{chosen_category}':")
print(same_category(chosen_category, df))
print()

# Q4: Add a new keyword to an entry (user input) and save to CSV

print("=" * 70)
print("Q4: Add Keyword and Save to CSV")
print("=" * 70)

target_question = "what is the annual fee"
target_index = df[df["question"] == target_question].index[0]

new_keyword = input(
    f"Enter a new keyword to add to the entry '{target_question}': "
).strip().lower()

existing_keywords = df.at[target_index, "keywords"]
df.at[target_index, "keywords"] = f"{existing_keywords} {new_keyword}".strip()

print(f"Updated keywords for '{target_question}': {df.at[target_index, 'keywords']}")

csv_filename = f"{roll_number}_faq_data.csv"
df.to_csv(csv_filename, index=False)
print(f"Full updated DataFrame saved to: {csv_filename}")
print()



# Q5: groupby - entries per category
print("=" * 70)
print("Q5: FAQ Entries per Category (groupby)")
print("=" * 70)
category_counts = df.groupby("category").size()
print(category_counts)
print()



# Q6: Scoring function that reports ties instead of silently picking one
def score_query_with_ties(query, dataframe):
    """
    Same scoring logic as Q2, but if two or more entries tie for the
    highest score, ALL of them are printed instead of silently
    returning just one.
    """
    query_words = set(query.lower().split())
    scored = []

    for _, row in dataframe.iterrows():
        keyword_set = set(row["keywords"].lower().split())
        score = len(query_words & keyword_set)
        if score > 0:
            scored.append({
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "score": score,
            })

    if not scored:
        print(f"Query: '{query}' -> No matching entries found.")
        return []

    max_score = max(item["score"] for item in scored)
    top_matches = [item for item in scored if item["score"] == max_score]

    print(f"Query: '{query}'")
    if len(top_matches) > 1:
        print(f"  TIE DETECTED: {len(top_matches)} entries tied at score {max_score}")
        for m in top_matches:
            print(f"    -> {m['question']} | {m['answer']} (category: {m['category']})")
    else:
        print(f"  Best match (score {max_score}): {top_matches[0]['question']}")
        print(f"  Answer: {top_matches[0]['answer']}")

    return top_matches


print("=" * 70)
print("Q6: Tie-Handling Scoring Function Demo")
print("=" * 70)

# Query that produces a TIE - "fee" matches both fee-related billing entries
tie_query = "fee"
score_query_with_ties(tie_query, df)
print()

# Query that does NOT produce a tie - matches only the password entry uniquely
no_tie_query = "reset password login"
score_query_with_ties(no_tie_query, df)
