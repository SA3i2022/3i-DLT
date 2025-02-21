#!/usr/bin/env python
# coding: utf-8

# In[3]:


import SBAccess
import socket
import numpy as np


# In[ ]:


def get_array(capture_number, channel):
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess.SBAccess(s)
        theInpSlideId = theSbAccess.GetCurrentSlideId();

        theInpCaptureIndex = capture_number;
        theNumRows = theSbAccess.GetNumYRows(theInpCaptureIndex)
        theNumColumns = theSbAccess.GetNumXColumns(theInpCaptureIndex)
        theNumPlanes = theSbAccess.GetNumZPlanes(theInpCaptureIndex)
        theNumChannels = theSbAccess.GetNumChannels(theInpCaptureIndex)
        
        hold=[]
        for theZPlane in range(theNumPlanes):          
            theSbAccess.SetTargetSlide(theInpSlideId)
            image = theSbAccess.ReadImagePlaneBuf(theInpCaptureIndex,0,0,theZPlane,channel) #captureid,position,timepoint,zplane,channel
            image=image.reshape(theNumRows,theNumColumns)
            hold.append(image)
        hold=np.array(hold)
        #outputs to z,x,y in sldbk ordering
    return hold

def get_mask_array(capture_number):
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess.SBAccess(s)
        theInpSlideId = theSbAccess.GetCurrentSlideId();

        theInpCaptureIndex = capture_number;
        theNumRows = theSbAccess.GetNumYRows(theInpCaptureIndex)
        theNumColumns = theSbAccess.GetNumXColumns(theInpCaptureIndex)
        theNumPlanes = theSbAccess.GetNumZPlanes(theInpCaptureIndex)
        theNumChannels = theSbAccess.GetNumChannels(theInpCaptureIndex)
        
        hold=[]
        for theZPlane in range(theNumPlanes):          
            theSbAccess.SetTargetSlide(theInpSlideId)
            image = theSbAccess.ReadMaskPlaneBuf(theInpCaptureIndex,0,0,theZPlane) #captureid,position,timepoint,zplane,channel
            image=image.reshape(theNumRows,theNumColumns)
            hold.append(image)
        hold=np.array(hold)
        #outputs to z,x,y in sldbk ordering
    return hold
    
def capture_numbers():
# Define the server address and port
    HOST = '127.0.0.1'  # or the appropriate IP address
    PORT = 65432      # The port used by the server

# Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            theSbAccess = SBAccess(s)
            theInpSlideId = theSbAccess.GetCurrentSlideId();
            num_captures = theSbAccess.GetNumCaptures()
    return num_captures

