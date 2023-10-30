# personal-finances

Personal Finance Tracker
This Python code is a personal finance tracker that allows you to record and analyze your spending. You can input details about your expenses, and the program will store them in a SQLite database. Additionally, it provides data visualization to help you analyze your spending patterns.

**Dependencies**

Make sure you have the following Python packages installed:

- pandas
- sqlite3
- matplotlib


**How to Use**

Clone or download this repository to your local machine.

Run the main.py file in your Python environment.

The program will prompt you with two options:

Enter new spending data.
Show spending analysis.
Choose the desired option by entering 1 or 2.


**Entering New Spending Data**

If you select option 1, you can enter information about a new expense. The program will guide you through the input process, including the date, industry, business, items purchased, cost, and any additional information. You can cancel data entry at any time by typing 'cancel' when prompted for additional information.

**Showing Spending Analysis**

If you select option 2, the program will retrieve your spending data from the SQLite database and generate various visualizations to help you analyze your financial habits. The visualizations include:


Monthly spending by business.
Spending by industry category.
Spending by item.
Daily spending for the current month.
Monthly spending trends.
Transaction counts by business.
The visualizations will be displayed using Matplotlib.

**Error Handling**

The code includes error handling for invalid inputs, such as negative costs or incorrect data types. If you decide to cancel your data entry, the program will raise a Cancel exception.

Feel free to use and modify this code to suit your personal finance tracking needs.
