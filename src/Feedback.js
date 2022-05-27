import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

export function Feedback() {
    const location = useLocation();
    const navigate = useNavigate();
    const navState = location.state;

    const [correctEquation, setCorrectEquation] = React.useState(false);
    const [equationFeedback, setEquationFeedback]= React.useState(false);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState('');
    const [segmentedImages, setSegmentedImages] = React.useState({});
    const characterClasses = ['','(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'C', 'X', 'cos', 'd', 'div', 'forward_slash', 'int', 'log', 'sin', 'sqrt', 'tan', 'y', 'z']
    const [classFeedback, setClassFeedback] = React.useState({});
    const [feedbackSubmitted, setFeedbackSubmitted] = React.useState(false);

    async function getSegmentedImages() {
        setLoading(true);
        fetch('http://127.0.0.1:5000/feedback',{
            method: 'GET',
            headers: {
                'Content-Type':'application/json'
            }
        })
        .then(result => result.json())
        .then(
            (res) => {
                setLoading(false);
                if(res['error'] === undefined) {
                    setSegmentedImages(res);
                    let tempFeedback = {};
                    Object.keys(res).forEach((key,index)=>{
                       tempFeedback[key] = ''; 
                    });
                    setClassFeedback(tempFeedback);
                } else {
                    setError(res.error);
                }
            },
            (error) => {
                setLoading(false);
            }
        )
    }

    function handleSelect(e,key) {
        let tempFeedback = classFeedback;
        tempFeedback[key] = e.target.value;
        setClassFeedback(tempFeedback);
    }

    async function sendResults() {
        fetch('http://127.0.0.1:5000/feedback',{
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(classFeedback)
        })
        .then(response=>response.json())
        .then(
            (res) => {
                setLoading(false);
                if(res['error'] === undefined) {
                   setFeedbackSubmitted(true); 
                    navigate('../',{replace:true});
                } else {
                    setError(res.error);
                }
            },
            (err) => {
                setError(err.message);
                setLoading(false);
            }
        )
    }

    return (
        <div>
            <h3>Feedback</h3>
            <h6>Equation: {navState.equation}</h6>
            <h6>Formatted Equation: {navState.formatted_equation}</h6>
            <h6>Result: {navState.result}</h6>
            <img style={{ width: 400, height: 200 }} src={navState.uploadedImage === null ? navState.savedImage : navState.uploadedImage} alt="saved equation"/>
            {!equationFeedback && <div>
            Is the result correct?
            <button type="button" disabled={loading} className="btn btn-primary" onClick={()=>{setCorrectEquation(true);setEquationFeedback(true)}} style={{ margin: 10 }}>Yes</button>
            <button type="button" disabled={loading} className="btn btn-primary" onClick={()=>{setCorrectEquation(false);setEquationFeedback(true);getSegmentedImages()}} style={{ margin: 10 }}>No</button>
            </div>}
            {error !== '' && <h6 style={{ color: 'red' }}>Error: {error}</h6>}
            {!correctEquation && equationFeedback && error === '' && <div>
                {Object.keys(segmentedImages).map((key,index)=>{
                    return (
                        <div key={key} style={{ margin: 10, padding: 10 }}>
                            <img style={{ width: 150, height: 150 }} src={"data:image/png;base64," + segmentedImages[key]} alt="segmented symbols"/>
                            <select onChange={e=>handleSelect(e,key)}>
                                {characterClasses.map((k,i) => {
                                    return (
                                        <option value={k}>{k}</option>
                                    )
                                })}
                            </select>
                            <h6>{key}</h6>
                            <hr/>
                        </div>
                    )
                })}
                <button type="button" disabled={loading} className="btn btn-primary" onClick={sendResults}>Submit</button>
            </div>}
        </div>
    )
}


