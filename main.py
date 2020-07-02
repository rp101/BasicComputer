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
    
    self.I = 0
    self.D = None
    self.E = 0
    
  #
  # cycle()
  #
  def cycle(self):
    self.SC.inr()
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
          # execute I/O instruction
          if self.I:
            self.SC.clr()
          
          # if I=0
          # execute register reference instruction
          else:
            
            # CLA instruction
            if self.IR.data == 0x7800:
              self.AC.clr()
              
            # CLE instruction
            elif self.IR.data == 0x7400:
              self.E = 0
              
            # CMA instruction
            elif self.IR.data == 0x7200:
              pass
              
            # CME instruction
            elif self.IR.data == 0x7100:
              pass
              
            # CIR instruction
            elif self.IR.data == 0x7080:
              pass
              
            # CIL instruction
            elif self.IR.data == 0x7040:
              pass
              
            # INC instruction
            elif self.IR.data == 0x7020:
              self.AC.inr()
              
            # SPA instruction
            elif self.IR.data == 0x7010:
              pass
              
            # SNA instruction
            elif self.IR.data == 0x7008:
              pass
              
            # SZA instruction
            elif self.IR.data == 0x7004:
              pass
              
            # SZE instruction
            elif self.IR.data == 0x7002:
              pass
              
            # HLT instruction
            elif self.IR.data == 0x7001:
              pass
              
            self.SC.clr()
          
        # if D7=0
        # execute memory reference instruction
        else:
          
          # if I=1
          # indirect memory reference
          if self.I:
            
            # AR <- M[AR]
            self.AR.data = self.memory.read(self.AR.data)
          
          # if I=0
          # direct memory reference
          else:
            pass
          self.SC.clr()
  #
  # run()
  #
  def run(self):
    tmp=0
    while tmp<12:
      self.cycle()
      if self.SC.T == -1:
        self.print_data()
      tmp+=1
  #
  # print_data
  #
  def print_data(self):
    print("")
    print("PC:" + hex(self.PC.data), end=' ')
    print("AC:" + hex(self.AC.data), end=' ')
    print("E:" + str(self.E), end=' ')
    print("")
    print("")
           
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
      
    def clr(self):
      self.data = 0
  #
  # Sequence counter   
  #
  class SequenceCounter:
    def __init__(self):
      self.T = -1 
    
    def inr(self):
      if self.T == 5:
        self.T = 0
      else:
        self.T += 1
        
    def clr(self):
      self.T = -1
        
  #
  # Memory
  #
  class Memory():
    def __init__(self):
      self.data = [0]*4096
      for i in range(4096):
        self.data.append(0)
        
        self.data[0] = 0x7020
        self.data[1] = 0x0222
        
    def read(self, address):
      return self.data[address]
  
 ###############################
    
bc = BasicComputer()
bc.run()
