import pandas as pd
import sqlite3
from sqlite3 import Error
from datetime import datetime, date, timedelta
from matplotlib import pyplot as plt

class Spend:
   
   """
    Represents a spending instance in a personal finance tracker.

    Attributes:
        enter_date (date)
        industry (str): The industry or category of the spending.
        business (str): The name of the business where the spending occurred.
        items (str): Description of the items or services purchased.
        cost (float): The cost of the spending.
        additional_info (str, optional): Additional information about the spending (default is None).
    """
   
   def __init__(self, enter_date: date, industry:str ,business:str, items:str ,cost: float, additional_info: str = None):
      
      """Raise ValueError if cost is below 0: invalid input"""
      if cost < 0:
            raise ValueError("Cost cannot be negative")
        
      """Checks that industry, business and items are not empty"""
      if not (enter_date or industry or business or items):
         raise ValueError("Date, industry, business, and items must not be empty")
   
      self.enter_date = enter_date
      self.industry = industry
      self.business = business
      self.items = items
      self.cost = cost
      self.additional_info = additional_info

   @staticmethod
   def write_to_sql(values):
      try:
         with sqlite3.connect('p_finance.db') as conn:
            # Connect to the SQLite database
            # Create a cursor
            cursor = conn.cursor()

            # Define the SQL INSERT statement
            sql = "INSERT INTO p_finance (date, industry, business, items, cost, additional_info) VALUES (?, ?, ?, ?, ?, ?)"

            # Insert a new row
            cursor.execute(sql, values)

            # Commit the changes
            conn.commit()
      except sqlite3.Error as e:
            print(f"Error: {e}")

   def inputs(self):
      
      print("If at anytime you would like to cancel the data entry, \n please enter 'cancel' when prompted to enter additional info")
      
      try:
         cost = round(float(input("How much did you spend? £")),2)
      except ValueError:
         cost = round(float(input("That was not a number, try again: ")),2)
         #add warning if it is not a float
         #add rounding to get 2dp

      industry = input("Which type of industry is this? e.g. transport, restaurant , pub ").lower()
      #Categorising spend on the main areas

      business = input("Where did you purchase your item  e.g., Sainsbury's ").lower()
      #keeping track on spending hotspots

      items = input('Which items did you buy? ').lower()
      #more genenric e.g., groceries, beer or cocktails

      additional_info = input("Any extra information you'd like to give surrounding this purchase? ").lower()
      #any final information that might be relevant to the purchase
      
      was_it_today = input("Was this purchase made today? Please enter 'yes' or 'no' ").lower()
      enter_date = date.today()
      if was_it_today == 'yes':
         enter_date = date.today()
      else:
         try:
            print('Please provide the date of the purchase (in number format): ')
            year = int(input("Year: "))
            month = int(input("Month (provided in number format): "))
            day = int(input("Day (enter the day of the month): "))
         except ValueError:
            print('Please provide integer values only, try again')
            year = int(input("Year: "))
            month = int(input("Month (provided in number format): "))
            day = int(input("Day (enter the day of the month): "))

         enter_date = date(year,month,day)
   
      self.enter_date = enter_date
      self.industry = industry
      self.business = business
      self.items = items
      self.cost = cost
      self.additional_info = additional_info

   @staticmethod
   def retrieve_SQL():
      try:
         # Connect to the SQLite database
         with sqlite3.connect('p_finance.db') as conn:
         # Create a cursor
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM p_finance")
            db = cursor.fetchall()
            try:
               df = pd.DataFrame(db)
               df.columns = ['primary_key','date','industry','business','items','cost','additional_info']
               df['new_date'] = pd.to_datetime(df['date'],format='ISO8601')
               return df
            except(ValueError,TypeError) as e:
               print(f"Error while converting to DataFrame : {e}")
      except sqlite3.Error as e:
         print(f"Error: {e}")
   
   
   def analyze(df):
      """Using matplotlib to analyze finance data"""
      fig = plt.figure(figsize=(8,6),facecolor='aliceblue',tight_layout =True)

      #Provides the name of the month to the database
      df['month'] = df['new_date'].dt.month
      month_names = {
      1: 'January',
      2: 'February',
      3: 'March',
      4: 'April',
      5: 'May',
      6: 'June',
      7: 'July',
      8: 'August',
      9: 'September',
      10: 'October',
      11: 'November',
      12: 'December'
      }
      
      df['month_name'] = df['month'].map(month_names)

      bymonth = df.groupby('month_name').agg({'cost':'sum'}).reset_index()
      bymonth.columns = ['month','cost']

      current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
      next_month_start = (current_month_start + pd.DateOffset(months=1)).replace(day=1)

      this_month = df[(df['new_date'] >= current_month_start) & (df['new_date'] < next_month_start)]

      bus_spend = this_month.groupby('business').agg({'cost':'sum'}).reset_index()
      bus_spend.columns = ['business','cost']

      bus_tr = df['business'].value_counts()
      bus_trans = pd.DataFrame({'business':bus_tr.index,'count':bus_tr.values})

      ind = this_month.groupby('industry').agg({'cost':'sum'}).reset_index()
      ind.columns = ['industry','cost']

      item = this_month.groupby('items').agg({'cost':'sum'}).reset_index()
      item.columns = ['items','cost']

      byday = this_month.groupby('new_date').agg({'cost':'sum'}).reset_index()
      byday.columns = ['date','cost']



      plt.subplot(3,2,1)
      plt.title('This Months Spend By Business', y=1.05)
      plt.bar(list(bus_spend.business),bus_spend.cost,color='blue')

      plt.subplot(3,2,2)
      plt.title("Spend by industry", y=1.05)
      plt.bar(list(ind.industry),ind.cost,color='orange')

      plt.subplot(3,2,3)
      plt.title('Spend by item', y=1.05)
      plt.bar(list(item['items']), item.cost, color = 'pink')
      plt.tick_params(axis='x',direction='out',color='black',labelcolor='black',labelrotation=30)

      plt.subplot(3,2,4)
      plt.title('Spend by day')
      plt.scatter(list(byday.date),byday.cost, color = 'cornflowerblue')
      plt.tick_params(axis='x',direction='out',color='black',labelcolor='black',labelrotation=30)

      plt.subplot(3,2,5)
      plt.title('Spend by month')
      plt.plot(list(bymonth.month),bymonth.cost,linestyle='dashed')
      plt.tick_params(axis='x',direction='out',color='black',labelcolor='black',labelrotation=30)

      plt.subplot(3,2,6)
      plt.title('Transactions by business')
      plt.bar(list(bus_trans.business),bus_trans['count'],color='purple')
      plt.tick_params(axis='x',direction='out',color='black',labelcolor='black',labelrotation=30)

      plt.show()
      

class Cancel(Exception):
   def __init__(self):
      print("Rerunning the program")

class Wrong(Exception):
   def __init__(self):
      print("Wrong number, next time please enter")

if __name__ == "__main__":
   
   while True:
      try:
         options = input("What would you like to do? Please enter the relevant number: 1: Enter new values \n2: Show analysis \n")
         options = int(options)
         if options == 1:
            
            spends_instance = Spend(date.today(),"default_industry",'default_business','default_items',1)
            spends_instance.inputs()
            
            if (spends_instance.industry == 'cancel' or
               spends_instance.business == 'cancel' or
               spends_instance.items == 'cancel' or
               spends_instance.additional_info == 'cancel'
            ):
               raise Cancel
            
            sql_data = (spends_instance.enter_date,
                        spends_instance.industry,
                        spends_instance.business,
                        spends_instance.items,
                        spends_instance.cost,
                        spends_instance.additional_info)
            
            spends_instance.write_to_sql(sql_data)
            continue
         elif options == 2:
            finance_data = Spend.retrieve_SQL()
            Spend.analyze(finance_data)
            continue
         else:
            print("Invalid input. Please enter 1 or 2.")
            continue
         
      except ValueError:
         print("Invalid input. Please enter a valid number (1 or 2).")


   
   



    
