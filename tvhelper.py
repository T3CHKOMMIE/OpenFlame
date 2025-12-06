import pycec as cec

# Initialize CEC (you might need to specify an adapter)
cec.init()
# Or use cec.init(adapter_path) if needed [3, 5]

# Create a TV device object
tv = cec.Device(cec.CECDEVICE_TV)

# Send the power on command
tv.power_on()


# Close the connection when done
cec.close()
