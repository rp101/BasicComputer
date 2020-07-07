import re

###################################
# POSITION
###################################

class Position:
  def __init__(self, L, P):
    self.line = L
    self.pos = P

###################################
# ERRORS
###################################

class Error:
  def __init__(self, error_name, details):
    self.error_name = error_name
    self.details = details
    
  def as_string(self):
    result = f'{self.error_name}:{self.details}'
    return result

class IllegalCharError(Error):
  def __init__(self, details):
    super().__init__("Illegal Character", details)
    
###################################
# TOKENS
###################################

class Token:
  instructions = ("ADD", "AND")
  
  def __init__(self, pos, value):
    self.pos = pos 
    self.value = value
    
  def __repr__(self):
    return f'\n{self.pos}:{self.value}'
    
###################################
# LEXER
###################################

class Lexer:
  def __init__(self, text):
    self.text = text
    print(self.text)
    
  def make_tokens(self):
    tokens = []
    line_no = -1 
    
    lines = re.split("\n", self.text)
    
    for line in lines:
      line_no += 1
      
      #atskiria komentarus
      line_no_comments = re.split("\s", (line.split('/')[0]))
      line_no_comments = line_no_comments[:3] # only three columns used
      
      tokens.append(self. tokenize_line(line_no, line_no_comments))
      
    return tokens, None
    
  def tokenize_line(self, line_no, line):
    tokens = []
    pos = -1
    
    for term in line:
      pos += 1
      for instruction in Token.instructions:
        if term == instruction:
          tokens.append(Token((line_no, pos), instruction))
      if term == "":
        tokens.append(Token((line_no, pos), "NUL"))
    return tokens
    
###################################
# RUN
###################################

def run(text):
  lexer = Lexer(text)
  tokens, error = lexer.make_tokens()
  
  #return tokens, error
  return tokens ,None
