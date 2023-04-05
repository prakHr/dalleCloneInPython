import dash
dash.register_page(__name__,path = '/imageGenerator')

from dash import dcc, html, Input, State, Output, callback
import dash_bootstrap_components as dbc
from config import api_key,api_host,config_file_path
from furl import furl
from pprint import pprint
import pyrebase
import requests
import json
layout  = html.Div(children = [
        html.H1("Create"),
        html.P("Generate an imaginative image through DALL-E"),
        dcc.Input(id="prompt-command", type="text", placeholder="", style={'marginRight':'10px'}),
     	html.Div(id='image-generator-component',children=[]),
     	html.Button('GENERATE IMAGE',id='submit-image-val',n_clicks=0),
])


@callback(
	Output("image-generator-component","children"),
	[
		Input("prompt-command","value"),
		Input("stored-data","data"),
		Input("submit-image-val","n_clicks"),
	]
)
def trigger_ImageGeneration(prompt_string_input,data,n_clicks):
	input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
	children = []
	if n_clicks>0 and input_id=="submit-image-val":

		# print(f"data={data}")
		email = data['email']
		password = data['password']
		# print(f"email={email}")
		# print(f"password={password}")
		f = open(config_file_path)

		try:
			#####################
			# user1@gmail.com ###
			# 123456 ############
			#####################

			# returns JSON object as 
			# a dictionary
			firebaseConfig = json.load(f)
			firebase = pyrebase.initialize_app(firebaseConfig)
			auth = firebase.auth()
			auth.sign_in_with_email_and_password(email,password)
			# print("Reached here!")
			url = f"https://{api_host}/images/generations"

			payload = {
				"prompt": prompt_string_input,
				"n": 1,
				"size": "256x256"
			}
			headers = {
				"content-type": "application/json",
				"X-RapidAPI-Key": api_key,
				"X-RapidAPI-Host": api_host
			}
			# print("Reached here2!")
			response = requests.request("POST", url, json=payload, headers=headers)
			# print("Reached here3!")
			# print(response.text)
			json_dict = json.loads(response.text)
			# print(f"json_dict={json_dict}")
			image_url = json_dict["data"][0]["url"]
			# print("Reached here4!")
			# print(f"image_url={image_url}")
			children.append(html.Img(src=image_url))
		except Exception as e:
			children.append(html.Div(f"{e}"))
		f.close()
		return children




