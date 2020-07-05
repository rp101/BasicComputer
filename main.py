import array
import math 

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
    self.E = 0 # carry
    
    #tmp
    self.AC.data=0x3001
    
  # cycle()
  #
  def cycle(self):
    self.SC.inr()
    
    if self.SC.T == 0: print("----------------------")
        
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
        print("IR:", bin(self.IR.data))
        
        # if D7=1
        if self.D == 7:
          print("D7=1")
          
          # if I=1
          # execute I/O instruction
          if self.I:
            print("I=1")
            self.SC.clr()
          
          # if I=0
          # execute register reference instruction
          else:
            print("I=0")
            
            # CLA instruction 
            # clear AC
            # AC <- 0
            if self.IR.data == 0x7800:
              self.AC.clr()
              
            # CLE instruction (lear E)
            elif self.IR.data == 0x7400:
              self.E = 0
              
            # CMA instruction (complement AC)
            elif self.IR.data == 0x7200:
              self.invertBits(self.AC.data)
              
            # CME instruction (complement E)
            elif self.IR.data == 0x7100:
              if self.E == 0: self.E = 1
              else: self.E = 0
              
            # CIR instruction
            elif self.IR.data == 0x7080:
              self.AC.data = (self.AC.data >> 1)|(self.E <<15)
              self. E = self.AC.data & 1
              
            # CIL instruction
            elif self.IR.data == 0x7040:
              tmp_E = self.E
              self.E = self.AC.data >> 15
            
              self.AC.data = (self.AC.data 
                | 0b10000000000000000 # making front zeros usable in left shift operation
                ) << 1 & 0b1111111111111111 | tmp_E
                
              
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
          print("D7=0")
          
          # if I=1
          # indirect memory reference
          if self.I:
            print("I=1")
            
            # AR <- M[AR]
            self.AR.data = self.memory.read(self.AR.data) & 0b0000111111111111
            
            self.memory_ref_instruction()
          
          # if I=0
          # direct memory reference
          else:
            print("I=0")
            self.memory_ref_instruction()
            
          self.SC.clr()
          
  # execute memory reference instruction
  #
  def memory_ref_instruction(self):
    
    print("IR:", hex(self.IR.data))
    self.DR.data = self.memory.read(self.AR.data)
    print("DR:",hex(self.DR.data))
    print("AR:", hex(self.AR.data))
    
    if self.D == 0:
      print("AND")
      
    elif self.D == 1:
      print("ADD")
      
    elif self.D == 2:
      self.AC.data = self.DR.data
          
    elif self.D == 3:
      self.memory.write(self.AR.data, self.AC.data)
      
    elif self.D == 4:
      print("BUN")
      
    elif self.D == 5:
      print("BSA")
      
    elif self.D == 6:
      print("ISZ")
      
  # number bit inverter
  #
  def invertBits(self, num):  

    # calculating number of bits  
    # in the number  
    x = int(math.log2(num)) + 1
  
    # Inverting the bits one by one  
    for i in range(x):  
        num = (num ^ (1 << i))  
        
    return num
    
  # get_bit()
  #
  def get_bit(self, num):
    pass 
    
    
  # run()
  #
  def run(self):
    tmp=0
    while tmp<8:
      self.cycle()
      if self.SC.T == -1:
        self.print_data()
      tmp+=1
      
  # print_data
  #
  def print_data(self):
    print("")
    print("PC:" + hex(self.PC.data), end=' ')
    print("AC:" + hex(self.AC.data), end=' ')
    print("E:" + str(self.E), end=' ')
    print("")
    print("")
    self.memory.print_data(0,4)
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
        
        self.data[0] = 0x2004
        self.data[1] = 0x3003
        self.data[2] = 0x7fff
        self.data[3] = 0x0002
        self.data[4] = 0x1234
        
    def read(self, address):
      return self.data[address]
      
    def write(self, address, data):
      self.data[address] = data
    
    def print_data(self, from_addr, to_addr):
      print("## MEMORY ##")
      address = from_addr
      while address <= to_addr:
        print(address,":",hex(self.data[address]))
        address += 1
      print("############")
  
 ###############################
    
bc = BasicComputer()
bc.run()
