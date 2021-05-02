import streamlit as st
from io import StringIO
from lxml import etree
import datetime

log_file = 'verificaiton.log'

def log_str(message: str, log=log_file):
    with open(log, 'a') as file:
        file.write(f'{datetime.datetime.now()} {message} \n')


st.title('SCL Verifier')

with open('XSD/SCL.xsd') as file:
    xml_doc = etree.parse(file)
    xml_scheme = etree.XMLSchema(xml_doc)


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    file_name = uploaded_file.name
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()

    try:
        st.markdown('Document parsing')
        xml_file = etree.fromstring(uploaded_file.getvalue())
        st.text('Parsing is Ok!')
        log_str(f'{file_name}: parsing ok!')
        st.markdown('Document verification')
        try:
            xml_scheme.assertValid(xml_file)
            st.text('Verification is Ok!')
            log_str(f'{file_name}: verification ok!')

        except etree.DocumentInvalid as err:
            st.text(err.error_log)
            log_str(f'{file_name}: verification failed!')

    except etree.XMLSyntaxError as err:
        st.text(err.error_log)
        log_str(f'{file_name}: parsing failed!')

