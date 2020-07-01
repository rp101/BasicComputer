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
    
    self.I = False
    self.D = None
    
  def run(self):
    tmp=-1
    while tmp<12:
      print("T:",str(self.SC.T))
      if self.R:
        pass
      else:
        if self.SC.T==0:
          
          # AR <- PC
          self.AR.data =self.PC.data  
          
        elif self.SC.T == 1:
          
          # IR <- M[AR]
          self.IR.data  = self.memory.read(self.AR.data) 
          
          # PC <- PC+1 increment program counter
          self.PC.inr() 
          
        elif self.SC.T == 2:
          
          # AR <- IR(0-11)
          self.AR.data =  self.IR.data & 0b0000111111111111
          
          # I <- IR(15)
          self.I = self.IR.data >> 15
          
          # D0..D7 <- Decode(12-14)
          self.D = self.IR.data >> 12 & 0b0111
          
        elif self.SC.T == 3:
          
          # if D7=1
          if self.D >> 2:
            
            # if I=1
            if self.I:
              pass
            
            # if I=0
            else:
              pass
            
            print(99)
            
          # if D7=0
          else:
            pass # do nothing
           
          print(bin(self.D>>2))
          
      self.SC.inr()
      tmp+=1
      
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
        
        self.data[0] = 0xffff
        
    def read(self, address):
      return self.data[address]
  
 ###############################
    
bc = BasicComputer()
bc.run()
