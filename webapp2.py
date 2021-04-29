# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:48:08 2021

@author: André Vitor
"""

import streamlit as st
import numpy as np
import cv2 as cv
import glob
from functions import *
import pandas as pd
import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt


st.title('Haziness')
st.write("This web app calculates the Haziness measure.")
st.write("#### Olar266")
st.write("""
         It can also calculate RMS, Histogram Spread,
         Michelson, Weber and Rizzi metrics.""")

calc_rms = st.checkbox('RMS')
# calc_Weber = st.checkbox('Weber')
calc_Michelson = st.checkbox('Michelson')
# calc_Rizzi = st.checkbox('Rizzi')
calc_HS = st.checkbox('Histogram Spread')

rms_list = []
Michelson_list = []
HS_list = []

'---'
" ## Sobre inputs:"
N = st.number_input("Select number of iterations: ",min_value=1, value=1000, step=1)
s = st.number_input("Select the size of the patches: ",min_value=1, value=2, step=1)


st.sidebar.text_area("Sequence input",
                        value= 10, #valor inicial
                        height=250)


#%% Sidebar
st.sidebar.header('User Input Features')


lista = ['a','b','c']
lista_default =['a']


variaveis_escolhidas = st.sidebar.multiselect('Nome',lista, lista_default)

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)


#%% 
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data


'---'
#%% File inputs

multiple_files = st.file_uploader("Select files: ",accept_multiple_files=True)
if multiple_files is None:
    st.text("No upload")
else:
    st.text("The files are:")
    files = [file.name for file in multiple_files]
    st.text("\n".join(files))


values = []
# @st.cache()
def calculations():
    for file in multiple_files:
    #     file2 = file.split("\\")[1]
        st.text(f'Calculating for {file.name}')
    #     file = cv.imread(file, 0)

        img = Image.open(file)
        img = ImageOps.grayscale(img)
        img = np.asarray(img)
        x, y = haziness_mean_std(img, N, s)
        values.append([file.name, round(x, 4), round(y, 4)])


        # Calculate other metrics
        if calc_rms:
            rms_list.append(RMS(img))
    #     if calc_Weber:
    #         Weber_list.append(Weber(img))
        if calc_Michelson:
            Michelson_list.append(Michelson(img))
    #     if calc_Rizzi:
    #         Rizzi_list.append(Rizzi(img))
        if calc_HS:
            HS_list.append(HS(img))

calculations()
DF = pd.DataFrame(values,columns=["Name", "Haziness", "Std"])
if calc_rms:
    DF["RMS"] = rms_list
if calc_Michelson:
    DF["Michelson"] = Michelson_list
if calc_HS:
    DF["HS"] = HS_list
DF.sort_values(by=['Name'],inplace=True,ignore_index=True)
st.write(DF)


fig, ax = plt.subplots()
ax.plot(range(len(values)),DF.Haziness,'ok--',label='Haziness')
if calc_rms:
    ax.plot(range(len(values)),rms_list,'or--',label='RMS')
if calc_Michelson:
    ax.plot(range(len(values)),Michelson_list,'ob--',label='Michelson')
if calc_HS:
    ax.plot(range(len(values)),HS_list,'og--',label='HS')
ax.legend()

import matplotlib.pyplot as plt
# plt.plot()
st.pyplot(fig)

#%% Append data to existing chart
'---'
import time

# # Get some data.
# data = np.random.randn(10, 2)

# # Show the data as a chart.
# chart = st.line_chart(data)

# # Wait 1 second, so the change is clearer.
# time.sleep(10)

# # Grab some more data.
# data2 = np.random.randn(10, 2)

# # Append the new data to the existing chart.
# chart.add_rows(data2)

# # Wait 1 second, so the change is clearer.
# time.sleep(10)

# # Grab some more data.
# data2 = np.random.randn(10, 2)

# # Append the new data to the existing chart.
# chart.add_rows(data2)


