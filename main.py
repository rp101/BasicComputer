#python 3.7.1

#
#  BasicComputer
#
class BasicComputer:
  def __init__(self):
    # Registers (see CSA pg. 128)
    self.DR = self.Register(16) # Data register
    self.AR = self.Register(12) # Address register
    self.AC = self.Register(16) # Accumulator
    self.IR = self.Register(16) # Instruction register
    self.PC = self.Register(12) # Program counter
    self.TR = self.Register(16) # Temporary register
    self.INPR = self.Register(8) # Input register
    self.OUTPR = self.Register(8) # Output register
    
    self.SC = self.SequenceCounter()
    self.main_bus = self.Bus()
    
    # CSA 154pg.
    self.R = False # interrupt flip-flop
    
  def run(self):
    n=-1
    while n<12:
      print("T:",str(self.SC.T))
      if self.R:
        pass
      else:
        if self.SC.T==0:
          self.main_bus.data = self.PC.data
          self.AR.data = self.main_bus.data 
          print("AR",str(self.AR.data))
        elif self.SC.T == 1:
          pass
      self.SC.inc()
      n+=1
      
      

  #
  # Buss
  #
  class Bus:
    def __init__(self):
      self.data = 0
  
  #
  # Register
  #
  class Register:
    def __init__(self, n_bits):
      self.n_bits = n_bits # number of bits
      self.data = 0
      
    def load(self, data):
      self.data = data
  #
  # Sequence counter   
  #
  class SequenceCounter:
    def __init__(self):
      self.T = 0
    
    def inc(self):
      if self.T == 5:
        self.T = 0
      else:
        self.T += 1
        
  #
  # Memory
  #
  class Memory():
    def __init__():
      pass
  
 ###############################
    
bc = BasicComputer()
bc.run()
