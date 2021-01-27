# Output Door-1
    def setOn1(self, command=None):
        if self.bc.binaryOutput(1) != 1:
            self.bc.binaryOutput(1, 1)
            self.setDriver("GV6", 1)
            self.setDriver("GV0", 255) 
            LOGGER.info('Output 1 On')   
            time.sleep(2)
        if self.bc.binaryOutput(1) != 0:    
            self.bc.binaryOutput(1, 0)
            self.setDriver("GV6", 0)
            LOGGER.info('Output 1 Off')
    # Door-1 Status
    def doorStat1(self, command=None):
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV0", 0, force=True)
        if self.bc.universalInput(1) == range(155, 161): 
            self.setDriver("GV0", 155, force=True)
        if self.bc.universalInput(1) == range(400, 560): 
            self.setDriver("GV0", 255, force=True)