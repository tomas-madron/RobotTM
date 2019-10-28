import piconzero as pz, time
pz.init()
pz.setOutputConfig(4, 1)

pz.setOutput(4, 100) # 100% - maximum
time.sleep(5)
