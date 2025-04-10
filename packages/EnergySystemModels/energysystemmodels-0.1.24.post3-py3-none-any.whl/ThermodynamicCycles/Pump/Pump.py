from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 

class Object:
    def __init__(self):
        self.Timestamp=None

        #Input and Output Connector
        self.Inlet=FluidPort() 
        self.Outlet=FluidPort()

        # #Input Data
        self.eta=0.7
        self.Pdischarge_bar=None
        # self.Tcond_degC=None
        self.Pdischarge=None #self.Pdischarge_bar*100000
        # self.Tdischarge_target=None #°C

        #points de fonctionnement de la pompe
        self.X_F = None #débit volumique m3/h X_F = [5,34,40,50]
      
        self.Y_hmt = None # Hauteur manométrique Y_hmt = [12,60,80,68]
        self.Y_eta = None # point de rendement Y_eta = [0.4,0.8,0.9,0.1]

        # #Initial Values
        #self.Inlet.fluid=None
        # self.Inlet.P=101325
        # self.F=0.1
        # self.Inlet.F=self.F

        # self.F_Sm3s=None
        # self.F_Sm3h=None
        self.F_Sm3s=None
        
        #Output Data
        self.df=[]

        self.Q_pump=0
    #     self.Q_losses=0
        self.Ti_degC=None
        
    def calculate (self):
        if self.Pdischarge_bar is not None:
            self.Pdischarge=self.Pdischarge_bar*100000

        self.Ti_degC=-273.15+PropsSI("T", "P", self.Inlet.P, "H", self.Inlet.h, self.Inlet.fluid)
        print("Ti_degC",self.Ti_degC)
        if self.Inlet.F is not None:
            self.F_m3s =self.Inlet.F/PropsSI("D", "P", self.Inlet.P, "T", (self.Ti_degC+273.15), self.Inlet.fluid)
        print("F_m3s",self.F_m3s)

        self.Q_pump=self.F_m3s*(self.Pdischarge-self.Inlet.P)/self.eta

        
    #     # outlet connector calculation
        self.Outlet.fluid=self.Inlet.fluid
        self.Outlet.h=self.Inlet.h
        self.Outlet.F=self.Inlet.F
        self.Outlet.P=self.Inlet.P

    #     # Results
        self.df = pd.DataFrame({'Pump': [self.Timestamp,self.Inlet.fluid,self.Inlet.F,self.Q_pump/1000,], },
                      index = ['Timestamp','pump_fluid','pump_F_kgs','Qpump(KW)', ])


        #Corrélation de la courbe caractéristique de la pompe
        #pip install scikit-learn
        from sklearn.linear_model import LinearRegression  
        from sklearn.preprocessing import PolynomialFeatures 
        from sklearn.metrics import mean_squared_error, r2_score

        import matplotlib.pyplot as plt
        import numpy as np
        import random

        #----------------------------------------------------------------------------------------#
        # Step 1: training data
        if self.X_F is None:
            self.X_F = [7,50,100,150]
        if self.Y_hmt is None:
            self.Y_hmt = [12,60,80,68]
        if self.Y_eta is None:
            self.Y_eta = [0.5,0.7,0.5,0.4]
        
       
        print(max(self.X_F))
        self.X_F = np.asarray(self.X_F)
        max_x=max(self.X_F)
        self.Y_hmt = np.asarray(self.Y_hmt)
        max_Y_hmt=max(self.Y_hmt)
        self.Y_eta = np.asarray(self.Y_eta)
        max_Y_eta=max(self.Y_eta)


        self.X_F = self.X_F[:,np.newaxis]
        self.Y_hmt = self.Y_hmt[:,np.newaxis]
        self.Y_eta = self.Y_eta[:,np.newaxis]

        plt.scatter(self.X_F,self.Y_hmt)
        plt.scatter(self.X_F,self.Y_eta)

        #----------------------------------------------------------------------------------------#
        # Step 2: data preparation

        nb_degree = len(self.X_F)-1

        polynomial_features = PolynomialFeatures(degree = nb_degree)

        X_TRANSF = polynomial_features.fit_transform(self.X_F)
       

        #----------------------------------------------------------------------------------------#
        # Step 3: define and train a model

        model_hmt = LinearRegression()
        model_eta = LinearRegression()

        #model_hmt.fit(X_TRANSF, self.Y_hmt)
        model_hmt.fit(X_TRANSF, self.Y_hmt)
        model_eta.fit(X_TRANSF, self.Y_eta)

        #----------------------------------------------------------------------------------------#
        # Step 4: calculate bias and variance

        Y_hmt_NEW = model_hmt.predict(X_TRANSF)
        Y_eta_NEW = model_eta.predict(X_TRANSF)

        rmse_hmt = np.sqrt(mean_squared_error(self.Y_hmt,Y_hmt_NEW))
        r2_hmt = r2_score(self.Y_hmt,Y_hmt_NEW)
        print('RMSE: ', rmse_hmt)
        print('R2: ', r2_hmt)

        rmse_eta = np.sqrt(mean_squared_error(self.Y_eta,Y_eta_NEW))
        r2_eta = r2_score(self.Y_eta,Y_eta_NEW)
        print('RMSE: ', rmse_eta)
        print('R2: ', r2_eta)

        #----------------------------------------------------------------------------------------#
        # Step 5: prediction

        x_new_min = 0.0
        x_new_max = 1.05*max_x

        X_NEW = np.linspace(x_new_min, x_new_max, 100)
        X_NEW = X_NEW[:,np.newaxis]
        print(X_NEW)

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)
   

        Y_hmt_NEW = model_hmt.predict(X_NEW_TRANSF)
        Y_eta_NEW = model_eta.predict(X_NEW_TRANSF)

        plt.plot(X_NEW,Y_hmt_NEW, color='coral', linewidth=3)
        plt.plot(X_NEW, Y_eta_NEW, color='blue', linewidth=3)

        plt.grid()
        plt.xlim(x_new_min,x_new_max)
        plt.ylim(0,1.05*max_Y_hmt)

        title = 'Degree = {}; RMSE = {}; R2 = {}'.format(nb_degree, round(rmse_hmt,2), round(r2_hmt,2))

        plt.title("Polynomial Linear Regression using scikit-learn and python 3 \n " + title,
                fontsize=10)
        plt.xlabel('m3/h')
        plt.ylabel('Hmt(m) & rendement')

        plt.savefig("polynomial_linear_regression.png", bbox_inches='tight')
        plt.show()

        
        print("hmt",model_hmt.predict([[15,15,15]]))
        print("eta",model_eta.predict([[15,15,15]]))