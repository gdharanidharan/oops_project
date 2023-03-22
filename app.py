import re
import nlpcloud


class NLPApp:
  """
    A simple NLP application that allows users to perform Named Entity Recognition,
    Language Detection, and Sentiment Analysis.
  """

  def __init__(self):
    self.__database = {}

  def run(self):
    """Runs the application."""
    self.__first_menu()

  def __first_menu(self):
    """Displays the first menu and handles user input."""
    while True:
      first_input = input("""
      Welcome to the NLP App!
      Please select an option:
      1. Register
      2. Login
      3. Exit
      """)

      if first_input in ['1', '2', '3']:
        break
      else:
        print("Invalid input. Please enter a number from 1 to 3.")

    if first_input == '1':
      self.__register()
    elif first_input == '2':
      self.__login()
    else:
      self.__exit()
  
  def __second_menu(self):
    """Displays the second menu and handles user input."""
    print("What would you like to do?")
    while True:
      second_input = input("""
      Please select an option:
      1. Named Entity Recognition
      2. Language Detection
      3. Sentiment Analysis
      4. Logout
      5. Delete account
      """)
      if second_input in ['1', '2', '3', '4','5']:
        break
      else:
        print("Invalid input. Please enter a number from 1 to 5.")
    
    if second_input == '1':
      self.__ner()
    elif second_input == '2':
      self.__language_detection()
    elif second_input == '3':
      self.__sentiment_analysis()
    elif second_input == '4':
      self.__logout()
    else:
      self.__delete_account()

  def __register(self):
    """Registers a new user."""
    while True:
      name = input('Please enter your name: ')
      if not name:
        print("Name cannot be empty. Please enter a valid name.")
      else:
        break

    while True:
      email = input('Please enter your email: ')
      if not email:
        print("Email cannot be empty. Please enter a valid email.")
      elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email address. Please enter a valid email.")
      elif email in self.__database:
        print("This email address is already registered. Please log in.")
        self.__first_menu()
      else:
        break

    while True:
        password = input('Please enter your password: ')
        if not password:
            print("Password cannot be empty. Please enter a valid password.")
        elif len(password) < 8:
            print("Password must be at least 8 characters long.")
        elif not re.search(r"[A-Z]", password):
            print("Password must contain at least one uppercase letter.")
        elif not re.search(r"[a-z]", password):
            print("Password must contain at least one lowercase letter.")
        elif not re.search(r"\d", password):
            print("Password must contain at least one digit.")
        elif not re.search(r"[!@#\$%\^&\*\(\)_\+<>\?]", password):
            print("Password must contain at least one special character.")
        else:
            break

    if email not in self.__database:
      self.__database[email] = [name, password]
      print('Registration successful.')
      self.__first_menu()

  def __login(self):
    """Logs in an existing user."""
    print('Please enter your login credentials.')
    while True:
      email = input('Email: ')
      if not email:
        print("Email cannot be empty. Please enter a valid email.")
      elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email address. Please enter a valid email.")
      else:
        break

    while True:
      password = input('Please enter your password: ')
      if not password:
        print("Password cannot be empty. Please enter a valid password.")
      else:
        break

    if email in self.__database:
      if password == self.__database[email][1]:
        print('Login successful. Welcome back, {}!'.format(self.__database[email][0]))
        self.__second_menu()
      else:
        print('Incorrect password. Please try again.')
        self.__first_menu()
    else:
      print('This account does not exist. Please register first.')
      self.__first_menu()

  def __ner(self):
    print('Performing Named Entity Recognition...')
    para = input('enter the paragraph')
    search_term = input('What you would like yo search')

    client = nlpcloud.Client("finetuned-gpt-neox-20b", "2b58d7fb9af09e617ee525e78c7766b6d8c5bb61", gpu=True, lang="en")
    response = client.entities(para, searched_entity=search_term)
    print(response)

  def __language_detection(self):
    print('Performing Language Detection...')

  def __sentiment_analysis(self):
    print('Performing Sentiment Analysis...')
    para = input('enter the paragraph')

    client = nlpcloud.Client("distilbert-base-uncased-emotion", "2b58d7fb9af09e617ee525e78c7766b6d8c5bb61", gpu=False, lang="en")
    response = client.sentiment(para)

    d = {}
    for i in response['scored_labels']:
      key = i['label']
      score = i['score']
      d[key] = score

    sentiment  = sorted(d,key=lambda x: x[1])[0]
    print(sentiment)

  def __logout(self):
    print('Logging out...')
    self.__first_menu()

  def __exit(self):
    print('Exiting NLP App...')
    exit()

if __name__ == '__main__':
  obj = NLPApp()
  obj.run()