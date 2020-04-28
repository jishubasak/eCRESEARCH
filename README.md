<p align="center"><img width=12.5% src="https://github.com/jishubasak/eCResearch/ecFullfill.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![Build Status](https://travis-ci.org/anfederico/Clairvoyant.svg?branch=master)](https://travis-ci.org/anfederico/Clairvoyant)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://gitHub.com/jishubasak/eCResearch)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://github.com/jishubasak)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://ecfullfill.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Research Overview

The main objective of this project is to develop an Artificial Intelligent dashboard for SME's who are either current users of the platform or would be willing to avail the service in future. The objective of the project is to provide a Product Performance Dashboard where SME's would be able to visualize the Performing Index of their product across different regions in the world which should help make a strategic decision as to which ecommerce channel and what country should they be selling their products to. The dashboard also has a functionality to produce a machine generated product description.
<p align="center"><img width=95% src="https://github.com/jishubasak/eCResearch/Schematic.png"></p>

<br>

## Prototype Wireframe  
<img src="https://github.com/jishubasak/eCResearch/ecfullfill_gif.gif" width=40%>

<br>

## Latest Development Changes
```bash
git clone https://github.com/anfederico/eCResearch
```

## Data Description
For this project we scraped data from the most popular ecommerce platform, Amazon for popular products sold by SME's in Philippines.
For our current research, we only focused on 4 countries which are USA, India, United Kingdom and Australia. The data description
is shown in the diagram below. All the highlights in the red were scraped and stored. The Data pipeline section will be discussed
in the next section.
<p align="center"><img width=95% src="https://github.com/jishubasak/eCResearch/data_des_1.png"></p>

<br>

<p align="center"><img width=95% src="https://github.com/jishubasak/eCResearch/data_des_2.png"></p>


## Data Pipeline
The data warehouse for this project mainly consist of Amazon product data(description in the figure above) which was scraped using Selenium + BeautifulSoup. For our project, we used Amazon EC2 instances(Vertical Scaling) to run our scrapers and stored data in Amazon-S3 bucket. You can find codes for each product for each product category stored in jupyter notebook in the Data Warehouse folder.
<p align="center"><img width=95% src="https://github.com/jishubasak/eCResearch/Schematic.png"></p>


## Accessing S3 Bucket
The following python code should yield the dataframe of the product pf interest.
Notice that there are two parameters in the KEY. 'Directory' is the path where the product is stored
and 'Product' is the name of the product. You can find the list of directories and products in
product.csv stored in the repository.

```python
import boto3
import pandas as pd
import sqlite

BUCKET_NAME = 'amazon-data-ecfullfill'
key_id = 'AKIAWR6YW7N5ZKW35OJI'
access_key = 'h/xrcI9A2SRU0ds+zts4EClKAqbzU+/iXdiDcgzm'

KEY = '{}/{}.db'.format(directory,product)
s3 = boto3.resource('s3',aws_access_key_id=key_id,
                      aws_secret_access_key=access_key)
try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'test.db')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
conn = sqlite3.connect('test.db')    
df = pd.read_sql('''SELECT * FROM Product''', conn)
```


#Modelling
After performing Data Cleaning, Wrangling and Preprocessing, which involved
concatenation, text cleaning, data imputation(using KNNImputer), we consolidated
all the database for a specific countries.

Our problem entails into regression problem where we want user input to be an image
of their product(captured through phone or a professional image), then they input
which product that is, followed by input meta data such as Product Length, Width, Height and
Weight of their product. Based on the image input and meta data input, the model yields
a score for each country, which essentially is the Performing index of that product in each Country.

For construct of model, we used a modified AlexNet Architecture and merge our Artificial Neural Network
which basically contains the meta input. We adopted the concept of 'Late Fusion'. I believe that for
image + metadata we may have to do the fusion after one or more layers.
The intuition is: first transform image and metadata to compatible domains and
concatenate the representations later. We can concatenate either transforming
the convnet image features to vector or reshaping the metadata features to an
image and appending the result as a new channel to the image representation.

Code Representation:

```python
# first input model
# First ConV Layer
visible1 = Input(shape=(128,128,3),name='main_input')
conv11 = Conv2D(96, kernel_size=(3,3),strides=(4,4),activation='relu',
                padding='valid')(visible1)
pool11 = MaxPooling2D(pool_size=(2, 2))(conv11)
batch11 = BatchNormalization()(pool11)

# Second ConV Layer
conv12 = Conv2D(64, kernel_size=(3,3),strides=(2,2),activation='relu',
                padding='valid')(batch11)
pool12 = MaxPooling2D(pool_size=(2, 2))(conv12)
batch12 = BatchNormalization()(pool12)

# Third ConV Layer
conv13 = Conv2D(32, kernel_size=(3,3),strides=(2,2),activation='relu',
                padding='valid')(batch12)
pool13 = MaxPooling2D(pool_size=(1, 1))(conv13)
batch13 = BatchNormalization()(pool13)

#Flattening the Image Input Model
flat1 = Flatten()(batch13)


# Second input model(Meta Data Input)
visible2 = Input(shape=(4,1,1),name='meta_input')
hidden21 = Dense(10, activation='relu')(visible2)
hidden22 = Dense(20, activation='relu')(hidden21)
hidden23 = Dense(10, activation='relu')(hidden22)
flat2 = Flatten()(hidden23)

# Concatenation of Image Input and Meta Data Input models
merge = concatenate([flat1, flat2])
# interpretation model
hidden1 = Dense(10, activation='relu')(merge)
hidden2 = Dense(10, activation='relu')(hidden1)
hidden3 = LeakyReLU(alpha=0.3)(hidden2)
output = Dense(1,name='output')(hidden3)
model_usa_shampoo = Model(inputs=[visible1, visible2], outputs=output)

# Compiling
opt = SGD(lr=0.01, momentum=0.9,clipnorm=1.0)
model_usa_shampoo.compile(optimizer=opt,
              loss='mean_absolute_error',
              metrics=['mean_squared_error',
                       'mean_absolute_error',
                       'mean_absolute_percentage_error',
                       'cosine_proximity'])

# And trained it via:
history_usa_shampoo = model_usa_shampoo.fit(x = {'main_input': np.array(images_usa),
                                                 'meta_input': meta_input_usa},
                                                  y = {'output': usa_shampoo_features['target'].values},
                                                  epochs=1000,
                                                  batch_size=32,
                                                  verbose=1)

# summarize layers
print(model_usa_shampoo.summary())
model_link = '/home/jishu/database_new/models/health_and_beauty/hair_products/shampoo/'
os.chdir(os.path.join(model_link))
model_usa_shampoo.save("usa_shampoo.h5")

```

For more information, please visit the directory 'Models' in the repository
The schematic diagram of the architecture is mentioned below:

<img src="https://github.com/jishubasak/eCResearch/architecture.png">


## Web Application
The construction of Web Application is done using Dash and Django Framework. It is still in its nascent stage but a quick demo is
available in the WebApp folder. To access the demo, go to Web App/demo/ then execute the following code in your CLI
(please install the prerequisites from the requirements).

```bash
python app.py
```

## Installation
1. Clone this repository
2. Install dependencies
   ```bash
   pip3 install -r requirements.txt
   ```
3. The requirements will vary from folders to folder. This for the current stage, it might be suggested
that you explore each modules independently. Will fix this in upcoming commits.

#### Pending Features
- Export all the databases files for scraped Products
- Export all the trained models
- Additional Features to be added in the Web application.
- Integrating Dash with Django
