from tabulate import tabulate
import csv
FILENAME="data.csv"
DEEP_REVISION_THRESHOLD = 0.75 # deep revise the worst 25%
class Data:
  def __init__(self):
    self._data = self.extract_data()

  #put all the data in one variable to access later
  def extract_data(self):
    data=[]
    with open(FILENAME, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    self._data = data
    return data
  
  def move_row_to_back(self,value):
    self._data = self.extract_data()
    data = []
    for i, row in enumerate(self._data):
      if row[0] == value:
        target_index = i
      data.append(row)
    new_order = list(range(target_index)) + list(range(target_index + 1, len(data))) + [target_index]
    with open(FILENAME, "w", newline="") as file:
      csv_writer = csv.writer(file)
      for i in new_order:
        csv_writer.writerow(data[i])

  def print_rows_by_values(self, values):
      print()
      rows = []
      for row in self._data:
        if row[0] in values:
          rows.append(row)
      return App.view_stats_from(rows)
  #update one row entirely
  def update_row(self, value, first,second):
    data = []
    for i, row in enumerate(self._data):
      if row[0] == value:
        new_row=[value,row[1],first,second,True]
        data.append(new_row)
      else:
        data.append(row)
    with open(FILENAME, "w", newline="") as file:
      csv_writer = csv.writer(file)
      for row in data:
        csv_writer.writerow(row)
    print("Done.\n")

  def get_data_list_as_int(self):
    output = []
    for i, row in enumerate(self._data):
      int_row = []
      try:
        int_row.extend([int(row[0]),int(row[2]),int(row[3])])
        output.append(int_row)
      except:
        pass # dont have the english row
    return output


class App:
  def __init__(self) -> None:
     #create data object
     self.stats = Data()

     #start menu 
     self.main_menu()

  def main_menu(self) :
      selection = input("Welcome to RevisionTracker:\n1.\tView your stats\n2.\tstart revision\n3.\tInsights\n\nExit by entering any selection not mentioned above \n")
      if selection == '1': App.view_stats_from(self.stats.extract_data())
      elif selection == '2': self.start_revision()
      elif selection == '3': self.insights()
      else: exit(0)
      self.main_menu()

  def insights(self):
    #create insights object
    _insights = SuggestionEngine()
    print(
    "Average Mistakes:\t",_insights.average_mistakes(),"\n",
    "Next Deep Revision:\tHizb ",_insights.generate_next_deep_revision(),"\n",
    "Aim for:\t",_insights.generate_mistake_goal()," mistakes\n",sep="")

  def start_revision(self):
      hizb_number = input("Which Hizb would you like to revise from?\n")
      try: 
        valid_hizb_num = int(hizb_number)
      except:
        print("that is not a number XD")
        return
      if int(valid_hizb_num) in range(1,61):
        skip = self.stats.print_rows_by_values(["Hizb",hizb_number])
        change = False
        if skip: change = True
        elif input("change these values? (y/n)")=="y": change = True
        if change:
          first=int(input("First half: "))
          second=int(input("Second half: "))
          self.stats.update_row(hizb_number,first,second)
        self.stats.move_row_to_back(hizb_number)
      else: 
          print("that is not a recorded hizb number in our system, try again\n")
        
    
  def view_stats_from(data):
    stats_to_show = [data[0]] # Title Bar
    stats_to_show.extend([i[0:4] for i in data if i[4] == "True"]) 
    if len(stats_to_show) != 1:
      print("\nStatistics:")
      print(tabulate(stats_to_show, headers="firstrow", tablefmt='grid'))
    else:
      print("CONGRATS ON STARTING A NEW HIZB!")
      print("Please enter the amount of mistakes made during your first revision:")
      return True

class SuggestionEngine:
  def __init__(self) -> None:
    print("Insights:\n")
    #get data
    self.stats = Data().get_data_list_as_int()
    self.all_mistakes = []
    for _,first_half_mistakes,second_half_mistakes in self.stats:
      self.all_mistakes.extend([first_half_mistakes,second_half_mistakes])
    self.all_mistakes.sort()
    self.all_mistakes = [i for i in self.all_mistakes if i != 0] # remove zeros

  def average_mistakes(self) -> float:
    try:
      return round(sum(self.all_mistakes)/len(self.all_mistakes),2)
    except:
      return "You don't make mistakes :D"
  
  def generate_mistake_goal(self):
    goal = self.average_mistakes() * .90 # remove 10% of issues
    return round(goal)
  def generate_next_deep_revision(self):
    min_mistakes_for_deep_revision = self.all_mistakes[int(len(self.all_mistakes) * DEEP_REVISION_THRESHOLD)]
    print("75th percentile of mistakes:\t",min_mistakes_for_deep_revision)
    for hizb,first_half_mistakes,second_half_mistakes in self.stats:
      if first_half_mistakes >= min_mistakes_for_deep_revision:
        return str(hizb)+" 1st half"
      elif second_half_mistakes >= min_mistakes_for_deep_revision:
        return str(hizb)+" 2nd half"
  
if __name__ == "__main__":
    App()