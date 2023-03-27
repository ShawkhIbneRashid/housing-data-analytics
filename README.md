# housing-data-analytics
<html>
<body>
  
<p align="justify">  </p>
  <p align="justify">
   This project aims to help users understand how apartment rent and price change with time and the price differences among different regions of the USA. To do that, I have created a dashboard that visualizes 
   different types of graphs. The users can also predict the rent and price of apartments by choosing the number of rooms, and by selecting a region. They can also specify the month and year of which they want 
   the predicted price or rent. The site contains a report generated from Microsoft Power BI. The report holds some visual representations showing relations among different attributes of one of the datasets 
   in the form of bar graph, line graph, scatter chart, matrix, and table.
  </p>
  <h4>Datasets</h4>
  <p align="justify">
   There are total 11 datasets used here. The datasets contain price and rent for apartments in different regions of America. The apartments can contain different number of rooms and their rent and price 
   varies based on time and room numbers. More information about them can be accessed from 
   <a href="https://www.kaggle.com/datasets/paultimothymooney/zillow-house-price-data"> dataset_link.</a> 
   One of the datasets contain information like area, number of pools, bathrooms, and year built. 
   More information about this dataset can be found in <a href="https://www.kaggle.com/competitions/zillow-prize-1/data?select=properties_2016.csv"> dataset_link.</a>  
  </p>
  <h4>Prediction</h4>
  <p align="justify">  
  The rent and price are predicted based on the historical data given in the rent and price datasets. First, I tried to find a pattern from the historical data and based on the pattern, a predicted price or 
  rent of the apartment is shown to the user. For this, the users first have to specify the number of rooms and the month and year that they want to get a prediction of. I have used ARIMA model to predict the 
  rent and price. First, I used some rows from a dataset to train ARIMA model to find the best order (value of p, d, q). Then based on the values of p, q and d, I used ARIMA to predict the new data points.
  </p>
  <h4>Back-end</h4>
  <p align="justify">
  I have used Flask to create an API which fetches information from the datasets stored in the MySQL database. Jinja template helped with showing the data sent from backend in the HTML pages.
  </p>
  <h4>Deployment</h4>
  <p align="justify">
  I deployed the webapp in Heroku. I used their ClearDB database to store the datasets and to access them. Later, I deployed the app on AWS cloud platform using Elastic Beanstalk service. I created the database using AWS RDS (MySQL).
  </p>
</body>
</html>
