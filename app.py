from flask import Flask, render_template, request, session, redirect
from web3 import Web3
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, validators
import json
from datetime import datetime


web3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com'))# Change to your RPC provider

# Load the smart contract ABI and address
contract_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_party","type":"string"},{"internalType":"string","name":"_imageUri","type":"string"}],"name":"addCandidate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"uint256","name":"_cnic","type":"uint256"},{"internalType":"uint256","name":"_qr","type":"uint256"}],"name":"addVoter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"candidateCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"electionStarted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"getCandidateDetailsByID","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getResult","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"party","type":"string"},{"internalType":"string","name":"imageUri","type":"string"},{"internalType":"uint256","name":"votes","type":"uint256"}],"internalType":"struct Voting.Candidate[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startElection","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stopElection","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalVotes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateId","type":"uint256"},{"internalType":"uint256","name":"_voterId","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"voterCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
contract_address = '0x818F7FF1375C59dCB3A8B47E21128d2EF1d45Bcc'

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Define the contract owner address (replace with the actual owner address)
owner_address = '0xff64b2C5B3A16e129F4Bb01aceD1eFC785200423'


with open('config.json','r') as c:
    params = json.load(c)["params"]
# create the extension

app = Flask(__name__)
app.secret_key = 'Commando-evms'

if params['local_server'] == True:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(20), nullable=False)
    phoneNo = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class voter_data(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    cnic = db.Column(db.Integer, nullable=False)
    qrCode = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Candidate_data(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    cnic = db.Column(db.Integer, nullable=False)
    party = db.Column(db.String(80), nullable=False)
    votes = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Admin_data(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    cnic = db.Column(db.Integer, nullable=False)
    qrCode = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=True)

class RegistrationForm(Form):
    votername = StringField('votername', [validators.Length(min=4, max=25)])
    cnic = StringField('CNIC', [validators.Length(min=13, max=13)])
    fingerprint = StringField('fingerprint', [validators.Length(min=4, max=20)])
    qrCode = StringField('qrCode', [validators.Length(min=4, max=20), validators.DataRequired()]) 
    

@app.route('/', methods =['GET' ])
def Commando():  
    return render_template('home.html', params = params)


#Blockchain Function Routing
#@app.route('/startElection', methods=['POST'])
#def deposit():
#   tx_hash = contract.functions.startElection().transact({'from': w3.eth.accounts[0]})
#    w3.eth.waitForTransactionReceipt(tx_hash)
#    return render_template('home.html')

#@app.route('/stopElection', methods=['POST'])
#def withdraw():
#    tx_hash = contract.functions.stopElection().transact({'from': w3.eth.accounts[0]})
#    w3.eth.waitForTransactionReceipt(tx_hash)
#    return render_template('home.html')

#@app.route('/totalVotes')
#def balance():
#    balance = contract.functions.totalVotes().call()
#    return f"Your balance is {balance}"


@app.route('/home', methods =['GET','POST'])
def home():
    if(request.method == "POST"):
        name1 = request.form.get('Name')
        email1 = request.form.get('Email')
        phoneNo1 = request.form.get('phoneNo')
        msg1 = request.form.get('msg')
        entry = Contacts(name = name1, email = email1, phoneNo = phoneNo1, msg = msg1, date = datetime.now() )
        db.session.add(entry)
        db.session.commit()
        """mail.send_message("New Message from EVMS by " + name1,
                          sender = email1,
                          recipients = params['myGmail'],
                          body = msg1 + '\n' + phoneNo1
                          )"""
    return render_template('home.html', params = params)


@app.route('/about', methods =['GET'])
def about():
    return render_template('about.html', params = params)

@app.route('/member', methods =['GET'])
def member():
    return render_template('member.html', params = params)

@app.route('/project', methods =['GET'])
def project():
    return render_template('project.html', params = params)

@app.route('/contact', methods =['GET'])
def contact():
    return render_template('contact.html', params = params)

@app.route('/Admin', methods =['GET', 'POST'])
def admin():

    if ('user' in session and session['user'] == params['admin_name'] ):
        contacts = Contacts.query.all()
        adminData = Admin_data.query.all()
        candidateData = Candidate_data.query.all()
        voterData = voter_data.query.all()
        return render_template('welcome.html', params = params, contacts = contacts, admins = adminData, candidates = candidateData, voters = voterData)



    if request.method == 'POST':
        adminName = request.form.get('username')
        adminCnic = request.form.get('cnic')
        adminQrcode = request.form.get('qrCode')
        if (adminName == params['admin_name'] and
            adminCnic == params['admin_cnic'] and
            adminQrcode == params['admin_qrCode'] ):
            session['user'] = adminName
            contacts = Contacts.query.all()
            adminData = Admin_data.query.all()
            candidateData = Candidate_data.query.all()
            voterData = voter_data.query.all()
            return render_template('welcome.html', params = params, contacts = contacts, admins = adminData, candidates = candidateData, voters = voterData)
    return render_template('Admin.html', params = params)
    

@app.route('/voter', methods =['GET','POST'])
def voter():
    if request.method == 'POST':
        voterQrCode = request.form.get('qrCode')
        voter = voter_data.query.filter_by(qrCode = voterQrCode).first()
        if voter == None:
              return render_template('vote.html', params = params)
        else:
            candidateData = Candidate_data.query.all()
            return render_template('vote.html', params = params, candidates = candidateData)
    return render_template('voter.html', params = params)



@app.route('/vote', methods =['GET', 'POST'])
def vote():
    return render_template('vote.html', params = params)

@app.route("/Add-new-voter/<string:sno>", methods =['GET', 'POST'])
def AddNewVoter(sno):
    if ('user' in session and session['user'] == params['admin_name'] ):
        if(request.method == "POST"):
            name1 = request.form.get('username')
            cnic1 = request.form.get('cnic')
            qrCode1 = request.form.get('qrCode')

            if sno == "0":
                voter = voter_data(name = name1, cnic = cnic1, qrCode = qrCode1, date = datetime.now() )
                db.session.add(voter)
                db.session.commit()
            else:
                voter = voter_data.query.filter_by(sno = sno).first()
                voter.name = name1
                voter.cnic = cnic1
                voter.qrCode = qrCode1
                voter.date = datetime.now()
                db.session.commit()
                return redirect('/Add-new-voter/' + sno)
    voter = voter_data.query.filter_by(sno = sno).first()
    return render_template('Add-new-voter.html', params = params, voter = voter)

@app.route('/delete_voter/<string:sno>', methods =['GET', 'POST'])
def del_voter(sno):
    if ('user' in session and session['user'] == params['admin_name'] ):
        voter = voter_data.query.filter_by(sno = sno).first()
        db.session.delete(voter)
        db.session.commit()
    return render_template('welcome.html', params = params)

@app.route('/Add_candidate/<string:sno>', methods =['GET', 'POST'])
def AddCandidate(sno):
    if ('user' in session and session['user'] == params['admin_name'] ):
        if(request.method == "POST"):
            name2 = request.form.get('username')
            cnic2 = request.form.get('cnic')
            party = request.form.get('party')
            votes = 0

            if sno == "0":
                candidate = Candidate_data(name = name2, cnic = cnic2, party = party,votes=0, date = datetime.now() )
                db.session.add(candidate)
                db.session.commit()
            else:
                candidate = Candidate_data.query.filter_by(sno = sno).first()
                candidate.name = name2
                candidate.cnic = cnic2
                candidate.party = party
                candidate.votes = votes
                candidate.date = datetime.now()
                db.session.commit()
                return redirect('/Add_candidate/' + sno)
    
    candidate = Candidate_data.query.filter_by(sno = sno).first()
    return render_template('Add_candidate.html', params = params, candidate = candidate)

@app.route('/delete_candidate/<string:sno>', methods =['GET', 'POST'])
def del_candidate(sno):
    if ('user' in session and session['user'] == params['admin_name'] ):
        candidate = Candidate_data.query.filter_by(sno = sno).first()
        db.session.delete(candidate)
        db.session.commit()
    return render_template('welcome.html', params = params)

@app.route('/success', methods =['GET'])
def success():
    return render_template('success.html', params = params)

@app.route('/result', methods =['GET'])
def result():
    result_data = contract.functions.getResult().call()
    return render_template('result.html',params = params, result_data=result_data)

@app.route('/thanku', methods =['GET'])
def thanku():
    return render_template('thanku.html', params = params)

@app.route('/logout', methods =['GET'])
def logout():
    session.pop('user')
    return render_template('Admin.html')


app.run(debug = True)