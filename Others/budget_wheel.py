import matplotlib.pyplot as plt

def create_budget_wheel(net_income, expenses):
    # Prepare data for the pie chart
    labels = list(expenses.keys())
    values = list(expenses.values())

    # Create a color map for expenses
    colors = ['red', 'blue', 'orange', 'purple', 'cyan']  # Add more colors as needed

    # Create the pie chart
    fig, ax = plt.subplots()
    patches, texts, _ = ax.pie(values, labels=labels, colors=colors,
                               startangle=90, counterclock=False, wedgeprops={'width': 0.4},
                               autopct='%1.1f%%')

    # Set aspect ratio to be equal so that pie is drawn as a circle
    ax.axis('equal')

    # Set title
    ax.set_title('Budget Wheel')

    # Display the net income value at the center
    ax.text(0, 0, f"${net_income:.2f}", va='center', ha='center', fontsize=12)

    # Adjust the position of the percentage labels within the colored sections
    for text in texts:
        text.set_horizontalalignment('center')
        text.set_verticalalignment('center')

    # Display the pie chart
    plt.show()

# Example usage
net_income = 5000
expenses = {
    'Rent': 1000,
    'Utilities': 300,
    'Groceries': 500,
    'Transportation': 200,
    'Entertainment': 250
}

create_budget_wheel(net_income, expenses)
