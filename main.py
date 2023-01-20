from flask import Flask, request
from pyresparser import ResumeParser
from base64 import b64decode

app = Flask(__name__)


@app.route('/sendResume', methods=["POST"])
def receiveResume():
    resume_in_b64 = request.get_data()
    resume_in_bytes = b64decode(resume_in_b64, validate=True)

    # Validate it is pdf file
    if resume_in_bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    resume = open('resumeReceived.pdf', 'wb')
    resume.write(resume_in_bytes)
    resume.close()
    return "SUCCESS"


@app.route('/receiveParsedData', methods=["GET"])
def parseResume():
    parsed_resume = ResumeParser('./resumeReceived.pdf').get_extracted_data()
    return parsed_resume


if __name__ == '__main__':
    app.run(debug=True, port=2000)
