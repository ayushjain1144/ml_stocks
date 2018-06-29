import numpy as np
from sklearn import svm, preprocessing
from sklearn.svm import SVC as svc
from sklearn.preprocessing import scale, Imputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold
import pandas as pd
import time

FEATURES =  ['DE Ratio',
			 'Trailing P/E',
			 'Price/Sales',
			 'Price/Book',
			 'Profit Margin',
			 'Operating Margin',
			 'Return on Assets',
			 'Return on Equity',
			 'Revenue Per Share',
			 'Market Cap',
			 'Enterprise Value',
			 'Forward P/E',
			 'PEG Ratio',
			 'Enterprise Value/Revenue',
			 'Enterprise Value/EBITDA',
			 'Revenue',
			 'Gross Profit',
			 'EBITDA',
			 'Net Income Avl to Common ',
			 'Diluted EPS',
			 'Earnings Growth',
			 'Revenue Growth',
			 'Total Cash',
			 'Total Cash Per Share',
			 'Total Debt',
			 'Current Ratio',
			 'Book Value Per Share',
			 #'Cash Flow',
			 'Beta',
			 'Held by Insiders',
			 'Held by Institutions',
			 'Shares Short (as of',
			 'Short Ratio',
			 'Short % of Float',
			 'Shares Short (prior ']


def Build_Data_Set():
	
	data_df = pd.read_csv('TotalDebtEquity.csv')
	data_df = data_df.replace("N/A", np.nan)
	imputer = Imputer(missing_values=np.nan, strategy = 'median', axis=0)
	data_df.iloc[:,4:-1] = imputer.fit_transform(data_df.iloc[:,4:-1])

	X = np.array(data_df[FEATURES].values.astype(float))
	#print(X.isnull().sum())
	#msno.matrix(data_df)
	#time.sleep(2)

	y = (np.array(data_df["Status"].replace("underperform", 0).replace("outperform", 1).values.astype(float)))
	
	X = preprocessing.normalize(X)
	X = preprocessing.scale(X)

	return X,y


def gaussianKernelGramMatrixFull(X1, X2, sigma = 1):

	gram_matrix = np.zeros((X1.shape[0], X2.shape[0]))
	for i, x1 in enumerate(X1):
		for j, x2 in enumerate(X2):
			x1 = x1.flatten()
			x2 = x2.flatten()
			gram_matrix[i, j] = np.exp(- np.sum(np.power((x1 - x2), 2)) / float(2 * (sigma**2)))

	return gram_matrix


def Analysis():


	# doing manually
	
	'''
	test_size = 1800
	X, y = Build_Data_Set()
	print(len(X))
	#time.sleep(15)
	#cross_validation_size = 1000

	clf = svm.SVC(kernel = "linear", C =1.0)
	clf.fit(X[:-test_size], y[:-test_size])

	correct_count = 0
	predictions = clf.predict(X) 

	for x in range(1, test_size+1):
		if predictions[-x] == y[-x]:
			correct_count += 1

	print("Accuracy:", (correct_count/test_size) * 100.00)
	'''
	
	X, y = Build_Data_Set()

	#normal approach

	'''
	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.3, random_state=65)
	'''	

	# as random data can suffer from class imbalance
	# Stratified k-fold cross validation

	skf = StratifiedKFold(n_splits=2, random_state=9, shuffle=True)

	for train_index, test_index in skf.split(X, y):
		print("Train:", train_index, "Test:", test_index)
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]


	
	#linear SVC

	#Results : Accuracy : 0.60
	#results given by StratifiedKfold: 0.567, 0.57
	#improvements possible: 1) Gaussian svm : already done :) 
	#					   2) Recovering data with N/A values: already done :)
	#					3) More data

		
		clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)

		predictions = clf.predict(X_test)

		accuracy = accuracy_score(predictions, y_test)

		print(accuracy)

			

		# implementing gaussian svm

	
		#Results: Accuracy = 0.61
		#Results: with c = 1; acc: 0.594, 0.591

		'''

		clf = svm.SVC(C = 1, kernel = "precomputed")
		model = clf.fit(gaussianKernelGramMatrixFull(X_train, X_train), y_train)

		predictions = clf.predict(gaussianKernelGramMatrixFull(X_test, X_train))

		accuracy = accuracy_score(predictions, y_test)	
		print(accuracy)

		'''




	

Analysis()	
	
	
