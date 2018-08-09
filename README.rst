npl_poc
--------

InDataLabs
----------

Testing the IDL endpoint with curl:

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "texts": [
        "Regardless of the industry, Data Science and Artificial Intelligence promise to reshape the way we do our jobs every day. At InData Labs we seek to bring the power of data science & AI to our customers.",
        "Whether you want to explore the possible use cases for big data analytics or have an AI solution in mind and want to start quickly, our team of world-class data scientists and data engineers can help you achieve big data success and get the most out of your investment."
    ]
}' \
  https://api.indatalabs.com/v1/text?apikey=XXXXX&models=interests

