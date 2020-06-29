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

  #
  # Buss
  #
  class Bus:
    def __init__(self):
      pass
  
  #
  # Register
  #
  class Register:
    def __init__(self, n_bits):
      self.n_bits = n_bits # number of bits
	
 ###############################
    
bc = BasicComputer()
  
