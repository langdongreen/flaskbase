from flask import render_template, request, flash, session,url_for, redirect, g
import logging
from base import app,c,ts

@app.route("/",methods=["GET","POST"])
def index():
     return render_template('page.html',message="index")