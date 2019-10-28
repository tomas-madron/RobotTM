import piconzero as pz, time
pz.init()
pz.setOutputConfig(0,1) #PWM 4 channel
pz.setOutputConfig(1,1) #PWM 4 channel
pz.setOutputConfig(2,1)
pz.setOutputConfig(3,1)

a = 30
cas = 3


#while True:

#dopredu
pz.setOutput(0, a)
pz.setOutput(1, 0)
pz.setOutput(2, 0)
pz.setOutput(3, a)
print 'Toci dopredu'


time.sleep(cas)
pz.setOutput(0, 0)
pz.setOutput(1, a)
pz.setOutput(2, a)
pz.setOutput(3, 0)
print 'Toci dozadu'


time.sleep(cas)
pz.setOutput(0, a)
pz.setOutput(1, 0)
pz.setOutput(2, 0)
pz.setOutput(3, a)


print 'Toci vlevo'

time.sleep(cas)
pz.setOutput(0, a)
pz.setOutput(1, 0)
pz.setOutput(2, a)
pz.setOutput(3, 0)
print 'Toci vpravo'


time.sleep(cas) 
pz.setOutput(0, 0)
pz.setOutput(1, a)
pz.setOutput(2, 0)
pz.setOutput(3, a)
time.sleep(cas)

pz.setOutput(0, 0)
pz.setOutput(1, 0)
pz.setOutput(2, 0)
pz.setOutput(3, 0)




print 'Nic netoci'





# for y in xrange(95, 100,1):
 #    print y
  #   pz.setOutput(4, y)     
   #  time.sleep(1)

 #for y in xrange(100, 95,-1):
  #   print y
   #  pz.setOutput(4, y)     
    # time.sleep(1)

 
 
