from flask import Flask, render_template, url_for, session, redirect, request,flash
import products
import logging
from ..utils import *
from sm import app,c


@app.route('/create/text/<text>')
def text(text):
    '''change text'''
    session['text'] = text

    return redirect(redirect_url())

@app.route('/create/collarcolour/<colour>')
def collarcolour(colour):
    '''change collar colour'''
    session['collarcolour'] = colour

    return redirect(redirect_url())

@app.route('/create/textcolour/<colour>')
def textcolour(colour):
    '''change collar colour'''
    session['textcolour'] = colour

    return redirect(redirect_url())

@app.route('/create/icon/<icon>')
def icon(icon):
    '''change icon'''
    session['icon'] = icon

    return redirect(redirect_url())

@app.route('/create/hardware/<colour>')
def hardwarecolour(colour):
    '''change collar colour'''
    session['hardware'] = colour

    return redirect(redirect_url())

@app.route('/create/buckle/<colour>')
def bucklecolour(colour):
    '''change collar colour'''
    session['buckle'] = colour

    return redirect(redirect_url())

@app.route('/create/width/<size>')
def width(size):
    '''change collar colour'''
    session['size'] = size

    return redirect(redirect_url())

@app.route('/create/leash/<choicer>')
def leash(choice):
    '''change collar colour'''
    session['leash'] = choice

    return redirect(redirect_url())
