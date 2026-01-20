import numpy as np




class model:
    def __init__(self, input_size=17, hidden1=256, hidden2=64, output_size=3):
        
        self.initialize(input_size, hidden1, hidden2, output_size)
    
    def initialize(self,input_size, hidden1, hidden2, output_size):
        self.W1=np.random.randn(input_size,hidden1)*0.01
        self.b1=np.zeros(hidden1)
        
        self.W1=np.random.randn(hidden1,hidden2)*0.01
        self.b1=np.zeros(hidden2)
        
        self.W1=np.random.randn(hidden2,output_size)*0.01
        self.b1=np.zeros(output_size)



    def Run(self,training_data):
        
        self.training_data=training_data
        self.forward_propagation()
        self.gradient_descent()
        self.backward_propagation()



    def ReLU(self,z):
        return np.maximum(0,z)

    def Loss_Function(self):
        pass

        
    def forward_propagation(self):
        
        # (1,17) (17,256)
        self.Z1=self.training_data@self.W1+self.b1
        self.A1=self.ReLU(self.Z1)
        # (17,256) (256,64)
        self.Z2=self.A1@self.W2+self.b2
        self.A2=self.ReLU(self.Z2)
        # (256,64) (64,3)
        self.Z3=self.A2@self.W3+self.b3
        self.A3=self.ReLU(self.Z3)
       


        
    def gradient_descent():
        pass
    def backward_propagation(self,learning_rate):
        self.W1-=self.dzW1*learning_rate
        self.b1-=self.dzb1*learning_rate

        self.W2-=self.dzW2*learning_rate
        self.b2-=self.dzb2*learning_rate
        
        self.W3-=self.dzW3*learning_rate
        self.b3-=self.dzb3*learning_rate

        






