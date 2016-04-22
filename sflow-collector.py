import socket
import struct

class sFlow:
    def __init__(self, dataGram):
        dataPosition = 0
        self.sample = []
        self.data = dataGram
        self.dgVersion = struct.unpack('i', (dataGram[0:4])[::-1])[0]
        self.addressType = struct.unpack('i', (dataGram[4:8])[::-1])[0]
        self.len = len(dataGram)
        if self.addressType == 1:
            self.agentAddress = socket.inet_ntoa(dataGram[8:12])
            self.subAgent = struct.unpack('i', (dataGram[12:16])[::-1])[0]
            self.sequenceNumber = struct.unpack('i', (dataGram[16:20])[::-1])[0]
            self.sysUpTime = struct.unpack('i', (dataGram[20:24])[::-1])[0]
            self.NumberSample = struct.unpack('i', (dataGram[24:28])[::-1])[0]
            dataPosition = 28
        elif self.addressType == 2:
            self.agentAddress = socket.inet_ntop(AF_INET6, dataGram[8:24])
            self.subAgent = struct.unpack('i', (dataGram[24:28])[::-1])[0]
            self.sequenceNumber = struct.unpack('i', (dataGram[28:32])[::-1])[0]
            self.sysUpTime = struct.unpack('i', (dataGram[32:36])[::-1])[0]
            self.NumberSample = struct.unpack('i', (dataGram[36:40])[::-1])[0]
            dataPosition = 40
        else:
            self.agentAddress = 0
            self.subAgent = 0
            self.sequenceNumber = 0
            self.sysUpTime = 0
            self.NumberSample = 0
        if self.NumberSample > 0:
            for i in range(self.NumberSample):
                SampleSize = struct.unpack('i', (dataGram[(dataPosition + 4):(dataPosition + 8)])[::-1])[0]
                self.sample.append(sFlowSample(dataGram[(dataPosition):(dataPosition + 4)], SampleSize, dataGram[(dataPosition + 8):(dataPosition + SampleSize + 8)]))
                dataPosition = dataPosition + 8 + SampleSize
             

class sFlowSample:
    def __init__(self, header, sampleSize, dataGram):
        self.record = []
        self.data = dataGram
        SampleHeader = struct.unpack('i', header[::-1])[0]
        SampleSource = struct.unpack('i', (dataGram[4:8])[::-1])[0]
        self.enterprise = (SampleHeader & 4294963200)/4096
        self.sampleType = (SampleHeader & 4095)
        self.length = sampleSize
        self.sequence = struct.unpack('i', (dataGram[0:4])[::-1])[0]
        self.sourceType = (SampleSource & 4278190080)/16777216
        self.sourceIndex = (SampleSource & 16777215)
        self.recordCount = struct.unpack('i', (dataGram[8:12])[::-1])[0]
        dataPosition = 12
        for i in range(self.recordCount):
            RecordSize = struct.unpack('i', (dataGram[(dataPosition + 4):(dataPosition + 8)])[::-1])[0]
            self.record.append(sFlowRecord(dataGram[(dataPosition):(dataPosition + 4)], RecordSize, dataGram[(dataPosition + 8):(dataPosition + RecordSize +8)]))
            dataPosition = dataPosition + 8 + RecordSize
            

class sFlowRecord:
    def __init__(self, header, length, dataGram):
        RecordHeader = struct.unpack('i', header[::-1])[0]
        self.header = header
        self.enterprise = (RecordHeader & 4294901760)/65536
        self.format = (RecordHeader & 65535)
        self.length = length
        self.data = dataGram

UDP_IP = "192.168.0.70"
UDP_PORT = 6343

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
                                                 
    data, addr = sock.recvfrom(4096)
    sFlowData = sFlow(data)

    print "Source:", addr[0]
    #print "length:", sFlowData.len
    #print "DG Version:", sFlowData.dgVersion
    #print "Address Type:", sFlowData.addressType
    #print "Agent Address:", sFlowData.agentAddress
    #print "Sub Agent:", sFlowData.subAgent
    #print "Sequence Number:", sFlowData.sequenceNumber
    #print "System UpTime:", sFlowData.sysUpTime
    #print "Number of Samples:", sFlowData.NumberSample
    print ""
    for i in range(sFlowData.NumberSample):
        #print "Sample Number:", i + 1
        #print "Sample Enterprise:", sFlowData.sample[i].enterprise
        #print "Sample Type:", sFlowData.sample[i].sampleType
        #print "Sample Sequence:", sFlowData.sample[i].sequence
        #print "Sample Record Count:", sFlowData.sample[i].recordCount
        #print ""
        for j in range(sFlowData.sample[i].recordCount):
            #print "Record Enterprise:", sFlowData.sample[i].record[j].enterprise
            print "Record Format:", sFlowData.sample[i].record[j].format
            print ""
