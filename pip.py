import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, make_response, \
    Response, jsonify
import threading
from urllib.request import urlopen
import certifi
import json




L=real_time_price()
print(L)