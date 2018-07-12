#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, redirect, url_for, request
app = Flask(__name__)
from lib import moclo
from lib import db_config

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/foo/<bar>")
def foo(bar):
    return jsonify({"foo": bar})

@app.route("/submit")
def submit():
    s = db_config.Submission(name="foo")
    db_session.add(s)
    db_session.commit()
    return jsonify({"foo": "hello"})

@app.route("/check-seq", methods = ['POST'])
def check_seq():
    data = request.get_json()
    if not data or not data['gene_id'] or not data['sequence'] or not data['part_type']:
        return jsonify({"error": "JSON must contain keys gene_id, sequence and part_type"})
    ret = moclo.sequence_input(data['gene_id'], data['sequence'], data['part_type'])
    return jsonify(ret)

@app.route("/checl-seq-test")
def check_seq_test():
    ret = moclo.sequence_input("test_dna" ,"atgagtgaagtaaacctaaaaggaaatacagatgaattagtgtattatcgacagcaaaccactggaaataaaatcgccaggaagagaatcaaaaaagggaaagaagaagtttattatgttgctgaaacggaagagaagatatggacagaagagcaaataaaaaacttttctttagacaaatttggtacgcatataccttacatagaaggtcattatacaatcttaaataattacttctttgatttttggggctattttttaggtgctgaaggaattgcgctctatgctcacctaactcgttatgcatacggcagcaaagacttttgctttcctagtctacaaacaatcgctaaaaaaatggacaagactcctgttacagttagaggctacttgaaactgcttgaaaggtacggttttatttggaaggtaaacgtccgtaataaaaccaaggataacacagaggaatccccgatttttaagattagacgtaaggttcctttgctttcagaagaacttttaaatggaaaccctaatattgaaattccagatgacgaggaagcacatgtaaagaaggctttaaaaaaggaaaaagagggtcttccaaaggttttgaaaaaagagcacgatgaatttgttaaaaaaatgatggatgagtcagaaacaattaatattccagaggccttacaatatgacacaatgtatgaagatatactcagtaaaggagaaattcgaaaagaaatcaaaaaacaaatacctaatcctacaacatcttttgagagtatatcaatgacaactgaagaggaaaaagtcgacagtactttaaaaagcgaaatgcaaaatcgtgtctctaagccttcttttgatacctggtttaaaaacactaagatcaaaattgaaaataaaaattgtttattacttgtaccgagtgaatttgcatttgaatggattaagaaaagatatttagaaacaattaaaacagtccttgaagaagctggatatgttttcgaaaaaatcgaactaagaaaagtgcaataa", "cds")
    return jsonify(ret)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    db_session, db_engine = db_config.connect_db()
    print("connected")
    app.run(debug=True)
