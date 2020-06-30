import array

#
#  BasicComputer
#
class BasicComputer:
  def __init__(self):
    self.memory = self.Memory()
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
          
          # AR <- PC
          self.AR.data =self.PC.data  
          
        elif self.SC.T == 1:
          
          # IR <- M[AR]
          self.IR.data = self.memory.read(self.AR.data) 
          
          # PC <- PC+1 increment program counter
          self.PC.inr() 
          
      self.SC.inr()
      n+=1
      
  #
  # Register
  #
  class Register:
    def __init__(self, n_bits):
      self.n_bits = n_bits # number of bits
      self.data = 0
      
    def load(self, data):
      self.data = data
      
    def inr(self):
      self.data += 1
  #
  # Sequence counter   
  #
  class SequenceCounter:
    def __init__(self):
      self.T = 0
    
    def inr(self):
      if self.T == 5:
        self.T = 0
      else:
        self.T += 1
        
  #
  # Memory
  #
  class Memory():
    def __init__(self):
      self.data = array.array('I')
      for i in range(65536):
        self.data.append(0)
        
    def read(self, address):
      return self.data[address]
  
 ###############################
    
bc = BasicComputer()
bc.run()
