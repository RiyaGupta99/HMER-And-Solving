import React, { Component } from 'react';
import P5Wrapper from 'react-p5-wrapper';
import sketch from './sketches/sketch';
import UploadButton from './UploadButton';
import Output from './Output';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Canvas.css';
import Graph from './Graph';
import { Link } from 'react-router-dom';

let savedImage = '';

class Canvas extends Component {
	constructor() {
		super();
		this.state = {
			color: false,
			evaluate: false,
			equation: '',
			formatted_equation: '',
			result: '',
			uploadedImage: null,
			loading: false,
			uploadedImageName: '',
			savedImage: '',
			graph: '',
			solved: false,
			error: ''
		};
	}

	pseudo = (data) => {
		savedImage = data;
	}

	setUploadedImage = (image) => {
		this.setState({ uploadedImage: image, evaluate: true, equation: '', formatted_equation: '', result: '', color: false });
	}

	setUploadedImageName = (fileName) => {
		this.setState({ uploadedImageName: fileName });
	}

	sendImgToServer = (image, action) => {
		this.setState({ loading: true });
		//let img = image.replace("data:image/png;base64,","");

		let data = {};
		let img;
		if (this.state.uploadedImage !== null) {
			img = this.state.uploadedImage.replace("data:image/png;base64,", "");
		} else {
			img = image.replace("data:image/png;base64,", "");
		}
		data.image = img;
		data.action = action;

		fetch('http://127.0.0.1:5000/predict', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		})
			.then(response => response.json())
			.then(res => {
				if (res['error'] === undefined) {
					this.setState(
						{
							color: false,
							evaluate: false,
							equation: res['Entered_equation'],
							formatted_equation: res['Formatted_equation'],
							result: res['solution'],
							loading: false,
							graph: res['graph'],
							solved: true,
							error: ''
						}
					)
				} else {
					this.setState({
						error: res['error'],
						loading: false,
						solved: false,
						evaluate: false
					});
				}
			})
			.then(res => {
				if (this.state.solved) {
					var graphExpr = this.state.formatted_equation.toLowerCase().split(';');
					var c = 0;
					for (var i = 0; i < graphExpr.length; i++) {
						var e = graphExpr[i];
						if (e.includes('=') && graphExpr.length == 1) {
							e = e.replace('=', '-')  
						}
						e = e.replace("**", "^")
						e = e.replace("*", "")
						window.c.setExpression({id: "graph" + c, latex: e})
						c += 1;
					}
					// if (graphExpr.includes('=')) {
					// 	const [lhs, rhs] = graphExpr.split('=');
					// 	graphE
					// }
					// if (graphExpr.includes(';')) {
					// 	var expr = graphExpr.split(';');
					// 	window.c.setExpression({id: "graph1", latex: expr[0]})
					// 	window.c.setExpression({id: "graph2", latex: expr[1]})
					// }
					// else {
					// 	graphExpr = graphExpr.replace("**", "^")
					// 	graphExpr = graphExpr.replace("*", "")
					// 	window.c.setExpression({ id: 'graph1', latex: graphExpr });
					// }
				}
			})
			.catch((error) => {
				console.error('Error:', error);
				this.setState({ loading: false, solved: false, error: error });
			});
	}

	onClear = () => {
		this.setState({
			color: true,
			evaluate: false,
			equation: '',
			formatted_equation: '',
			result: '',
			loading: false,
			uploadedImage: null,
			solved: false,
			error: ''
		});
		var exprs = window.c.getExpressions();
		for (var i = 0; i < exprs.length; i++) {
			window.c.removeExpression({id: exprs[i].id})
		}
	}

	onEval = () => {
		this.setState({
			color: false,
			evaluate: true,
			equation: '',
			formatted_equation: '',
			result: ''
		});
	}

	render() {
		return (
			<div className="main">
				<div className="row">
					<div className="col-9">
						<h2>Draw the equation below</h2>
						<div>
							<P5Wrapper sketch={sketch}
								color={this.state.color}
								evaluate={this.state.evaluate}
								callBack={this.pseudo}>
							</P5Wrapper>
						</div>
					</div>
					<div className="col-3">
						<br></br>
						<br></br>
						<div>
							<UploadButton disable={this.state.loading} sendImgToServer={this.sendImgToServer} setUploadedImage={this.setUploadedImage} uploadedImage={this.state.uploadedImage} setUploadedImageName={this.setUploadedImageName} />
						</div>
						<div>
							{this.state.evaluate ? "Image saved" : "Image not saved"}
							<button
								type="button"
								onClick={this.onEval}
								className="btn btn-primary btn-block "
								disabled={this.state.loading}
							>
								Save
							</button>
							<button
								type="button"
								className="btn btn-primary btn-block "
								onClick={() => this.sendImgToServer(savedImage, 'solve')}
								disabled={this.state.loading || !this.state.evaluate}
							>
								Solve
							</button>
							<button
								type="button"
								className="btn btn-primary btn-block "
								onClick={() => this.sendImgToServer(savedImage, 'expand')}
								disabled={this.state.loading || !this.state.evaluate}
							>
								Expand
							</button>
							<button
								type="button"
								onClick={this.onClear}
								className="btn btn-danger btn-block "
								disabled={this.state.loading}
							>
								Clear
							</button>
							{this.state.error === "" && this.state.solved && <Link to="/feedback" state={{ 'savedImage': savedImage, 'uploadedImage': this.state.uploadedImage, 'equation': this.state.equation, 'formatted_equation': this.state.formatted_equation, 'result': this.state.result }}>
								<button
									type="button"
									className="btn btn-primary btn-block "
									style={{ marginTop: 70 }}
									disabled={this.state.loading || !this.state.solved}
								>
									Feedback
								</button>
							</Link>}
						</div>
					</div>
				</div>

				<div className="row">
					<div className="col-6 mt-5">
						{this.state.error !== "" && <div className="row">
							<h5 style={{ "textAlign": "center", "width": "100%", color: "red" }}>Error: {this.state.error}</h5>
						</div>}
						<Output
							equation={this.state.equation}
							formatted_equation={this.state.formatted_equation}
							result={this.state.result}
						/>
					</div>
					<div className="col-6" style={{ "height": "20rem", "width": "80rem", "marginBottom": "1%" }}>
						{/* {this.state.graph !== '' && <img src={"data:image/png;base64," + this.state.graph} alt="graph" />} */}
						<Graph></Graph>
					</div>
				</div>
			</div>
		);
	}
}

export default Canvas;
