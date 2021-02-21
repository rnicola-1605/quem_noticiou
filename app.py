# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, session, jsonify

@app.route("/")
def home():
	"""Pagina inicial."""
	return 'HOME DO APP'