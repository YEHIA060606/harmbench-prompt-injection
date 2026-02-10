import matplotlib.pyplot as plt

# Graph 1: Standard vs Contextual
types = ["Standard", "Contextual"]
accuracy_types = [50.0, 24.1]

plt.figure()
plt.bar(types, accuracy_types)
plt.title("Accuracy by Prompt Type")
plt.ylabel("Accuracy (%)")
plt.ylim(0, 100)
plt.show()

# Graph 2: Accuracy by Category
categories = [
    "Jailbreak", "Authority", "Emotional",
    "Policy Bypass", "Fake System", "Roleplay", "Misinformation"
]
accuracy_cat = [0, 0, 0, 31.8, 50.0, 70.0, 83.3]

plt.figure()
plt.bar(categories, accuracy_cat)
plt.title("Accuracy by Attack Category")
plt.ylabel("Accuracy (%)")
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.show()
